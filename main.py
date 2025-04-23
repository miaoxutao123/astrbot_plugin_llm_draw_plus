from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import requests
from .ttp import generate_image

@register("pic-gen", "喵喵", "使用硅基流动api 让llm帮你画图", "0.0.2")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_key = config.get("api_key")
        # self.model = config.get("model")
        self.image_size = config.get("image_size")
        self.seed = config.get("seed")
    @llm_tool(name="pic-gen")
    async def pic_gen(self, event: AstrMessageEvent, prompt: str,model: str) -> str:
        '''
        When a user requires image generation or drawing, and asks you to create an image, or when you need to create a drawing to demonstrate or present something to the user,
        call this function. If the image description provided by the user is not in English, translate it into English and reformat it to facilitate generation by the stable-diffusion model. 
        Enrich the prompt with additional details to achieve better results, the more detailed the better. 
        Autonomously select the most suitable model based on the request: use `black-forest-labs/FLUX.1-schnell` for high-resolution images with rich details and a focus on anatomical precision,
        and use `stabilityai/stable-diffusion-3-5-large` for realistic skin textures and diverse artistic styles. **Only these two models should be used**.

        Args:
        - prompt (string): image description  
        - model (string): model name (`black-forest-labs/FLUX.1-schnell` or `stabilityai/stable-diffusion-3-5-large`)
        '''
        api_key = self.api_key
        model = model
        image_size = self.image_size
        seed = self.seed
        if seed == 0:
            seed = None
        image_url, image_path = generate_image(prompt,api_key,model=model,image_size=image_size,seed=seed)
        chain = [Image.fromURL(image_url)]
        yield event.chain_result(chain)