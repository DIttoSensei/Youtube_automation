import os
from openai import OpenAI

## FILE NAME
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
            "content": "You are a professional scriptwriter who writes engaging YouTube short video scripts."
            "First, choose a highly engaging topic that is trending on YouTube Shorts. Can be related to tech, lifestyle, health, or entertainment."
            "Write a 2-minute video script while using a fast paced engaging tone with clear visual cues."
            "Remember to keep the script short and concise and engaging, suitable for a short video format."
        }
    ],
    temperature=0.9
)

clean_text = completion.choices[0].message.content


# SAVE AND CLEAN
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(clean_text)