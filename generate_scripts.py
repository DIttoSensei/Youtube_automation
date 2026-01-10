import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

file_name = 'script_output.txt'

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv('HF_TOKEN'),
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct:novita",
    messages=[
        {
            "role": "system",
            "content": """
You are a professional scriptwriter who writes engaging YouTube Shorts scripts.
Write a 2-minute YouTube Short script using a fast-paced, engaging tone.
Split it into 10 parts. Each part of talking should be **no more than 12 seconds long**.
Each segmeent should no be too short, a single narration should at least have 37 words or more.
Keep it concise and suitable for a short video format.
Talk on only Tech, AI and Computers.
Pick a subject from those topics and write on that.

IMPORTANT OUTPUT FORMAT:

===SCRIPT===
Output JSON array of narration segments with timestamps. Example:

[
  {"start": 0, "end": 12, "text": "First narration segment here"},
  {"start": 12, "end": 24, "text": "Second narration segment here"},
  ...
]

===PROMPTS===
Write exactly 10 cinematic image prompts, one per line, numbered 1 to 10.
Focus on strong visual imagery only. No dialogue, no explanations.
"""
        }
    ],
    temperature=0.9
)

clean_text = completion.choices[0].message.content

with open(file_name, 'w', encoding='utf-8') as f:
    f.write(clean_text)

print("✅ Script with timestamps generated and saved to", file_name)
