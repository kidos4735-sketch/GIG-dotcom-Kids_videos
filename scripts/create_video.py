import subprocess
import os

output_dir = "output"
video_file = os.path.join(output_dir, "final_video.mp4")

images = [
    os.path.join(output_dir, "img_01.png"),
    os.path.join(output_dir, "img_02.png"),
    os.path.join(output_dir, "img_03.png"),
]

audio = os.path.join(output_dir, "voice.wav")

# Safety checks
for f in images + [audio]:
    if not os.path.exists(f):
        raise Exception(f"Missing file: {f}")

# Create FFmpeg input file
list_file = os.path.join(output_dir, "images.txt")
with open(list_file, "w") as f:
    for img in images:
        f.write(f"file '{img}'\n")
        f.write("duration 3\n")

# FFmpeg command
command = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", list_file,
    "-i", audio,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    video_file
]

subprocess.run(command, check=True)

print("🎬 Video created successfully:", video_file)
