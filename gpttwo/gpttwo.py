from transformers import GPT2Tokenizer, GPT2LMHeadModel


def main():
    model = GPT2LMHeadModel.from_pretrained("distilgpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")

    with open("system.txt", encoding="utf-8") as f:
        seed_text = f.read()

    input_text = seed_text.strip()
    print(input_text)

    for _ in range(5):
        raw_fortune = gen_output(input_text, model, tokenizer)

        left, fortune, right = raw_fortune.split('"', 2)
        print("")
        print("- " + fortune + " -")


def gen_output(input_text: str, model, tokenizer) -> str:
    tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)
    outputs = model.generate(
        inputs["input_ids"],
        max_length=64,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
        repetition_penalty=1.2
    )

    fortune = str(tokenizer.decode(outputs[0], skip_special_tokens=True))
    return fortune


if __name__ == "__main__":
    main()
