class Prompt():
    def __init__(self, instruction):
        self.system_instruction = instruction
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