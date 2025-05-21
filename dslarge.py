import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

def main():
    model_name = "deepseek-ai/deepseek-llm-7b-chat"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )

    tokenizer.pad_token = tokenizer.eos_token
    model.generation_config = GenerationConfig.from_pretrained(model_name)
    model.generation_config.pad_token_id = model.generation_config.eos_token_id

    messages = [
        {"role": "system", "content": "You are a wise Alchemist."},
        {"role": "user", "content": "Who are you?"}
    ]

    input_tensor = tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt"
    )
    outputs = model.generate(input_tensor.to(model.device), max_new_tokens=100)
    result = tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)

    print(result)

if __name__ == "__main__":
    main()
