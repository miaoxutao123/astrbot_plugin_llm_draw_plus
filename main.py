from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import astrbot.api.message_components as Comp
from .ttp import generate_image
from .music_gen_test import generate_audio
from .file_send_server import send_file
import subprocess

@register("pic-gen", "喵喵", "使用硅基流动api 让llm帮你画图", "0.0.2")
class MyPlugin(Star):
    def __init__(self, context: Context,config: dict):
        super().__init__(context)
        self.api_key = config.get("api_key")
        # self.model = config.get("model")
        self.image_size = config.get("image_size")
        self.seed = config.get("seed")
        self.comfyui_endpoint = config.get("comfyui_endpoint")
        self.nap_server_address = config.get("nap_server_address")
        self.nap_server_port = config.get("nap_server_port")
    @llm_tool(name="pic-gen")
    async def pic_gen(self, event: AstrMessageEvent, prompt: str, model: str) -> str:
        """
        When a user requires image generation or drawing, and asks you to create an image, 
        or when you need to create a drawing to demonstrate or present something to the user, 
        call this function. If the image description provided by the user is not in English,
        translate it into English and reformat it to facilitate generation by the stable-diffusion model.
        **Autonomously enrich the prompt with additional details to achieve better results**,
        focusing on clarity, specificity, and context, without asking the user for further requirements.
        Autonomously select the most suitable model based on the request: 
        use `black-forest-labs/FLUX.1-schnell` for high-resolution images with rich details and a focus on anatomical precision,
        and use `stabilityai/stable-diffusion-3-5-large` for realistic skin textures and diverse artistic styles. **Only these two models should be used**.

        Args:  
            prompt (string): Image description provided by the user, which will be enriched autonomously.  
            model (string): Model name (`black-forest-labs/FLUX.1-schnell` or `stabilityai/stable-diffusion-3-5-large`).
        """
        # 确保从配置中正确加载
        api_key = self.api_key
        image_size = self.image_size
        seed = self.seed

        # 如果 seed 为 0，设置为 None
        if seed == 0:
            seed = None

        # 调用生成图像的函数
        image_url, image_path =await generate_image(prompt, api_key, model=model, image_size=image_size, seed=seed)

        # 返回生成的图像
        chain = [Image.fromURL(image_url)]
        yield event.chain_result(chain)

    # @llm_tool(name="music-gen")
    # async def music_gen(self, event: AstrMessageEvent,tags: str, lyrics: str, duration: int) -> str:
    #     """
    #     When a user needs to generate music, you should call this function to complete the audio generation task. 
    #     If the information provided by the user is vague, you should generate the required content on your own 
    #     without asking the user again. If the user provides relevant information, you should strictly generate 
    #     the parameters in the above format to ensure that the structure of the tags and lyrics is clear and meets 
    #     the requirements.

    #     STRICT REQUIREMENTS:
    #     - The `tags` parameter must be a comma-separated string describing the style, scene, instruments, vocal types, 
    #     or professional terms of the music. Examples:
    #         - Music styles: pop, electronic, rock, soul, cyberpunk
    #         - Scene types: background music for parties, radio broadcasts, workout playlists
    #         - Instrument elements: saxophone, piano, violin
    #         - Vocal types: female voice, male voice, clean vocals
    #         - Professional terms: 110 bpm, fast tempo, acoustic guitar

    #     - The `lyrics` parameter must strictly follow the given format:
    #         - Use structural tags such as [verse], [chorus], [bridge], etc.
    #         - Use language tags such as [zh] for Chinese, [ko] for Korean, [es] for Spanish, [fr] for French.
    #         - For Chinese lyrics, use a pinyin-like format. Example:
    #             [verse]
    #             [zh]wo3zou3guo4shen1ye4de5jie1dao4
    #             [zh]leng3feng1chui1luan4si1nian4de5piao4liang4wai4tao4
    #             [chorus]
    #             [zh]ni3shi4wo3zui4hao3de5peng2you3

    #     - The `duration` parameter must be an integer representing the desired duration of the generated audio 
    #     (in seconds). The maximum duration is 180 seconds.

    #     Note:
    #     - The ComfyUI server must be running and accessible through the specified endpoint.
    #     - The workflow file must be correctly formatted and compatible with the ComfyUI server.
    #     - The language tags in the lyrics must match the supported languages; otherwise, the generated results 
    #     may not meet expectations.
    #     """
    #     comfyui_endpoint = self.comfyui_endpoint
    #     workflow_file = "data/plugins/astrbot_plugin_llm_draw_plus/wrokflow/music/ace_step.json"

    #     music_gen_path =await generate_audio(tags, lyrics, duration, comfyui_endpoint, workflow_file)
    #     # 使用ffmpeg将MP3格式转换为WAV格式
    #     wav_path = music_gen_path.replace(".mp3", ".wav")
    #     subprocess.run(["ffmpeg", "-i", music_gen_path, wav_path], check=True)

    #     # 更新路径为WAV文件路径
    #     music_gen_path = wav_path
    #     # if self.nap_server_address != "localhost":
    #     #     nap_file_path = await send_file(music_gen_path, HOST=self.nap_server_address, PORT=self.nap_server_port)
                    

    #     chain = [
    #         Comp.Record.fromFileSystem(path = wav_path)
    #     ]
    #     yield event.chain_result(chain)
    

