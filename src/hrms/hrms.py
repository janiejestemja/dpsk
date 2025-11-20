from pathlib import Path
from llama_cpp import Llama

class Prompt():
    module_dir = Path(__file__).parent
    prompt_path = module_dir / "hrms_p.txt"

    def __init__(self, instruction):
        self.chat = [instruction]

    def from_user(self, text: str):
        self.chat.append("<|im_start|>user\n" + text + "<|im_end|>")
        self.chat.append("<|im_start|>assistant\n")

    def from_assistant(self, text: str):
        self.chat[-1] += text + "<|im_end|>"

    def get_prompt(self):
        prompt = ""
        for line in self.chat:
            prompt += line
        return prompt

    @classmethod
    def load_model(cls, model_path):
        # Try loading model
        try:
            llm = Llama(
                model_path=model_path,
                n_ctx=32768,
                verbose=False,
            )
        except Exception:
            print("Model not found.")
            raise FileNotFoundError("Unresolved model path")

        try:
            with open(cls.prompt_path) as f:
                instruction = f.read().strip()
        except Exception:
            print("Prompt not found.")
            raise FileNotFoundError("Unresolved prompt path")

        return llm, instruction

    def gen_response(self, llm):
        output = llm(
            self.get_prompt(),
            max_tokens=1024,
            temperature=0.5,
            top_p=0.9,
            top_k=50,
            repeat_penalty=1.1,
            stop=["<|im_end|>"],
        )
        return output["choices"][0]["text"]