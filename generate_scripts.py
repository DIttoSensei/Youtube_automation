import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
file_name = 'script_output.txt'
hf_token = os.getenv("HUGGING_FACE_API_KEY")

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
You are a professional scriptwriter who writes engaging YouTube Shorts scripts for 'TECH MAGE CHRONICLES'.
Write a 2-minute script split into EXACTLY 10 parts. 

STRICT STYLE RULES:
1. POV: Always write in the FIRST PERSON ('I discovered...', 'I've been testing...').
2. VALUE DENSITY: Do not just narrate; teach. Every segment must provide a 'lightbulb moment'. Squeeze the point in early.
3. HOOKS: The first 3 seconds must be a 'pattern interrupt' hook (e.g., 'Everyone is wrong about...').
4. Always pick a unique, specific niche within Tech, AI, or Computers.

CONSTRAINTS (To avoid errors):
- Each segment must be 30 to 35 words (This is the "sweet spot" for 12 seconds).
- There MUST be exactly 10 segments in the JSON.
- Total video time: 120 seconds.

IMPORTANT OUTPUT FORMAT:

===SCRIPT===
[
  {"start": 0, "end": 12, "text": "First segment of 30-35 words..."},
  {"start": 12, "end": 24, "text": "Second segment of 30-35 words..."},
  ...
  {"start": 108, "end": 120, "text": "Tenth segment of 30-35 words..."}
]

===PROMPTS===
Write exactly 10 cinematic image prompts, one per line, numbered 1 to 10.
"""
        }
    ],
    temperature=0.9
)

with open(file_name, 'w', encoding='utf-8') as f:
    f.write(completion.choices[0].message.content)

print("✅ Tech Mage Script Restored and Saved!")
