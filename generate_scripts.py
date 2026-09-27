import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from prompt import PROMPT

load_dotenv()

file_name = 'script_output.txt'

# Verify API key availability
hf_token = os.getenv("HUGGING_FACE_API_KEY")

if not hf_token:
    print("❌ Error: HUGGING_FACE_API_KEY environment variable is not set!")
    sys.exit(1)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)

try:
    print("🚀 Sending request to Hugging Face router...")
    
    completion = client.chat.completions.create(
        # Updated model route without the invalid ':novita' provider suffix
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {
                "role": "system",
                "content": PROMPT
            }
        ],
        temperature=0.9
    )

    clean_text = completion.choices[0].message.content

    if not clean_text or not clean_text.strip():
        print("❌ Error: Received empty output from the model.")
        sys.exit(1)

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(clean_text)

    print("✅ Script with timestamps successfully saved to", file_name)

except Exception as e:
    # Print exact exception so orchestrator logs capture the failure
    print(f"❌ Unhandled API Exception during script generation: {e}", file=sys.stderr)
    sys.exit(1)
