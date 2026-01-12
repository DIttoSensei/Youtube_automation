import os
import requests
import json
import re
import sys
from datetime import datetime

# ================= CONFIG =================
VIDEO_PATH = "output/final_video_subtitled.mp4"
SCRIPT_FILE = "script_output.txt"
LOG_FILE = "automation_errors.log"
# ==========================================

ai_disclosure = "ℹ️ This video includes AI-generated narration and/or visuals."

def log_error(message):
    """Logs errors so you can check them later without stopping the whole process."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] FB_ERROR: {message}\n")
    print(f"⚠️ LOGGED TO FILE: {message}")

def get_viral_caption():
    """Constructs a high-engagement caption using YOUR exact viral structure."""
    header = "🧙‍♂️ TECH MAGE CHRONICLES"
    headline = "THE AI REVOLUTION IS HERE. ARE YOU READY? 💻🚀"
    dynamic_hook = "Breaking down the future of technology."

    # --- YOUR ORIGINAL HOOK EXTRACTION ---
    try:
        if os.path.exists(SCRIPT_FILE):
            with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                texts = re.findall(r'"text":\s*"(.*?)"', content)
                if texts:
                    words = texts[0].split()
                    dynamic_hook = " ".join(words[:8]) + "..."
    except Exception as e:
        log_error(f"Could not parse hook: {e}")

    # --- YOUR EXACT VIRAL CAPTION FORMAT ---
    caption = f"""{header}
{headline}

{dynamic_hook}

I'm deep-diving into the tech that actually matters. Don't get left behind in the analog age. ⚡

What's inside:
🔥 Future-Proof AI Insights
🔥 Expert Tech Breakdown
🔥 No-Fluff Innovation

{ai_disclosure}

#TechMage #AI #ArtificialIntelligence #FutureTech #Programming #ComputerScience #TechNews #Innovation #Software #CodingLife #ViralTech #TechTrends2026 #MadeWithAI"""
    
    return caption

def upload_to_facebook():
    """Uploads with a safety check so YouTube can still run if this fails."""
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    
    if not page_id or not access_token:
        log_error("Credentials missing (FB_PAGE_ID/TOKEN)")
        return

    if not os.path.exists(VIDEO_PATH):
        log_error(f"Video file not found at {VIDEO_PATH}")
        return

    url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"
    caption = get_viral_caption()

    payload = {
        'description': caption,
        'access_token': access_token,
        'content_category': 'TECHNOLOGY'
    }
    
    try:
        with open(VIDEO_PATH, 'rb') as v_file:
            files = {'source': (os.path.basename(VIDEO_PATH), v_file, 'video/mp4')}
            print("🚀 [FB] Initializing Viral Upload...")
            response = requests.post(url, data=payload, files=files, timeout=300)
            result = response.json()

            if response.status_code == 200:
                print(f"✅ SUCCESS! FB_ID: {result.get('id')}")
            else:
                log_error(f"API ERROR: {result.get('error', {}).get('message', 'Unknown')}")
    except Exception as e:
        log_error(f"CRITICAL SYSTEM ERROR: {e}")

if __name__ == "__main__":
    upload_to_facebook()
    # 🪄 Crucial: sys.exit(0) tells GitHub "Keep going!" even if FB failed
    sys.exit(0)
