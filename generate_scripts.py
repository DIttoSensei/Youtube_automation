import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

file_name = 'script_output.txt'
hf_token = os.getenv("HUGGING_FACE_API_KEY")

if not hf_token:
    print("❌ Error: HF_TOKEN not found!")
    exit(1)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token,
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct:novita",
    messages=[
        {
            "role": "system",
            "content": """
You are a professional scriptwriter for 'TECH MAGE CHRONICLES'. 
Write a high-energy script on Tech, AI, or Computers.

STRICT STYLE RULES:
1. POV: Always FIRST PERSON ('I discovered...', 'I've been testing...').
2. VALUE DENSITY: Teach something specific. Every segment needs a 'lightbulb moment'.
3. HOOKS: The first 3 seconds must be a 'pattern interrupt' (e.g., 'Everyone is wrong about...').
4. NICHE: Pick a unique, specific tech niche.
5. LENGTH: 10 segments total.

CONSTRAINTS:
- Each segment must be between 25 and 32 words.
- Each segment is exactly 12 seconds of the timeline.

IMPORTANT OUTPUT FORMAT:

===SCRIPT===
[
  {"start": 0, "end": 12, "text": "25-32 words of engaging narration here..."},
  {"start": 12, "end": 24, "text": "Next 25-32 words of narration here..."},
  ... up to 120 seconds ...
]

===PROMPTS===
1. Cinematic image prompt...
...
10. Cinematic image prompt...
"""
        }
    ],
    temperature=0.9
)

with open(file_name, 'w', encoding='utf-8') as f:
    f.write(completion.choices[0].message.content)

print("✅ Script saved to", file_name)
