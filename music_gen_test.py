import json
import requests
import asyncio
import aiohttp
import os



async def generate_audio(tags: str, lyrics: str, duration: int, comfyui_endpoint :str ,workflow_file :str) -> str:
    """
    异步生成音频文件。

    """
    # ComfyUI 服务器地址
    COMFYUI_ENDPOINT = comfyui_endpoint

    # 工作流文件路径
    WORKFLOW_FILE = workflow_file


    # 读取工作流文件
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        workflow_data = json.load(f)

    # 修改工作流中的歌词、风格标签和时长
    workflow_data["14"]["inputs"]["tags"] = tags
    workflow_data["14"]["inputs"]["lyrics"] = lyrics
    workflow_data["17"]["inputs"]["seconds"] = duration  # 设置音频时长

    # 提交工作流到 ComfyUI
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{COMFYUI_ENDPOINT}/prompt",
            json={"prompt": workflow_data}
        ) as response:
            if response.status != 200:
                raise Exception(f"提交工作流失败: {await response.text()}")
            response_data = await response.json()
            prompt_id = response_data["prompt_id"]
            print(f"任务已提交，任务 ID: {prompt_id}")

        # 轮询任务状态
        print("等待完成，3 秒查询一次...")
        while True:
            await asyncio.sleep(3)
            async with session.get(f"{COMFYUI_ENDPOINT}/history/{prompt_id}") as poll_response:
                if poll_response.status == 200:
                    poll_data = await poll_response.json()
                    if poll_data.get(prompt_id, {}).get("status", {}).get("completed", False):
                        break
                # print(".", end="", flush=True)

        # 获取生成的音频文件信息
        outputs = poll_data[prompt_id].get("outputs", {})
        if "59" not in outputs or "audio" not in outputs["59"]:
            raise KeyError(f"'audio' 不存在于响应的 'outputs' 中: {outputs}")

        # 提取音频信息
        audio_info = outputs["59"]["audio"][0]
        filename = audio_info["filename"]
        subfolder = audio_info["subfolder"]
        audio_url = f"{COMFYUI_ENDPOINT}/view?filename={filename}&subfolder={subfolder}&type=output"

        # 下载音频文件
        async with session.get(audio_url) as audio_response:
            if audio_response.status != 200:
                raise Exception(f"下载音频文件失败: {await audio_response.text()}")
            audio_data = await audio_response.read()

        # 保存音频文件
        output_file = os.path.join(subfolder, filename)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"音频已成功保存到 {output_file}")
        return output_file

# 示例调用
if __name__ == "__main__":
    tags = "pop, multilingual, emotional, duet, chinese, english"
    lyrics = """
    [verse]
    [zh]zai4ye4wan3dejie1dao4shang4man4bu4
    [zh]leng3feng1chui1guo4,si1xu4ru2chao2
    [zh]ni3dewei1xiao4xiang4xing1guang1shan3yao4
    [zh]zhao4liang4lewogudu2demei3yi1miao3

    [chorus]
    [en]You light up my world, like the stars in the sky
    [en]Your voice is the melody, that makes my heart fly
    [en]Together we sing, a harmony so true
    [en]In this endless night, I’ll always find you

    [verse]
    [zh]chuan1yue4ren2hai3xun2zhao3ni3deshen1ying3
    [zh]mei3yi1bu4dou1chong1man3leshēnqíng
    [zh]ni3dege1sheng1shi4zui4mei3defeng1jing3
    [zh]rang4wo3chen2zui4zaizhemeng4jing4

    [bridge]
    [en]Through the darkness, I’ll follow your light
    [en]A beacon of hope, shining so bright
    [en]No matter the distance, no matter the time
    [en]Our song will echo, forever in rhyme

    [chorus]
    [zh]ni3dian3liang4lewodeshi4jie4,ru2tian1shang4dexing1chen2
    [zh]ni3desheng1yin1shi4xuan2lü4,rang4wodexin1fei1xiang2
    [zh]wo3menyi1qi3ge1chang4,he2xie2er2zhen1zhi4
    [zh]zaizhewujin4deye4wan3,wo3zong3neng2zhao3dao4ni3
    """
    duration = 180  # 设置音频时长为 300 秒（5 分钟）
    asyncio.run(generate_audio(tags, lyrics, duration, comfyui_endpoint, workflow_file))
