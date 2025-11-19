class Prompt():
    def __init__(self, instruction):
        self.system_instruction = instruction
        self.chat = [instruction]

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