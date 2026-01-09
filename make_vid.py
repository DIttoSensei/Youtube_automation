from moviepy.editor import ImageClip, concatenate_videoclips
import os

# ---------------- CONFIG ----------------
IMAGES_DIR = "images"
OUTPUT_VIDEO = "output/video.mp4"
DURATION_PER_IMAGE = 3       # seconds per image
CROSSFADE_DURATION = 0.5     # seconds
FPS = 30
FINAL_WIDTH = 1080
FINAL_HEIGHT = 1920
# ----------------------------------------

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)

# Get images sorted
images = sorted([os.path.join(IMAGES_DIR, f)
                 for f in os.listdir(IMAGES_DIR)
                 if f.endswith((".png", ".jpg", ".jpeg"))])

if not images:
    raise Exception("No images found in the images/ folder!")

clips = []
for img_path in images:
    # Create clip
    clip = ImageClip(img_path).set_duration(DURATION_PER_IMAGE)
    
    # Resize to Shorts vertical while keeping aspect ratio
    clip = clip.resize(height=FINAL_HEIGHT)
    
    # Center crop if width too large
    if clip.w > FINAL_WIDTH:
        clip = clip.crop(x_center=clip.w // 2, width=FINAL_WIDTH)
    
    # Ken Burns effect: slight zoom-in over duration
    # Zoom from 100% → 105%
    clip = clip.resize(lambda t: 1 + 0.05 * (t / DURATION_PER_IMAGE))
    
    clips.append(clip)

# Concatenate clips with crossfade
final_clip = concatenate_videoclips(clips, method="compose", padding=-CROSSFADE_DURATION)

# Export final video
final_clip.write_videofile(
    OUTPUT_VIDEO,
    fps=FPS,
    codec="libx264",
    audio=False,  # later you can add audio
    preset="medium",
    threads=4
)

print("✅ Video created:", OUTPUT_VIDEO)
