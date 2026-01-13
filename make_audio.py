import json
import asyncio
import edge_tts
import os

SCRIPT_JSON = "content.json"
OUTPUT_DIR = "audio_segments"
VOICE = "en-US-GuyNeural" 

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio():
    with open(SCRIPT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        segments = data.get("script_segments", [])

    for i, seg in enumerate(segments):
        text = seg["text"].strip()
        if not text: continue
        
        filename = f"{OUTPUT_DIR}/segment_{i}.mp3"
        
        # Try up to 3 times to prevent the "NoAudioReceived" crash
        for attempt in range(3):
            try:
                print(f"🎙️ Generating {filename} (Attempt {attempt+1})...")
                communicate = edge_tts.Communicate(text, VOICE)
                await communicate.save(filename)
                
                if os.path.exists(filename) and os.path.getsize(filename) > 0:
                    break 
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed: {e}")
                if attempt < 2: await asyncio.sleep(5)
                else: raise # Only fail after 3 tries

if __name__ == "__main__":
    asyncio.run(generate_audio())
