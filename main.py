from src import Prompt

def main():
    llm, instruction = Prompt.load_model()
    sysprom = Prompt(instruction)

    while True:
        try:
            print("")
            user_input = input("Prompt: ")

            if user_input.startswith("load: "):
                _, filepath = user_input.split("load: ", 1)
                with open(filepath) as f:
                    file_content = f.read()
                print("File loaded")
                print("")
                user_input = input("Prompt: ")
                user_input = user_input + "\n```\n" + file_content + "\n```"
                
            print("")

        except EOFError:
            print("")
            break

        else:
            sysprom.from_user(user_input)
            prompt = sysprom.get_prompt()
            text_output = sysprom.gen_response(
                llm,
                prompt,
            )
            sysprom.from_assistant(text_output)

            print(text_output)


if __name__ == "__main__":
    main()