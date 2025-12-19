import os
import subprocess

OUTPUT_DIR = "output"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
IMAGES_TXT = os.path.join(OUTPUT_DIR, "images.txt")
VOICE_FILE = os.path.join(OUTPUT_DIR, "voice.wav")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final_video.mp4")

os.makedirs(IMAGE_DIR, exist_ok=True)

# 🟢 Create placeholder images if none exist
if not any(f.endswith(".png") for f in os.listdir(IMAGE_DIR)):
    for i in range(1, 6):
        img_path = os.path.join(IMAGE_DIR, f"img_{i:02d}.png")
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "color=c=blue:s=1280x720",
            "-vf", f"drawtext=text='Scene {i}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2",
            img_path
        ], check=True)

# 🟢 Create images.txt
with open(IMAGES_TXT, "w") as f:
    for img in sorted(os.listdir(IMAGE_DIR)):
        if img.endswith(".png"):
            f.write(f"file '{os.path.join(IMAGE_DIR, img)}'\n")
            f.write("duration 3\n")

# 🟢 Build video
command = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", IMAGES_TXT,
    "-i", VOICE_FILE,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    FINAL_VIDEO
]

subprocess.run(command, check=True)

print("✅ Video created:", FINAL_VIDEO)
