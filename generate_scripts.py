import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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
            "content": """
                        You are a professional scriptwriter who writes engaging YouTube Shorts scripts.
                        Write a 2-minute YouTube Short script using a fast-paced, engaging tone.
                        Keep it concise and suitable for short video format.
                        Choose from a variety of topics like, tech, science, lifestyle, and entertainment but one per script.
                        Don't talk about 2 or more topics in one script.
            

                        IMPORTANT OUTPUT FORMAT:
                        You MUST output the text in the following structure exactly.

                        ===SCRIPT===
                        (Write only the narration here. No scene numbers or decriptions on what the host is doing, just narration.)

                        ===PROMPTS===
                        Write exactly 7 cinematic image prompts.
                        Each prompt must describe a different visual moment.
                        No dialogue. No explanations.
                        One prompt per line, numbered 1 to 7.
                        Focus on strong visual imagery only.
                    """
        }
    ],
    temperature=0.9
)

clean_text = completion.choices[0].message.content


# SAVE AND CLEAN
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(clean_text)