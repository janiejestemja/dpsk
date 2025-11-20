# LLM Client's
---
> Boilerplate setup for local LLM clients running without GPU. Using various `Q4_K_M` models made available by huggingface.

## Features
---
- Run a local language model in terminal
- Load in a file at the start to chat about
- Chat until context limit is reached

## Setup requirements
---
Clone the repo and change directory into it...
```bash
git clone https://github.com/janiejestemja/dpsk
cd dpsk
```


Check `g++` installation...
```bash
g++ --version
```
...or install it if necessary.

Setup a virtual environment for `Python 3.14` and install requirements...

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Download model
### TinyLLm (1.1B)
---
> [Download link to TinyLlama](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/blob/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf)

>[Link to more information about the model](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF).

### OpenHermes (7B)
---
> [Download link to OpenHermes](https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/blob/main/openhermes-2.5-mistral-7b.Q4_K_M.gguf)

> [Link to more information about the model](https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF).

### DeepSeek (7B)
---
> [Download link to DeepSeek](https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF/blob/main/deepseek-llm-7b-chat.Q4_K_M.gguf)

> [Link to more information about the model](https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF).

## Run cli
---
> Run an infinite loop with a chatbot until the context window breaks...

### Usage
---
```plaintext
main.py [-h] --model {dpsk,hrms,tiny} --model_path MODEL_PATH [--src SRC]
```
> The source argument is used to load a file to chat about. It will be appended to the initial question.

Run the following command to print available options.
```bash
python main.py -h
```

> To exit gracefully use `EOFError` (`Ctrl + D`)