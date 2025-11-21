from pathlib import Path
from llama_cpp import Llama

class Prompt():
    module_dir = Path(__file__).parent
    model_flags = ["dpsk", "hrms", "phi", "tiny"]

    tiny_config = {
        "prompt_file": "tiny_p.txt",
        "context_length": 2048,

        "user_start_token": "<|user|>\n",
        "user_end_token": "</s>\n",
        "assistant_start_token": "<|assistant|>\n",
        "assistant_end_token": "</s>\n",
        "llm_stop_token": "</s>",
    }

    phi_config = {
        "prompt_file": "phi_p.txt",
        "context_length": 4096,

        "user_start_token": "<|user|>\n",
        "user_end_token": "<|end|>\n",
        "assistant_start_token": "<|assistant|>\n",
        "assistant_end_token": "<|end|>\n",
        "llm_stop_token": "<|end|>",
    }

    hrms_config = {
        "prompt_file": "hrms_p.txt",
        "context_length": 32768,

        "user_start_token": "<|im_start|>user\n",
        "user_end_token": "<|im_end|>\n",
        "assistant_start_token": "<|im_start|>assistant\n",
        "assistant_end_token": "<|im_end|>\n",
        "llm_stop_token": "<|im_end|>",
    }

    dpsk_config = {
        "prompt_file": "dpsk_p.txt",
        "context_length": 4096, 

        "user_start_token": "User: ",
        "user_end_token": "\n\n",
        "assistant_start_token": "Assistant: ",
        "assistant_end_token": "\n\n",
        "llm_stop_token": "<｜end▁of▁sentence｜>",
    }

    def __init__(self, config):
        self.config = config
        self.prompt_path = self.module_dir / "prompts" / self.config["prompt_file"]
        self.chat = []
        self.instruction = None
        self.llm = None
    
    def from_user(self, text: str):
        self.chat.append(
            self.config["user_start_token"] + text + self.config["user_end_token"]
        )
        self.chat.append(self.config["assistant_start_token"])
    
    def from_assistant(self, text: str):
        self.chat[-1] += text + self.config["assistant_end_token"]

    def get_prompt(self):
        return "".join(self.chat)

    def load_model(self, model_path):
        try:
            llm = Llama(
                model_path=model_path,
                n_ctx=self.config["context_length"],
                verbose=False,
            )

        except Exception:
            print("Model not found.")
            raise FileNotFoundError("Unresolved model path")

        else:
            self.llm = llm
    
    def load_instruction(self):
        try:
            with open(self.prompt_path) as f:
                instruction = f.read().strip()
        except Exception:
            print("Prompt not found.")
            raise FileNotFoundError("Unresolved prompt path")
        else:
            self.instruction = instruction

    def reset_instruction(self):
        self.chat = [self.instruction]
    
    def gen_response(self):
        output = self.llm(
            self.get_prompt(),
            max_tokens=1024,
            temperature=0.5,
            top_p=0.9,
            top_k=50,
            repeat_penalty=1.1,
            stop=[self.config["llm_stop_token"]],
        )
        return output["choices"][0]["text"]