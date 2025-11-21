from pathlib import Path
from llama_cpp import Llama

class Prompt():
    module_dir = Path(__file__).parent
    model_flags = ["dpsk", "hrms", "phi", "tiny"]

    prompts = {
        "chat": "chat.txt",
        "todo": "todo.txt",
        "dpsk": "dpsk.txt",
    }

    tiny_config = {
        "context_length": 2048,

        "user_start_token": "<|user|>\n",
        "user_end_token": "</s>\n",
        "assistant_start_token": "<|assistant|>\n",
        "assistant_end_token": "</s>\n",
        "llm_stop_token": "</s>",

        "prompt_start_token": "<|system|>\n",
        "prompt_end_token": "</s>",
    }

    phi_config = {
        "context_length": 4096,

        "user_start_token": "<|user|>\n",
        "user_end_token": "<|end|>\n",
        "assistant_start_token": "<|assistant|>\n",
        "assistant_end_token": "<|end|>\n",
        "llm_stop_token": "<|end|>",

        "prompt_start_token": "<|system|>\n",
        "prompt_end_token": "<|end|>",
    }

    hrms_config = {
        "context_length": 32768,

        "user_start_token": "<|im_start|>user\n",
        "user_end_token": "<|im_end|>\n",
        "assistant_start_token": "<|im_start|>assistant\n",
        "assistant_end_token": "<|im_end|>\n",
        "llm_stop_token": "<|im_end|>",

        "prompt_start_token": "<|im_start|>\n",
        "prompt_end_token":"<|im_end|>",
        
    }

    dpsk_config = {
        "context_length": 4096, 

        "user_start_token": "User: ",
        "user_end_token": "\n\n",
        "assistant_start_token": "Assistant: ",
        "assistant_end_token": "\n\n",
        "llm_stop_token": "<｜end▁of▁sentence｜>",

        "prompt_start_token": "System: ",
        "prompt_end_token": "\n\n",
    }

    def __init__(self, config):
        self.config = config
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
    
    def load_instruction(self, prompt_file):
        prompt_path = self.module_dir / "prompts" / prompt_file
        try:
            with open(prompt_path) as f:
                instruction = f.read().strip()
        except Exception:
            print("Prompt not found.")
            raise FileNotFoundError("Unresolved prompt path")
        else:
            prepared_instruction = self.config["prompt_start_token"] + instruction + self.config["prompt_end_token"]
            self.instruction = prepared_instruction

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