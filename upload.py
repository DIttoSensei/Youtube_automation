import os
import pickle
import base64
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube Setup
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_PATH = "output/final_video_subtitled.mp4"

def get_authenticated_service():
    # Looks for the secret on GitHub
    pickle_data = os.getenv("PICKLE_TOKEN")
    
    if pickle_data:
        print("🔑 Using PICKLE_TOKEN from GitHub Secrets")
        credentials = pickle.loads(base64.b64decode(pickle_data))
    elif os.path.exists("token.pickle"):
        print("🔑 Using local token.pickle file")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    else:
        raise Exception("❌ No credentials found! Need token.pickle or GitHub Secret.")

    return build("youtube", "v3", credentials=credentials)

def upload():
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: Could not find video at {VIDEO_PATH}")
        return

    youtube = get_authenticated_service()

    # Optimized Title and Trending Hashtags for Shorts
    body = {
        "snippet": {
            "title": "Unbelievable Tech Magic! #Shorts #TechMage",
            "description": "Witness the power of AI and Tech. #AI #FutureTech #Programming #Coding #Trending #Viral #ShortsFeed",
            "tags": ["AI", "Tech", "Shorts", "Trending", "Coding"],
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"🚀 Uploading Shorts to YouTube...")
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