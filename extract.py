import json

INPUT_FILE = "script_output.txt"
CONTENT_JSON = "content.json"
PROMPTS_JSON = "prompts.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Split sections
try:
    script_text = text.split("===SCRIPT===")[1].split("===PROMPTS===")[0].strip()
    prompts_text = text.split("===PROMPTS===")[1].strip()
except IndexError:
    raise RuntimeError("❌ Could not find ===SCRIPT=== or ===PROMPTS=== in file")

# ----------- SCRIPT SEGMENTS -----------
# Try to parse AI JSON from script section
try:
    script_segments = json.loads(script_text)
    if not isinstance(script_segments, list):
        raise ValueError
except (json.JSONDecodeError, ValueError):
    # Fallback: plain text → assign 12s per line
    lines = [line.strip() for line in script_text.split("\n") if line.strip()]
    script_segments = []
    for i, line in enumerate(lines):
        segment = {
            "start": i * 12,
            "end": (i + 1) * 12,
            "text": line
        }
        script_segments.append(segment)

# Save script
with open(CONTENT_JSON, "w", encoding="utf-8") as f:
    json.dump({"script_segments": script_segments}, f, indent=2, ensure_ascii=False)

# ----------- PROMPTS -----------
prompts = []
for line in prompts_text.splitlines():
    line = line.strip()
    if not line:
        continue
    # Remove numbering if present
    if line[0].isdigit() and "." in line:
        line = line.split(".", 1)[1].strip()
    prompts.append(line)

# Keep all 10 prompts
prompts = prompts[:10]

# Save prompts
with open(PROMPTS_JSON, "w", encoding="utf-8") as f:
    json.dump({"prompts": prompts}, f, indent=2, ensure_ascii=False)

print("✅ Extraction complete")
print(f"Segments: {len(script_segments)}")
print(f"Prompts: {len(prompts)}")
