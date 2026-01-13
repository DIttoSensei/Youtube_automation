import json
import asyncio
import edge_tts
import os

# ================= CONFIG =================
SCRIPT_JSON = "content.json"
OUTPUT_DIR = "audio_segments"
VOICE = "en-US-GuyNeural" 
# ==========================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio():
    with open(SCRIPT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Get segments, but FORCE it to only take the first 10
        segments = data.get("script_segments", [])[:10] 

    for i, seg in enumerate(segments):
        text = seg["text"].strip() # .strip() removes hidden empty spaces
        
        if not text:
            print(f"⚠️ Warning: Segment {i} is empty! Skipping to avoid crash.")
            continue
            
        filename = f"{OUTPUT_DIR}/segment_{i}.mp3"
        print(f"Generating {filename}...")

        # Added a try/except here so one bad segment doesn't kill the whole run
        try:
            communicate = edge_tts.Communicate(text, VOICE, rate="+0%")
            await communicate.save(filename)
        except Exception as e:
            print(f"❌ Failed to generate audio for segment {i}: {e}")

    print(f"\n✅ Audio generation complete! (Processed {len(segments)} segments)")

if __name__ == "__main__":
    asyncio.run(generate_audio())
