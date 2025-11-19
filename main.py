import sys
from llama_cpp import Llama

class ModelConfig:
    model_flag = None
    model_flags = ["tiny", "hrms", "dpsk"]
    model_path = "../models/"
    model_paths = {
        "tiny" : "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "hrms" : "openhermes-2.5-mistral-7b.Q4_K_M.gguf",
        "dpsk" : "deepseek-llm-7b-chat.Q4_K_M.gguf",
    }

    model_ctxl = {
        "tiny" : 2048,
        "hrms" : 32768,
        "dpsk" : 4096,
    }

    model_stops = {
        "tiny" : ["</s>"],
        "hrms" : ["<|im_end|>"],
        "dpsk" : ["\n\n"],
    }

    def __init__(self):
        if len(sys.argv) == 2 and sys.argv[1] in self.model_flags:
            self.model_flag = sys.argv[1]

        else:
            raise NotImplementedError("Please specify a valid model flag: " + ", ".join(self.model_flags))


def main():
    cfg = ModelConfig()
    match cfg.model_flag:
        case "tiny":
            from src.tiny import Prompt
            cfg.prompt = "src/tiny_p.txt"
        case "hrms":
            from src.hrms import Prompt
            cfg.prompt = "src/hrms_p.txt"
        case "dpsk":
            from src.dpsk import Prompt
            cfg.prompt = "src/dpsk_p.txt"
    # Load model
    llm = Llama(
        model_path=cfg.model_path + cfg.model_paths[cfg.model_flag],
        n_ctx=cfg.model_ctxl[cfg.model_flag],
        verbose=False,
    )

    with open(cfg.prompt) as f:
        instruction = f.read().strip()
    sysprom = Prompt(instruction)

    while True:
        try:
            print("")
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
                stop=cfg.model_stops[cfg.model_flag],
            )

            text_output = output["choices"][0]["text"]
            sysprom.from_assistant(text_output)

            print(text_output)


if __name__ == "__main__":
    main()