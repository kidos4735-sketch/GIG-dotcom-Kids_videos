import subprocess
import os

os.makedirs("output", exist_ok=True)

command = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", "output/images.txt",
    "-i", "output/voice.wav",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    "output/final_video.mp4"
]

subprocess.run(command, check=True)

print("🎬 Video created: output/final_video.mp4")
