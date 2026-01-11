import os
import pickle
import base64
import re
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube Setup
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_PATH = "output/final_video_subtitled.mp4"
SCRIPT_FILE = "script_output.txt"

def get_viral_metadata():
    """Generates consistent title and description based on the Facebook style."""
    
    # 1. Dynamic Hook Extraction (Matching FB)
    dynamic_hook = "Breaking down the future of technology."
    try:
        if os.path.exists(SCRIPT_FILE):
            with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                texts = re.findall(r'"text":\s*"(.*?)"', content)
                if texts:
                    words = texts[0].split()
                    dynamic_hook = " ".join(words[:8]) + "..."
    except Exception as e:
        print(f"⚠️ Could not parse hook: {e}")

    # 2. Optimized Title (YouTube Shorts titles must be short)
    # Adding #Shorts in the title is crucial for the algorithm
    title = f"🧙‍♂️ {dynamic_hook[:50]} #Shorts #TechMage"

    # 3. Viral Description (The exact same FB structure)
    description = f"""🧙‍♂️ TECH MAGE CHRONICLES
THE AI REVOLUTION IS HERE. ARE YOU READY? 💻🚀

{dynamic_hook}

I'm deep-diving into the tech that actually matters. Don't get left behind. ⚡

#TechMage #AI #FutureTech #Programming #ComputerScience #Innovation #CodingLife #ViralTech #ShortsFeed #Trending"""

    return title, description

def get_authenticated_service():
    pickle_data = os.getenv("PICKLE_TOKEN")
    if pickle_data:
        credentials = pickle.loads(base64.b64decode(pickle_data))
    elif os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    else:
        raise Exception("❌ No credentials found!")
    return build("youtube", "v3", credentials=credentials)

def upload():
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: Video not found at {VIDEO_PATH}")
        return

    youtube = get_authenticated_service()
    title, description = get_viral_metadata()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["AI", "Tech", "Shorts", "Trending", "Coding", "TechMage"],
            "categoryId": "28" # Technology
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"🚀 Uploading Shorts to YouTube: {title}")
    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(VIDEO_PATH, chunksize=-1, resumable=True)
    )
    
    response = insert_request.execute()
    print(f"✅ DONE! Video ID: {response['id']}")
    print(f"Check it here: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    upload()