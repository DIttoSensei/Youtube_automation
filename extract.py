import json

INPUT_FILE = "script_output.txt"
CONTENT_JSON = "content.json"
PROMPTS_JSON = "prompts.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Split sections
script_part = text.split("===SCRIPT===")[1].split("===PROMPTS===")[0].strip()
prompts_part = text.split("===PROMPTS===")[1].strip()

# Clean prompts
prompts = []
for line in prompts_part.splitlines():
    line = line.strip()
    if not line:
        continue
    if line[0].isdigit():
        prompts.append(line.split(".", 1)[1].strip())

# Save narration
with open(CONTENT_JSON, "w", encoding="utf-8") as f:
    json.dump(
        {"script": script_part},
        f,
        indent=2,
        ensure_ascii=False
    )

# Save prompts
with open(PROMPTS_JSON, "w", encoding="utf-8") as f:
    json.dump(
        {"prompts": prompts[:7]},  # hard cap at 7
        f,
        indent=2,
        ensure_ascii=False
    )

print("✅ Extraction complete")
print(f"Script length: {len(script_part.split())} words")
print(f"Image prompts: {len(prompts[:7])}")
