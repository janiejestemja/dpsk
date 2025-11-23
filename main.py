import os
import sys
import argparse
from src.prompt import Prompt


# Definition of CLI
parser = argparse.ArgumentParser(description="CLI LLM Client.")
parser.add_argument("--model", choices=Prompt.model_flags, help="Model flag.", required=True)
parser.add_argument("--model_path", type=str, help="Path to model.", required=True)
parser.add_argument("--src", type=str, help="Path to source.")
args = parser.parse_args()

if not os.path.exists(args.model_path):
    sys.exit("Path to model must exist.")

# Cases defined in Prompt.model_flags
match args.model:
    case "dpsk":
        sysprom = Prompt(Prompt.dpsk_config)
    case "hrms":
        sysprom = Prompt(Prompt.hrms_config)
    case "phi":
        sysprom = Prompt(Prompt.phi_config)
    case "tiny":
        sysprom = Prompt(Prompt.tiny_config)

sysprom.load_model(args.model_path)

def todo_main(src_path):
    from src.todo_context import TodoContext
    from src.db.crud import DBcrud
    db = DBcrud()
    if db.create():
        print("Database created.")

    issue_counter = 1
    todo_paths = list(
        TodoContext.extract_codeblocks(
            src_path,
            issue_counter
        )
    )
    todo_paths.sort(key=lambda x: x.path)

    for path in todo_paths:
        for i, line_number in enumerate(path.line_numbers):
            code_block = "".join(path.code_blocks[i][2])
            db.enter(
                path.issue_numbers[i],
                path.path,
                code_block,
            )
            db.enter_advice(
                path.issue_numbers[i],
                "Placeholder"
            )

    # Turn following into unit test
    """
    for path in todo_paths:
        for i, line_number in enumerate(path.line_numbers):
            block = db.get_block(path.issue_numbers[i])
            print(block)
    """

    sysprom.load_instruction(Prompt.prompts["todo"])
    for path in todo_paths:
        for i, line_number in enumerate(path.line_numbers):
            sysprom.reset_instruction()
            code_block = "```\n" + "".join(path.code_blocks[i][2]) + "\n```"
            sysprom.from_user(code_block)
            text_output = sysprom.gen_response()
            db.enter_advice(
                path.issue_numbers[i],
                text_output,
            )

    db.close()

def main():
    if args.model == "dpsk":
        sysprom.load_instruction(Prompt.prompts["dpsk"])
    else:
        sysprom.load_instruction(Prompt.prompts["chat"])
    sysprom.reset_instruction()
    while True:
        try:
            print("")
            user_input = input("Prompt: ")
            print("")
            if user_input.startswith("load: "):
                cmd, file_path = user_input.split(": ", 1)
                with open(file_path) as f:
                    file_content = f.read()
                print(f"File provided from: {file_path} will be appended beneath.")
                print("")
                new_input = input("Prompt: ")
                user_input = new_input + "\n```\n" + "".join(file_content) + "\n```"
                print("")

        except EOFError:
            print("")
            break

        else:
            sysprom.from_user(user_input)
            try:
                text_output = sysprom.gen_response()
            except ValueError:
                sys.exit("Context limit reached. Ending session.")
            else:
                sysprom.from_assistant(text_output)
                print(text_output)


if __name__ == "__main__":
    if args.src:
        todo_main(args.src)
    else:
        main()