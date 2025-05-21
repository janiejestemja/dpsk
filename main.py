from llama_cpp import Llama
from hermes import Prompt


def main():
    # Load model
    llm = Llama(
        model_path="../models/openhermes-2.5-mistral-7b.Q4_K_M.gguf",
        n_ctx=32768,  # 4096,
        verbose=False,
    )

    with open("prompt.txt") as f:
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
                max_tokens=1024,
                temperature=0.5,
                top_p=0.9,
                top_k=50,
                repeat_penalty=1.1,
                stop=["<|im_end|>"],
            )

            text_output = output["choices"][0]["text"]
            sysprom.from_assistant(text_output)

            print(text_output)


if __name__ == "__main__":
    main()