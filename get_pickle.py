import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# This must match exactly what you set in Google Cloud Console
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def generate_pickle():
    # 1. Look for your JSON file
    if not os.path.exists("client_secret.json"):
        print("❌ ERROR: I can't find 'client_secrets.json' in this folder!")
        return

    print("🚀 Attempting to open browser for login...")
    
    try:
        # 2. Setup the login flow
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', 
            scopes=SCOPES
        )
        
        # 3. THIS opens the browser. 
        # If it doesn't open, look at your terminal; it might give you a link to copy.
        creds = flow.run_local_server(port=0, authorization_prompt_message="Please visit this URL: {url}")
        
        # 4. Save the "Golden Ticket"
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
            
        print("✅ SUCCESS! 'token.pickle' has been created.")
        print("You can now delete this script and use your main Tech Mage scripts.")

    except Exception as e:
        print(f"❌ CRASHED: {e}")

if __name__ == "__main__":
    generate_pickle()