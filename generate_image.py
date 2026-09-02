import os
import json
import requests
import time
import base64

# ---------------- CONFIG (CLOUD READY) ----------------
# We pull these directly from GitHub's environment variables
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
API_TOKEN = os.getenv("API_TOKEN")

MODEL = "@cf/black-forest-labs/flux-1-schnell"
PROMPTS_FILE = "prompts.json"
OUTPUT_DIR = "images"

# Safety check: Stop the script if the keys are missing
if not ACCOUNT_ID or not API_TOKEN:
    print("❌ ERROR: Missing ACCOUNT_ID or CLOUDFLARE_API_TOKEN in environment!")
    exit(1)
# ------------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"

with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)["prompts"]

print(f"🚀 Decoding Base64 images from Cloudflare into /{OUTPUT_DIR}...")

for index, prompt in enumerate(prompts):
    image_name = f"image_{index+1}.png"
    image_path = os.path.join(OUTPUT_DIR, image_name)
    
    print(f"🎨 Generating {index+1}/{len(prompts)}...", end="", flush=True)

    payload = {
        "prompt": f"{prompt}, high quality, realistic, 8k",
        "steps": 4 
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Cloudflare returns: {"result": {"image": "BASE64_STRING_HERE"}}
            if "result" in data and "image" in data["result"]:
                image_base64 = data["result"]["image"]
                
                # Convert the text string back into actual image bytes
                image_binary = base64.b64decode(image_base64)
                
                with open(image_path, "wb") as f:
                    f.write(image_binary)
                print(" ✅ SUCCESS")
            else:
                print(f" ❌ UNEXPECTED JSON FORMAT: {data}")
        else:
            print(f" ❌ ERROR {response.status_code}: {response.text}")

        time.sleep(1)

    except Exception as e:
        print(f" ❌ SCRIPT ERROR: {e}")

print("\n✨ All images decoded and saved! You can open them now.")
