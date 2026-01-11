import subprocess
import os
import time
import sys

# ================= CONFIGURATION =================
SCRIPT_OUTPUT = "script_output.txt"
CONTENT_JSON = "content.json"
PROMPTS_JSON = "prompts.json"
IMAGES_DIR = "images"
AUDIO_DIR = "audio_segments"
FINAL_VIDEO = "output/final_video_subtitled.mp4"

REQUIRED_IMAGE_COUNT = 10
REQUIRED_AUDIO_COUNT = 10
STEP_DELAY = 7  # 7-second buffer
# =================================================

def run_script(script_name):
    """Runs a python script and waits for it to finish."""
    print(f"\n🚀 [MAIN] Starting: {script_name}")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"💤 Waiting {STEP_DELAY}s for system to settle...")
        time.sleep(STEP_DELAY) 
    except subprocess.CalledProcessError as e:
        print(f"❌ [MAIN] Error running {script_name}: {e}")
        sys.exit(1)

def wait_for_files(file_list, is_dir=False, required_count=0):
    """Keeps checking for files until they exist."""
    print(f"⏳ Verifying files...")
    while True:
        success = False
        if is_dir:
            if os.path.exists(file_list):
                files = [f for f in os.listdir(file_list) if f.lower().endswith(('.png', '.jpg', '.mp3'))]
                if len(files) >= required_count:
                    success = True
        else:
            if all(os.path.exists(f) for f in file_list):
                success = True
        
        if success:
            print(f"✅ Verified! Proceeding to next task.")
            break
        time.sleep(2)

def main():
    print("--- 🪄 TECH MAGE AUTOMATION STARTING ---")

    # STEP 1: Generate Script
    run_script("generate_scripts.py") 
    wait_for_files([SCRIPT_OUTPUT])

    # STEP 2: Extract JSONs
    run_script("extract.py")
    wait_for_files([CONTENT_JSON, PROMPTS_JSON])

    # STEP 3: Generate Images
    run_script("generate_image.py")
    wait_for_files(IMAGES_DIR, is_dir=True, required_count=REQUIRED_IMAGE_COUNT)

    # STEP 4: Generate Audio
    run_script("make_audio.py") 
    wait_for_files(AUDIO_DIR, is_dir=True, required_count=REQUIRED_AUDIO_COUNT)

    # STEP 5: Render Video
    run_script("make_vid.py")
    wait_for_files([FINAL_VIDEO])

    # STEP 6: Upload to YouTube
    run_script("upload.py")

    # STEP 7: Wait 7 seconds then Clear Folders
    print(f"💤 Final 7s wait before clearing folders...")
    time.sleep(STEP_DELAY)
    run_script("clear_folders.py")

    print("\n" + "="*40)
    print(f"🎉 TECH MAGE: MISSION ACCOMPLISHED!")
    print("="*40)

if __name__ == "__main__":
    main()