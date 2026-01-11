class TechMageConfig:
    # --- Hugging Face ---
    HUGGING_FACE_API_KEY = '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'
    
    # --- Cloudflare ---
    ACCOUNT_ID = '1009d37ae137647b1e187d25fd12ec3e'
    API_TOKEN = 'xKmsUfMcTNUqvx2Y0xBL_eu1elYiD4IIGOERlxm1'


import os
import base64
import pickle

class TechMageConfig:
    # 1. API Keys - Tells Python to look for GitHub Secrets
    HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
    ACCOUNT_ID = os.getenv('ACCOUNT_ID')
    API_TOKEN = os.getenv('API_TOKEN')
    #FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
    #FB_PAGE_ID = "your_actual_page_id_here" # You can hardcode this

    @staticmethod
    def get_youtube_creds():
        # Look for the Secret String we made earlier
        github_token = os.getenv("PICKLE_TOKEN")
        if github_token:
            return pickle.loads(base64.b64decode(github_token))
        
        # Fallback for your laptop
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as f:
                return pickle.load(f)
        return None