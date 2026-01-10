import os
import json
import datetime
import subprocess
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

# ================= CONFIG =================
IMAGES_DIR = "images"
AUDIO_DIR = "audio_segments"
SCRIPT_JSON = "content.json"

# Intermediate and Final file names
RAW_VIDEO = "output/raw_video.mp4"
FINAL_VIDEO = "output/final_video_subtitled.mp4"

FPS = 18 
WIDTH, HEIGHT = 1080, 1920
ZOOM_SPEED = 0.04 
EXPORT_PRESET = "ultrafast"
# ==========================================

os.makedirs("output", exist_ok=True)

def format_srt_time(seconds):
    """Formats seconds into SRT timestamp format: HH:MM:SS,mmm"""
    td = datetime.timedelta(seconds=seconds)
    total_sec = int(td.total_seconds())
    m, s = divmod(total_sec, 60)
    h, m = divmod(m, 60)
    ms = int(td.microseconds / 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def create_srt(script_data, audio_dir, srt_path):
    """Creates an SRT file based on actual audio file durations."""
    current_time = 0.0
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(script_data):
            audio_path = os.path.join(audio_dir, f"segment_{i}.mp3")
            if os.path.exists(audio_path):
                duration = AudioFileClip(audio_path).duration
                start_srt = format_srt_time(current_time)
                end_srt = format_time = format_srt_time(current_time + duration)
                
                f.write(f"{i+1}\n{start_srt} --> {end_srt}\n{seg['text']}\n\n")
                current_time += duration

# 1. Load Data
with open(SCRIPT_JSON, "r", encoding="utf-8") as f:
    script_segments = json.load(f).get("script_segments", [])

images = sorted([
    os.path.join(IMAGES_DIR, f) 
    for f in os.listdir(IMAGES_DIR) 
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
])

# 2. Build Video Clips
clips = []
print(f"🚀 Processing {len(images)} images and syncing audio...")

for i, img_path in enumerate(images):
    audio_path = os.path.join(AUDIO_DIR, f"segment_{i}.mp3")
    
    if os.path.exists(audio_path):
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration 
    else:
        continue 

    # Image processing
    clip = ImageClip(img_path).set_duration(duration)
    clip = clip.resize(height=HEIGHT)
    if clip.w < WIDTH:
        clip = clip.resize(width=WIDTH)
    clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=WIDTH, height=HEIGHT)

    # Fast Ken Burns Zoom
    clip = clip.resize(lambda t: 1 + (ZOOM_SPEED * t / duration))
    clip = clip.crop(x1=0, y1=0, x2=WIDTH, y2=HEIGHT)

    # Attach Audio
    clip = clip.set_audio(audio_clip)
    clips.append(clip)

# 3. Export Raw Video
print(f"\n⚡ Rendering raw video at {FPS} FPS...")
final_raw = concatenate_videoclips(clips, method="chain") 
final_raw.write_videofile(
    RAW_VIDEO, 
    fps=FPS, 
    codec="libx264", 
    preset=EXPORT_PRESET,
    threads=4,
    audio_codec="aac"
)

# 4. Generate SRT and Burn Subtitles
print("\n📜 Generating SRT file...")
create_srt(script_segments, AUDIO_DIR, "subtitles.srt")

print("🎨 Burning Modern Subtitles with FFmpeg...")
# STYLE: Alignment=2 (Bottom Center), BorderStyle=3 (Opaque background box)
# MarginV=140 (Vertical distance from bottom), Fontsize=22
# Modern YouTube Style: Centered, Smaller, Black Outline
# Alignment=10 (Mid-Center), BorderStyle=1 (Outline only), Outline=2 (Thick stroke)

ffmpeg_cmd = [
    'ffmpeg', '-y', '-i', RAW_VIDEO,
    '-vf', (
        "subtitles=subtitles.srt:force_style='"
        "Alignment=10,"      # 10=Center of screen, 2=Bottom center
        "Fontname=Arial,"    # Bold fonts look better for this
        "Fontsize=7,"       # Smaller size as requested
        "PrimaryColour=&H00FFFFFF,"  # White text
        "BorderStyle=1,"     # 1=Outline, 3=Background Box
        "Outline=0,"         # Thickness of the black outline
        "Shadow=0'"          # No drop shadow for a cleaner look
    ),
    '-c:a', 'copy', 
    FINAL_VIDEO
]

subprocess.run(ffmpeg_cmd)

print(f"\n✅ SUCCESS! Your final video is here: {FINAL_VIDEO}")