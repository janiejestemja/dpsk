import os
import sys
import argparse

model_flags = ["dpsk", "hrms", "tiny"]

# Definition of CLI
parser = argparse.ArgumentParser(description="CLI LLM Client.")
parser.add_argument("--model", choices=model_flags, help="model flag", required=True)
parser.add_argument("--model_path", type=str, help="Path to model", required=True)
parser.add_argument("--src", type=str, help="Path to file.")
args = parser.parse_args()

# Load model
if not os.path.exists(args.model_path):
    sys.exit("Path to model must exist.")

match args.model:
    case "dpsk":
        from src.dpsk import dpsk
        llm, instruction = dpsk.Prompt.load_model(args.model_path)
        sysprom = dpsk.Prompt(instruction)
    case "hrms":
        from src.hrms import hrms
        llm, instruction = hrms.Prompt.load_model(args.model_path)
        sysprom = hrms.Prompt(instruction)
    case "tiny":
        from src.tiny import tiny
        llm, instruction = tiny.Prompt.load_model(args.model_path)
        sysprom = tiny.Prompt(instruction)

def todo_main():
    with open(args.src) as f:
        file_content = f.read()
    print("File provided from:\n", args.src)

    example_instruction = "Could you please give me summary of the following file?\n"
    print("Example instruction:\n", example_instruction)

    instruction = input("Initial question:\n")
    inital_prompt = instruction + "```n" + "".join(file_content) + "\n```"
    sysprom.from_user(inital_prompt)
    try:
        text_output = sysprom.gen_response(llm)
    except ValueError:
        sys.exit("Input file to long. Ending session.")
    else:
        sysprom.from_assistant(text_output)
        print("Summary of given file:\n", text_output)

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
            try:
                text_output = sysprom.gen_response(llm)
            except ValueError:
                sys.exit("Context limit reached. Ending session.")
            else:
                sysprom.from_assistant(text_output)
                print(text_output)

def main():
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
            try:
                text_output = sysprom.gen_response(llm)
            except ValueError:
                sys.exit("Context limit reached. Ending session.")
            else:
                sysprom.from_assistant(text_output)
                print(text_output)


if __name__ == "__main__":
    if args.src:
        todo_main()
    else:
        main()