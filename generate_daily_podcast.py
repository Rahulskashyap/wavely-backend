import os
import json
import subprocess

from datetime import datetime

from news_service_v3 import get_all_news
from gemini_service import generate_podcast_script
from audio_service import generate_podcast_audio
from preferences_service import get_user_preferences
from highlights_service import generate_highlights


# -----------------------------------
# PODCAST DIRECTORY
# -----------------------------------

PODCAST_DIR = "podcasts"

os.makedirs(PODCAST_DIR, exist_ok=True)


# -----------------------------------
# GET USER PREFERENCES
# -----------------------------------

prefs = get_user_preferences(1)

country = prefs[0]
state = prefs[1]
language = prefs[2]
voice = prefs[3]
news_mode = prefs[4]
try:
    selected_categories = json.loads(news_mode)
except Exception:
    selected_categories = []
podcast_length = prefs[5]

print("Country :", country)
print("State :", state)
print("Language :", language)
print("Voice :", voice)
print("News Mode :", news_mode)
print("Duration :", podcast_length)


# -----------------------------------
# FILE NAMES
# -----------------------------------

today = datetime.now().strftime("%Y-%m-%d")

script_file = "daily_script.txt"

raw_audio = os.path.join(
    PODCAST_DIR,
    f"{today}.mp3"
)

final_audio = os.path.join(
    PODCAST_DIR,
    f"{today}_final.mp3"
)

transcript_file = os.path.join(
    PODCAST_DIR,
    f"{today}.txt"
)

highlights_file = os.path.join(
    PODCAST_DIR,
    "highlights.json"
)


# -----------------------------------
# FETCH NEWS
# -----------------------------------

print("Fetching news...")
print("Country =", country)
print("State =", state)

news = get_all_news(
    country,
    state
)


# -----------------------------------
# GENERATE SCRIPT
# -----------------------------------

print("Generating script...")

news_sections = []


# -----------------------------------
# KARNATAKA / STATE NEWS FIRST
# -----------------------------------

if "State" in selected_categories:

    news_sections.append(f"""
KARNATAKA STATE NEWS - HIGHEST PRIORITY:

{news['state']}
""")


# -----------------------------------
# INDIA NATIONAL NEWS
# -----------------------------------

if "National" in selected_categories:

    news_sections.append(f"""
IMPORTANT INDIA NATIONAL NEWS:

{news['india']}
""")


# -----------------------------------
# BUSINESS AND ECONOMY
# -----------------------------------

if "Business" in selected_categories:

    news_sections.append(f"""
INDIA BUSINESS AND ECONOMY NEWS:

{news['economy']}
""")


# -----------------------------------
# TECHNOLOGY
# -----------------------------------

if "Technology" in selected_categories:

    news_sections.append(f"""
INDIA TECHNOLOGY AND AI NEWS:

{news['technology']}
""")


# -----------------------------------
# SPORTS
# -----------------------------------

if "Sports" in selected_categories:

    news_sections.append(f"""
INDIA SPORTS NEWS:

Give highest priority to cricket and major Indian sporting events.

{news['sports']}
""")


# -----------------------------------
# ENTERTAINMENT
# -----------------------------------

if "Entertainment" in selected_categories:

    news_sections.append(f"""
INDIA ENTERTAINMENT NEWS:

{news['entertainment']}
""")


# -----------------------------------
# HEALTH
# -----------------------------------

if "Health" in selected_categories:

    health_news = news.get("health", "")

    if health_news:

        news_sections.append(f"""
IMPORTANT HEALTH NEWS:

{health_news}
""")


# -----------------------------------
# WORLD NEWS LAST
# -----------------------------------

if "World" in selected_categories:

    news_sections.append(f"""
IMPORTANT WORLD NEWS:

Include only major international developments that are relevant or important.

{news['world']}
""")


all_news = "\n\n".join(news_sections)
if not all_news.strip():
    all_news = f"""
STATE NEWS:
{news.get('state', '')}

NATIONAL NEWS:
{news.get('india', '')}

IMPORTANT WORLD NEWS:
{news.get('world', '')}
"""

# -----------------------------------
# GENERATE PODCAST SCRIPT
# -----------------------------------

print("Generating podcast script with Gemini...")

script = generate_podcast_script(
    all_news,
    podcast_length
)

print("Podcast script generated.")


# -----------------------------------
# GENERATE HIGHLIGHTS
# -----------------------------------

print("Generating AI Highlights...")

try:

    highlights = generate_highlights(script)

except Exception as e:

    print(f"Highlights generation failed: {e}")

    highlights = []


with open(
    highlights_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        {
            "highlights": highlights
        },
        f,
        ensure_ascii=False,
        indent=4,
    )


print("Highlights saved.")


# -----------------------------------
# CLEAN SCRIPT
# -----------------------------------

script = script.replace("[PAUSE]", "\n\n")
script = script.replace('"[PAUSE]"', "")
script = script.replace("PAUSE", "")

script = script.replace("*", "")
script = script.replace("#", "")
script = script.replace("•", "")


# -----------------------------------
# SAVE SCRIPT
# -----------------------------------

with open(
    script_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(script)


with open(
    transcript_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(script)


print("Script saved")


# -----------------------------------
# GENERATE AUDIO
# -----------------------------------

print("Generating audio...")


generate_podcast_audio(
    text=script,
    language=language,
    voice=voice,
    output_file=raw_audio,
)


print("Audio generated")


# -----------------------------------
# ADD INTRO / OUTRO
# -----------------------------------

print("Adding intro/outro...")


command = [

    "ffmpeg",

    "-i",
    "assets/intro.mp3",

    "-i",
    raw_audio,

    "-i",
    "assets/intro.mp3",

    "-filter_complex",
    "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]",

    "-map",
    "[out]",

    final_audio,

    "-y"
]


try:

    subprocess.run(
        command,
        check=True
    )

    print("Intro/outro added successfully.")

except Exception as e:

    print(f"FFmpeg failed: {e}")

    print("Using raw audio instead.")

    final_audio = raw_audio


print()
print("SUCCESS")
print("Podcast saved at:")
print(final_audio)