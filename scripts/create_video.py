import os
import subprocess
import sys

# =========================
# Paths
# =========================
OUTPUT_DIR = "output"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
IMAGES_TXT = os.path.join(OUTPUT_DIR, "images.txt")
VOICE_FILE = os.path.join(OUTPUT_DIR, "voice.wav")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final_video.mp4")

# =========================
# Prepare directories
# =========================
os.makedirs(IMAGE_DIR, exist_ok=True)

# =========================
# Check voice file
# =========================
if not os.path.exists(VOICE_FILE):
    print("❌ voice.wav not found in output/")
    sys.exit(1)

# =========================
# Create placeholder images if none exist
# =========================
png_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]

if not png_files:
    print("ℹ️ No images found. Creating placeholder images...")
    for i in range(1, 6):
        img_path = os.path.join(IMAGE_DIR, f"img_{i:02d}.png")
        subprocess.run(
    [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=blue:s=1280x720",
        "-vf", "drawtext=text='Scene 1':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2",
        "-frames:v", "1",   # 🔑 THIS LINE FIXES EVERYTHING
        "output/images/img_01.png"
    ],
    check=True
    )

# =========================
# Build images.txt for FFmpeg concat
# =========================
with open(IMAGES_TXT, "w") as f:
    for img in sorted(os.listdir(IMAGE_DIR)):
        if img.endswith(".png"):
            img_path = os.path.join(IMAGE_DIR, img)
            f.write(f"file '{img_path}'\n")
            f.write("duration 3\n")

    # Required by ffmpeg to show last image
    last_image = sorted(os.listdir(IMAGE_DIR))[-1]
    f.write(f"file '{os.path.join(IMAGE_DIR, last_image)}'\n")

# =========================
# Create video
# =========================
command = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", IMAGES_TXT,
    "-i", VOICE_FILE,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    FINAL_VIDEO,
]

print("🎬 Creating video...")
subprocess.run(command, check=True)

print("✅ Video created successfully:")
print(FINAL_VIDEO)
