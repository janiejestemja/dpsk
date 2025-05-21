from llama_cpp import Llama 

def main():
    # Load model
    llm = Llama(
        model_path="./llama.cpp/models/deepseek-llm-7b-chat.Q4_K_M.gguf",
        n_ctx=4096,
        verbose=False,
    )

    with open("system.txt") as f:
        instruction = f.read().strip()
    sysprom = Prompt(instruction)

    while True:
        try:
            user_input = input("Prompt: ")
            print("")

        except EOFError:
            print("")
            break

        else:
            sysprom.from_user(user_input)
            prompt = sysprom.get_prompt()
         
            output = llm(
                prompt,
                max_tokens=200,
                temperature=0.5,
                top_p=0.9,
                top_k=50, 
                repeat_penalty=1.1,
                stop=["<|user|>", "<|system|>"],
            )

            text_output = output["choices"][0]["text"]
            sysprom.from_assistant(text_output)

            print(text_output)

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

if __name__ == "__main__":
    main()
