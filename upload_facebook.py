import os
import requests
import json
import re
import sys

# ================= CONFIG =================
VIDEO_PATH = "output/final_video_subtitled.mp4"
SCRIPT_FILE = "script_output.txt"
# ==========================================
ai_disclosure = (
    "ℹ️ This video includes AI-generated narration and/or visuals."
)

def get_viral_caption():
    """Constructs a high-engagement caption with a fixed viral structure."""
    
    # 1. Fixed Viral Branding & Headline
    header = "🧙‍♂️ TECH MAGE CHRONICLES"
    headline = "THE AI REVOLUTION IS HERE. ARE YOU READY? 💻🚀"

    # 2. Dynamic Hook Extraction (Cleaned)
    dynamic_hook = "Breaking down the future of technology."
    try:
        if os.path.exists(SCRIPT_FILE):
            with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                # Find the first "text" value in the JSON script
                texts = re.findall(r'"text":\s*"(.*?)"', content)
                if texts:
                    # Take first 8 words to keep it punchy
                    words = texts[0].split()
                    dynamic_hook = " ".join(words[:8]) + "..."
    except Exception as e:
        print(f"⚠️ Could not parse hook: {e}")

    # 3. The "Viral Loop" Body & Hashtags (The Exact Format You Requested)
    caption = f"""{header}
{headline}

{dynamic_hook}

I'm deep-diving into the tech that actually matters. Don't get left behind in the analog age. ⚡

What's inside:
🔥 Future-Proof AI Insights
🔥 Expert Tech Breakdown
🔥 No-Fluff Innovation


{ai_disclosure}

#TechMage #AI #ArtificialIntelligence #FutureTech #Programming #ComputerScience #TechNews #Innovation #Software #CodingLife #ViralTech #TechTrends2026"""
    
    return caption

def upload_to_facebook():
    """Uploads the video using the Facebook Graph API."""
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    
    # Validation
    if not page_id or not access_token:
        print("❌ ERROR: Facebook Credentials (FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN) not found!")
        sys.exit(1) # Stops main.py

    if not os.path.exists(VIDEO_PATH):
        print(f"❌ ERROR: Video file not found at {VIDEO_PATH}")
        sys.exit(1) # Stops main.py

    caption = get_viral_caption()

    # Facebook Graph API Video Endpoint
    url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"
    
    # Multi-part form data
    payload = {
        'description': caption,
        'access_token': access_token,
        'content_category': 'TECHNOLOGY' 
    }
    
    try:
        files = {
            'source': (os.path.basename(VIDEO_PATH), open(VIDEO_PATH, 'rb'), 'video/mp4')
        }

        print("🚀 [FB] Initializing Viral Upload...")
        response = requests.post(url, data=payload, files=files)
        result = response.json()

        if response.status_code == 200:
            print(f"✅ SUCCESS! Video is live. FB_ID: {result.get('id')}")
            # Successful finish (Exit Code 0)
        else:
            print(f"❌ FACEBOOK API ERROR: {result.get('error', {}).get('message', 'Unknown Error')}")
            print(f"Full Response: {json.dumps(result, indent=2)}")
            sys.exit(1) # FAILURE: Stops main.py from going to YouTube
            
    except Exception as e:
        print(f"❌ CRITICAL UPLOAD ERROR: {e}")
        sys.exit(1) # FAILURE: Stops main.py

if __name__ == "__main__":
    upload_to_facebook()