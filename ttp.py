import requests
import json
import time
import random
def generate_image(prompt,api_key,model="stabilityai/stable-diffusion-3-5-large",seed=None,image_size = "1024x1024"):
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

    while True:
        response = requests.request("POST", url, json=payload, headers=headers)
        data = json.loads(response.text)

        if data.get("code") == 50603:
            print("System is too busy now. Please try again later.")
            time.sleep(1)
            continue

        if 'images' in data:
            for image in data['images']:
                image_url = image['url']
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_path = 'downloaded_image.jpeg'
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
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
    api_key = "不告诉你"
    image_url, image_path = generate_image(prompt, api_key, model="black-forest-labs/FLUX.1-schnell")
    print(f"Image URL: {image_url}, Image Path: {image_path}")