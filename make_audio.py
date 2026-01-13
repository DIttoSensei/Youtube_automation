import json
import asyncio
import edge_tts
import os
import time

# ================= CONFIG =================
SCRIPT_JSON = "content.json"
OUTPUT_DIR = "audio_segments"
VOICE = "en-US-GuyNeural" 
# ==========================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio():
    with open(SCRIPT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        segments = data.get("script_segments", [])

    for i, seg in enumerate(segments):
        text = seg["text"].strip()
        
        # 🪄 SAFETY: Skip if text is empty to avoid API errors
        if not text:
            print(f"⚠️ Segment {i} is empty. Skipping...")
            continue

        filename = f"{OUTPUT_DIR}/segment_{i}.mp3"
        
        # 🪄 RETRY LOGIC: Try 3 times before giving up
        for attempt in range(3):
            try:
                print(f"🎙️ Generating {filename} (Attempt {attempt + 1})...")
                communicate = edge_tts.Communicate(text, VOICE, rate="+0%")
                await communicate.save(filename)
                
                # Check if file was actually created and has size
                if os.path.exists(filename) and os.path.getsize(filename) > 0:
                    break # Success! Move to next segment
                else:
                    raise Exception("File created but is empty.")

            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed for {filename}: {e}")
                if attempt < 2:
                    await asyncio.sleep(5) # Wait 5s before retrying
                else:
                    print(f"🛑 CRITICAL: Could not generate audio for segment {i}")
                    raise # This will trigger your main.py exit(1)

        # 🪄 THROTTLING: Small pause to prevent being flagged as a bot
        await asyncio.sleep(1)

    print("\n✅ All audio segments generated!")

if __name__ == "__main__":
    asyncio.run(generate_audio())
