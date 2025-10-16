import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    # "runwayml/stable-diffusion-v1-5",
    "dreamlike-art/dreamlike-photoreal-2.0",
    safety_checker=None,
    torch_dtype=torch.float32,
)
pipe = pipe.to("cpu")

prompt = "idyllic pond in the woods, mythological wildlife, surreal impressionism"

image = pipe(prompt, height=512, width=512).images[0]
image.save("target/output0.png")
