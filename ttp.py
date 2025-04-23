import requests
import json
import time
import random
import aiohttp
import asyncio
import aiofiles
async def generate_image(prompt, api_key, model="stabilityai/stable-diffusion-3-5-large", seed=None, image_size="1024x1024"):
    url = "https://api.siliconflow.cn/v1/images/generations"

    if seed is None:
        seed = random.randint(0, 9999999999)

    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": image_size,
        "seed": seed
    }
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.post(url, json=payload, headers=headers) as response:
                data = await response.json()

                if data.get("code") == 50603:
                    print("System is too busy now. Please try again later.")
                    await asyncio.sleep(1)
                    continue

                if 'images' in data:
                    for image in data['images']:
                        image_url = image['url']
                        async with session.get(image_url) as img_response:
                            if img_response.status == 200:
                                image_path = 'downloaded_image.jpeg'
                                async with aiofiles.open(image_path, 'wb') as f:
                                    await f.write(await img_response.read())
                                print(f"Image downloaded from {image_url}")
                                return image_url, image_path
                            else:
                                print(f"Failed to download image from {image_url}")
                                return None, None
                else:
                    print("No images found in the response.")
                    return None, None


if __name__ == "__main__":
    # Example call
    prompt = (
        "A cute catgirl with blue hair, realistic and anthropomorphic, "
        "wearing a stylish outfit, standing in a serene forest with soft sunlight, "
        "detailed fur texture, expressive eyes, and a gentle smile."
    )
    api_key = ""
    image_url, image_path = generate_image(prompt, api_key, model="black-forest-labs/FLUX.1-schnell")
    print(f"Image URL: {image_url}, Image Path: {image_path}")