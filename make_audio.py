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
        
        success = False
        for attempt in range(4): # Increased to 4 attempts
            try:
                # We create a NEW Communicate object every single time
                communicate = edge_tts.Communicate(text, VOICE)
                await communicate.save(filename)
                
                # Validation: Check if file exists AND has content
                if os.path.exists(filename) and os.path.getsize(filename) > 0:
                    print(f"✅ Segment {i} success on attempt {attempt + 1}")
                    success = True
                    break 
                else:
                    # If file is 0 bytes, delete it so we can try fresh
                    if os.path.exists(filename): os.remove(filename)
                    raise Exception("Empty file received")
                    
            except Exception as e:
                wait_time = (attempt + 1) * 5 # Incremental wait (5s, 10s, 15s)
                print(f"⚠️ Segment {i} failed: {e}. Cooling down for {wait_time}s...")
                await asyncio.sleep(wait_time)
        
        if not success:
            print(f"❌ FATAL: Could not generate audio for segment {i}")
        
        # INCREASED PAUSE: This is the 'Set it and Forget it' secret
        # 5 seconds is slow, but it's 100% safer for automation
        await asyncio.sleep(5) 

    print(f"\n✅ All segments processed!")
    print(f"\n✅ Audio generation complete!")
if __name__ == "__main__":
    asyncio.run(generate_audio())
