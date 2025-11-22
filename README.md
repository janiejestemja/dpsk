# LLM Client's
---
> Boilerplate setup for local LLM client running without GPU. Using various `Q4_K_M` models made available by huggingface.

## Features
---
- Run a local language model in terminal (chat)
  - Load in a file (to chat about)
  - Chat until context limit is reached
- Scan a code base for todo-inline comments
  - Store findings and metadata in a database (SQLite)
  - Generate llm advice about how to finish what is to do
  - View database per Webinterface via local server (uvicorn, FastAPI)

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
### TinyLLm
---
> [Download link to TinyLlama (1.1B)](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/blob/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf)

>[Link to more information about the model](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF).

### Phi-3-mini 
---
> [Download link to Phi-3-mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)

> [Link to more information about the model](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)

### OpenHermes
---
> [Download link to OpenHermes (7B)](https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/blob/main/openhermes-2.5-mistral-7b.Q4_K_M.gguf)

> [Link to more information about the model](https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF).

### DeepSeek
---
> [Download link to DeepSeek (7B)](https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF/blob/main/deepseek-llm-7b-chat.Q4_K_M.gguf)

> [Link to more information about the model](https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF).

## Usage
---

### Run cli
---
Run an infinite loop with a chatbot until the context window breaks...

```plaintext
main.py [-h] --model {dpsk,hrms,phi,tiny} --model_path MODEL_PATH [--src SRC]
```

Run the following command to print available options.
```bash
python main.py -h
```

To exit gracefully use `EOFError` (`Ctrl + D`)

### Run local server
---
When running the `main.py` script point the `--src` path to the directory to be scanned for todo's to fill the database.

Change directory into the `src` directory and run...
```bash
uvicorn api:app --reload
```
...to view the database in your browser on localhost.