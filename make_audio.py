import json
import asyncio
import edge_tts
import os

# ================= CONFIG =================
SCRIPT_JSON = "content.json"
OUTPUT_DIR = "audio_segments"
# Recommendation: "en-US-GuyNeural" or "en-US-AriaNeural"
VOICE = "en-US-GuyNeural" 
# ==========================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio():
    with open(SCRIPT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        segments = data.get("script_segments", [])

    for i, seg in enumerate(segments):
        text = seg["text"]
        start_time = seg["start"]
        end_time = seg["end"]
        duration = end_time - start_time
        
        filename = f"{OUTPUT_DIR}/segment_{i}.mp3"
        print(f"Generating {filename}...")

        # We can adjust the rate (speed) to try and fit the duration
        # +0% is normal speed. 
        communicate = edge_tts.Communicate(text, VOICE, rate="+0%")
        await communicate.save(filename)

    print("\n✅ All audio segments generated!")

if __name__ == "__main__":
    asyncio.run(generate_audio())
