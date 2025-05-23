import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
        # "runwayml/stable-diffusion-v1-5",
        "dreamlike-art/dreamlike-photoreal-2.0",
        safety_checker=None,
        torch_dtype=torch.float32
        )
pipe = pipe.to("cpu")

prompt = "circle with four corners in the background, a moebius strip in the middleground, a square without edges in the foreground"

for i in range(6):
    image = pipe(prompt).images[0]
    image.save(f"output0{i}.png")
