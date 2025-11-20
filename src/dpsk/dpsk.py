from llama_cpp import Llama

class Prompt():
    prompt_path = "src/dpsk/dpsk_p.txt"

    def __init__(self, instruction):
        self.chat = [instruction + "\n"]

    def from_user(self, text: str):
        self.chat.append("User: " + text + "\n\n")
        self.chat.append("Assistant: ")

    def from_assistant(self, text: str):
        self.chat[-1] += text + "\n\n"

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
                n_ctx=4096,
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
            stop=["<｜end▁of▁sentence｜>"],
        )
        return output["choices"][0]["text"]