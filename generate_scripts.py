import os
from openai import OpenAI
from dotenv import load_dotenv
from prompt import PROMPT


load_dotenv()

file_name = 'script_output.txt'

# Use the HF_TOKEN directly from environment variables
hf_token = os.getenv("HUGGING_FACE_API_KEY")

if not hf_token:
    print("❌ Error: HF_TOKEN not found in environment variables!")
    exit(1)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token, # Passing it here satisfies the library's check
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct:novita",
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
