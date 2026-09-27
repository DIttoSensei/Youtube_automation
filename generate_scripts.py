import os
from openai import OpenAI
from dotenv import load_dotenv
from prompt import PROMPT

load_dotenv()

file_name = 'script_output.txt'

# Use the token directly from environment variables
hf_token = os.getenv("HUGGING_FACE_API_KEY")

if not hf_token:
    print("❌ Error: HUGGING_FACE_API_KEY not found in environment variables!")
    exit(1)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)

try:
    completion = client.chat.completions.create(
        # FIX: Removed the unsupported ':novita' provider tag
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

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(clean_text)

    print("✅ Script with timestamps generated and saved to", file_name)

except Exception as e:
    print(f"❌ Error during API call: {e}")
    exit(1)
