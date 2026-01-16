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
        segments = data.get("script_segments", [])[:10] 

    for i, seg in enumerate(segments):
        text = seg["text"].strip()
        if not text: continue
            
        filename = f"{OUTPUT_DIR}/segment_{i}.mp3"
        
        # --- MAGIC RETRY LOGIC START ---
        success = False
        for attempt in range(3): # Try 3 times
            try:
                print(f"Generating {filename} (Attempt {attempt + 1})...")
                communicate = edge_tts.Communicate(text, VOICE)
                await communicate.save(filename)
                success = True
                break # It worked! Exit the retry loop.
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying in 5s...")
                await asyncio.sleep(5) # Wait before trying again
        
        if not success:
            print(f"❌ Permanent failure for segment {i}")
        
        # Small "Human" pause between segments to avoid being blocked
        await asyncio.sleep(2) 
        # --- MAGIC RETRY LOGIC END ---

    print(f"\n✅ Audio generation complete!")
if __name__ == "__main__":
    asyncio.run(generate_audio())
