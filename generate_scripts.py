import os
from openai import OpenAI
from dotenv import load_dotenv

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
            "content": """
You are a professional scriptwriter who writes engaging YouTube Shorts scripts.
Write a 2-minute YouTube Short script using a fast-paced, engaging tone.
Split it into 10 parts. Each part of talking should be **no more than 12 seconds long**.
Each segmeent should no be too short, a single narration should at least have 37 words or more.
Keep it concise and suitable for a short video format.
Talk on only Tech, computer architecture, computer hardware, computer software, ai.
Pick a subject from those topics and write on that and make sure it something they might not know so they can learn.

STRICT STYLE RULES:
1. POV: Always write in the FIRST PERSON ('I discovered...', 'I've been testing...', 'My favorite tech...').
2. VALUE DENSITY: Do not just narrate; teach. Every segment must provide a 'lightbulb moment' or a specific piece of information. Squeeze the point in early.
3. HOOKS: The first 3 seconds must be a 'pattern interrupt' hook (e.g., 'Everyone is wrong about...', 'I found the hidden setting for...').
4. Always pick a unique, specific niche within Tech/AI so every video is different.
5. Just as prompt is 10 segments should also match that.
6. Scripts segment should be 10 or in other words 10 narrations only, 

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
