import os
import json
import requests

# ---------------- CONFIG ----------------
API_URL = "https://api.imagegpt.online/generate/text-image"
API_KEY = "imagegpt-2VSCramD5uaXSRtG8ydYGS6Ht0j1"

WIDTH = 1080
HEIGHT = 1920
BASE_SEED = 51
MODEL = "flux"
MAX_IMAGES = 10

PROMPTS_FILE = "prompts.json"
OUTPUT_DIR = "images"
# ----------------------------------------

# Create images folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load prompts
with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)["prompts"][:MAX_IMAGES]

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

for index, prompt in enumerate(prompts):
    seed = BASE_SEED + index

    payload = {
        "prompt": prompt,
        "width": WIDTH,
        "height": HEIGHT,
        "seed": seed,
        "model": MODEL,
        "outputType": "binary"
    }

    print(f"🎨 Generating image {index + 1}/{len(prompts)} (seed={seed})")

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        image_path = os.path.join(OUTPUT_DIR, f"image_{index + 1}.png")
        with open(image_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved: {image_path}")
    else:
        print(f"❌ Failed image {index + 1}: {response.status_code}")
        print(response.text)
print(" Image generation complete!")