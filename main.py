import subprocess
import os
import time
import sys
import json

# ================= CONFIGURATION =================
SCRIPT_OUTPUT = "script_output.txt"
CONTENT_JSON = "content.json"
PROMPTS_JSON = "prompts.json"
IMAGES_DIR = "images"
AUDIO_DIR = "audio_segments"
FINAL_VIDEO = "output/final_video_subtitled.mp4"

REQUIRED_COUNT = 10
MAX_AI_RETRIES = 5  # How many times to try re-generating if segment count is wrong
STEP_DELAY = 5      # Seconds to wait between steps
# =================================================

def run_script(script_name):
    """Runs a python script and waits for it to finish."""
    print(f"\n🚀 [MAIN] Starting: {script_name}")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        time.sleep(STEP_DELAY) 
    except subprocess.CalledProcessError as e:
        print(f"❌ [MAIN] Error running {script_name}: {e}")
        return False
    return True

def clean_failed_attempt():
    """Deletes temporary files so the AI starts fresh on retry."""
    files_to_wipe = [SCRIPT_OUTPUT, CONTENT_JSON, PROMPTS_JSON]
    for f in files_to_wipe:
        if os.path.exists(f):
            os.remove(f)
    print("🧹 Workspace cleared for fresh retry.")

def check_segment_count():
    """Checks if CONTENT_JSON has exactly the required number of segments."""
    if not os.path.exists(CONTENT_JSON):
        return False
    try:
        with open(CONTENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            count = len(data.get("script_segments", []))
            print(f"📊 Quality Check: Found {count} segments.")
            return count == REQUIRED_COUNT
    except Exception as e:
        print(f"⚠️ Error reading JSON: {e}")
        return False

def main():
    print("--- 🪄 TECH MAGE AUTOMATION: ACTIVATED ---")

    # --- STEP 1 & 2: REGENERATION LOOP ---
    script_ready = False
    for attempt in range(MAX_AI_RETRIES):
        print(f"\n🎬 [PHASE 1] Script Generation Attempt {attempt + 1} of {MAX_AI_RETRIES}")
        
        run_script("generate_scripts.py")
        run_script("extract.py")

        if check_segment_count():
            script_ready = True
            break
        else:
            print(f"⚠️ Segment count incorrect (Not {REQUIRED_COUNT}).")
            clean_failed_attempt()

    if not script_ready:
        print("❌ FATAL: AI failed to produce 10 segments after multiple tries. Exiting.")
        sys.exit(1)

    # --- STEP 3: ASSETS ---
    run_script("generate_image.py")
    run_script("make_audio.py") 

    # --- STEP 4: RENDER ---
    if not run_script("make_vid.py"):
        print("❌ Video render failed.")
        sys.exit(1)

    # --- STEP 5: DEPLOYMENT ---
    # We use 'if' so that if FB fails, we can still try YouTube
    print("\n🌍 [PHASE 2] Starting Social Deployment...")
    run_script("upload_facebook.py")
    run_script("upload.py")

    # --- STEP 6: CLEANUP ---
    print("\n🧹 Mission Accomplished. Cleaning folders...")
    run_script("clear_folders.py")
    print("✅ SYSTEM READY FOR NEXT RUN.")

if __name__ == "__main__":
    main()
