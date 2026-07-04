import subprocess
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

intro_file = "assets/intro.mp3"
podcast_file = f"../podcasts/{today}.mp3"
output_file = f"../podcasts/{today}_final.mp3"

command = [
    r"C:\ffmpeg\ffmpeg-2026-06-04-git-c27a3b12e3-essentials_build\bin\ffmpeg.exe",
    "-i", intro_file,
    "-i", podcast_file,
    "-i", intro_file,
    "-filter_complex",
    "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]",
    "-map", "[out]",
    output_file,
    "-y"
]

subprocess.run(command)

print("Final podcast created!")