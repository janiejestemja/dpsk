# DeepSeek Client
---
Boilerplate LLM client.

## Pytorch installation
---
```python
pip install torch
```
## llama.cpp quickstart
---
Requirement: cmake
```bash
sudo dnf install cmake
```

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build -DLLAMA_CURL=OFF
cmake --build build --config Release
```

The llama.cpp directory contains a subdirectory named models where the models are expected to be found. 

[Link to models](https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF/blob/main/README.md).

## Other huggingface transformers
---
```bash
pip install "transformers[torch]"
```
