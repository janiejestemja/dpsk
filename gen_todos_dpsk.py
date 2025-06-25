import os
import re
import sys
import datetime

from llama_cpp import Llama 

class TodoPath():
    todo_call = re.compile(r"\btodo!\s*\(") 
    todo_comment = re.compile(r"//\s*(TODO)\b", re.IGNORECASE)
    fixme_comment = re.compile(r"//\s*(FIXME)\b", re.IGNORECASE) 
    fn_pattern = re.compile(r"^\s*(pub\s+)?(async\s+)?(unsafe\s+)?fn\s+(\w+)\s*\(")

    def __init__(self, path):
        self.path = path

    @classmethod
    def scan_for_todos(cls, filepath):
        with open(filepath, errors="ignore") as f:
            lines = f.readlines()

        findings = []
        current_fn = None
        for i, line in enumerate(lines):
            fn_match = cls.fn_pattern.match(line)
            if fn_match:
                current_fn = fn_match.group(4)

            line_number = i + 1

            if cls.todo_call.search(line):
                findings.append({
                    "line_number": line_number,
                    "description": f"*todo!()* in *function*: {current_fn}" if current_fn else "no function?"
                    })
            elif cls.todo_comment.search(line):
                findings.append({
                    "line_number": line_number,
                    "description": "*TODO*"
                })

            elif cls.fixme_comment.search(line):
                findings.append({
                    "line_number": line_number,
                    "description": "*FIXME*"
                })

        return findings

class TodoContext(TodoPath):
    upper_margin = 50
    lower_margin = 50

    def __init__(self, path):
        super().__init__(path)
        # Filled by static method of TodoPath
        self.first_findings = []

        # Parsed first findings
        self.line_numbers = []
        self.descriptions = []

        # Code context - list[tuple(start_line, end_line, code_block)]
        self.code_blocks = []

    @classmethod
    def initialize_paths(cls):

        todo_paths = set()
        # Crawling through current work directory
        for root, _, files in os.walk("../from_github/datex-core/"):

            for file in files:
                # Checking rust files
                if file.endswith(".rs"):

                    path = os.path.join(root, file)
                    # Checking regexes via parent class 
                    findings = cls.scan_for_todos(path)
                    if findings:
                        tempTodoPath = TodoContext(path)
                        for f in findings:
                            # Memorize first findings
                            tempTodoPath.first_findings.append(f)
                        todo_paths.add(tempTodoPath)

        # Separation of line numbers and descriptions of first findings
        for path in todo_paths:
            path.line_numbers += [x["line_number"] for x in path.first_findings]
            path.descriptions += [x["description"] for x in path.first_findings]
     
        # Exctract code blocks 
        for path in todo_paths:
            for line_number in path.line_numbers:
                # Circumvent naively indexing out of bounds
                context_start = 0 if line_number - cls.upper_margin < 0 else line_number - cls.upper_margin
                context_end = line_number + cls.lower_margin

                with open(path.path) as f:
                    lines = f.readlines()
                    # Try to apply upper margin or fall back to line where todo was detected
                    try:
                        context_block = lines[context_start: context_end]
                    except Exception:
                        context_block = lines[context_start: line]

                    # Memorize code_block and metadata
                    path.code_blocks.append((context_start, context_end, context_block))

        # Return list of instances of this class
        return todo_paths

    @staticmethod
    def write_report(out_file):
        todo_paths = list(TodoContext.initialize_paths())
        todo_paths.sort(key=lambda x: x.path)
        
        # Set counters
        total_count = 0
        lines_of_context = 0

        todo_call_count = 0
        todo_comment_count = 0
        fixme_comment_count = 0

        # Count
        for path in todo_paths:
            for i, code_block in enumerate(path.code_blocks):
                total_count += 1 
                if path.descriptions[i].startswith("*todo!()*"):
                    todo_call_count += 1
                elif path.descriptions[i].startswith("*TODO*"):
                    todo_comment_count += 1
                elif path.descriptions[i].startswith("*FIXME*"):
                    fixme_comment_count += 1

                lines_of_context += code_block[1] - code_block[0]

        # Overwrite with Header
        with open(out_file, "w") as f:
            print(f"Found: {len(todo_paths)} files with todo markings.")
            f.write("# Todo check...\n")
            f.write(f"...found: {len(todo_paths)} files to do.\n")
            f.write(f"Date of running this check: {datetime.datetime.now().date()}.\n")
            f.write("\n")

            f.write(f"These files contain: {total_count} todo expressions.\n")
            f.write(f"- {todo_call_count} todo!()'s.\n")
            f.write(f"- {todo_comment_count} TODO's.\n")
            f.write(f"- {fixme_comment_count} FIXME's.\n")
            f.write("\n")

            f.write(f"Total lines of context: {lines_of_context} ~ 100 per todo: missing {total_count * 100 - lines_of_context} lines.\n")


        # Append to file
        with open(out_file, "a") as f:
            for i, path in enumerate(todo_paths):
                f.write(" \n")
                f.write(f"## f{i:02n}:" + str(path.path) + "\n")

                for x, y in zip(path.line_numbers, path.descriptions):
                    f.write(f"- {x:4n}: {y}\n")

            f.write("\n")

class Prompt():
    def __init__(self, instruction):
        self.system_instruction = instruction
        self.chat = [instruction]

    def from_user(self, text: str):
        self.chat.append("<|user|>" + text)
        self.chat.append("<|assistant|>")

    def from_assistant(self, text: str):
        self.chat[-1] += text

    def get_prompt(self):
        prompt = ""
        for line in self.chat:
            prompt += line
        return prompt

def main():
    todo_paths = list(TodoContext.initialize_paths())
    todo_paths.sort(key=lambda x: x.path)

    model_path = "./llama.cpp/models/deepseek-llm-7b-chat.Q4_K_M.gguf"
    # Load model
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        verbose=False,
    )

    with open("system.txt") as f:
        instruction = f.read().strip()

    for i, todo_path in enumerate(todo_paths):
        for j, code_block in enumerate(todo_path.code_blocks):
            print()
            print("Init new prompt...")
            sysprom = Prompt(instruction)

            user_input = "```rust\n" + str([line for line in code_block]) + "```"

            sysprom.from_user(user_input)
            prompt = sysprom.get_prompt()

            print("Generating answer...")
            output = llm(
                prompt,
                max_tokens=2_000,
                temperature=0.4, 
                top_p=0.9, 
                top_k=60,
                repeat_penalty=1.1,
                stop=["<|user|>", "<|system|>"],
             )

            text_output = output["choices"][0]["text"]
            # Enable for stacking chat
            # sysprom.from_assistant(text_output)
            print(text_output)

            print("Writing file with answer...")
            with open(f"./answers/f{i:02n}l{j:02n}.md", "w") as f:
                f.write(f"{todo_path.path}\n")
                f.write(f"{todo_path.line_numbers[j]}\n")
                f.write(f"{todo_path.descriptions[j]}\n")
                f.write("Answer:\n")
                f.write(text_output)

def write_todo_list(out_file):
    TodoContext.write_report(out_file)

if __name__ == "__main__":
    if len(sys.argv) <2:
        main()

    elif len(sys.argv) > 2:
        print("Need output file name")
        sys.exit()

    else:
        print("Legacy main...")
        out_file = sys.argv[1]
        write_todo_list(out_file)
        print(f"Report written to '{out_file}'.") 
