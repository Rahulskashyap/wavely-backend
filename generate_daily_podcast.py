
from news_service_v3 import get_all_news
from gemini_service import generate_podcast_script
from audio_service import generate_podcast_audio
from preferences_service import get_user_preferences
from highlights_service import generate_highlights
import json

from datetime import datetime
import subprocess

# -----------------------------
# Get user preferences
# -----------------------------
prefs = get_user_preferences(1)

country = prefs[0]
state = prefs[1]
language = prefs[2]
voice = prefs[3]
news_mode = prefs[4]
podcast_length = prefs[5]

print("Country :", country)
print("State :", state)
print("Language :", language)
print("Voice :", voice)
print("News Mode :", news_mode)
print("Duration :", podcast_length)

# -----------------------------
# File names
# -----------------------------
today = datetime.now().strftime("%Y-%m-%d")

script_file = "daily_script.txt"

raw_audio = f"../podcasts/{today}.mp3"

final_audio = f"../podcasts/{today}_final.mp3"

# -----------------------------
# Fetch news
# -----------------------------
print("Fetching news...")
print("Country =", country)
print("State =", state)

news = get_all_news(
    country,
    state
)

# -----------------------------
# Generate script
# -----------------------------
print("Generating script...")
if news_mode == "National":

    all_news = f"""

NATIONAL NEWS:
{news['india']}

BUSINESS NEWS:
{news['economy']}

TECHNOLOGY NEWS:
{news['technology']}

SPORTS NEWS:
{news['sports']}

ENTERTAINMENT NEWS:
{news['entertainment']}

"""

elif news_mode == "Global":

    all_news = f"""

WORLD NEWS:
{news['world']}

BUSINESS NEWS:
{news['economy']}

TECHNOLOGY NEWS:
{news['technology']}

SPORTS NEWS:
{news['sports']}

ENTERTAINMENT NEWS:
{news['entertainment']}

"""

else:

    all_news = f"""

STATE NEWS:
{news['state']}

NATIONAL NEWS:
{news['india']}

WORLD NEWS:
{news['world']}

BUSINESS NEWS:
{news['economy']}

TECHNOLOGY NEWS:
{news['technology']}

SPORTS NEWS:
{news['sports']}

ENTERTAINMENT NEWS:
{news['entertainment']}

"""

script = generate_podcast_script(
    all_news,
    podcast_length
)
print("Generating AI Highlights...")

highlights = generate_highlights(script)

with open("../podcasts/highlights.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "highlights": highlights
        },
        f,
        ensure_ascii=False,
        indent=4,
    )

print("Highlights saved.")
# -----------------------------
# Clean script before TTS
# -----------------------------
script = script.replace("[PAUSE]", "\n\n")
script = script.replace('"[PAUSE]"', "")
script = script.replace("PAUSE", "")

script = script.replace("*", "")
script = script.replace("#", "")
script = script.replace("•", "")

# -----------------------------
# Save script
# -----------------------------
with open(script_file, "w", encoding="utf-8") as f:
    f.write(script)

# Save transcript with today's podcast
with open(f"../podcasts/{today}.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("Script saved")

# -----------------------------
# Generate audio
# -----------------------------
print("Generating audio...")

generate_podcast_audio(
    text=script,
    language=language,
    voice=voice,
    output_file=raw_audio,
)

print("Audio generated")

# -----------------------------
# Add intro + outro
# -----------------------------
print("Adding intro/outro...")

command = [
    r"C:\ffmpeg\ffmpeg-2026-06-04-git-c27a3b12e3-essentials_build\bin\ffmpeg.exe",
    "-i", "assets/intro.mp3",
    "-i", raw_audio,
    "-i", "assets/intro.mp3",
    "-filter_complex",
    "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]",
    "-map",
    "[out]",
    final_audio,
    "-y"
]

subprocess.run(command)

print()
print("SUCCESS")
print("Podcast saved at:")
print(final_audio)
