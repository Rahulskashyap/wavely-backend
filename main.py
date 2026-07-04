from fastapi import FastAPI
from history_service import get_podcast_history
from models import PreferenceUpdate
from news_service import get_global_news
from models import PreferenceUpdate, PodcastGenerateRequest
from fastapi.staticfiles import StaticFiles
import subprocess
import json
import sys
from weather_service import get_weather
import os

from preferences_service import (
    get_user_preferences,
    update_user_preferences
)

PODCAST_DIR = "podcasts"

os.makedirs(PODCAST_DIR, exist_ok=True)

app = FastAPI()

app.mount(
    "/podcasts",
    StaticFiles(directory=PODCAST_DIR),
    name="podcasts"
)

@app.post("/preferences/{user_id}")
def update_preferences(
    user_id: int,
    prefs: PreferenceUpdate
):

    update_user_preferences(
        user_id,
        prefs.country,
        prefs.state,
        prefs.language,
        prefs.voice,
        json.dumps(prefs.categories),
        prefs.duration
    )

    return {
        "message": "Preferences Updated"
    }

@app.get("/history")
def history():

    return {
        "podcasts": get_podcast_history()
    }

@app.get("/api/podcasts/latest")
def latest_podcast():
    history = get_podcast_history()

    if len(history) == 0:
        return {}

    return history[0]


@app.get("/api/podcasts/list")
def podcast_list():

    history = get_podcast_history()

    return history


@app.post("/api/podcasts/generate")
def generate_podcast(request: PodcastGenerateRequest):

    subprocess.run(
        [sys.executable, "generate_daily_podcast.py"],
        check=True
    )

    return {
        "success": True,
        "message": "Podcast generated successfully"
    }

@app.get("/")
def home():
    return {
        "message": "AI News Podcast Backend Running"
    }


@app.get("/news")
def news():
    return get_global_news()


@app.get("/preferences/{user_id}")
def preferences(user_id: int):

    prefs = get_user_preferences(user_id)

    return {
        "country": prefs[0],
        "state": prefs[1],
        "language": prefs[2],
        "voice": prefs[3],
        "categories": json.loads(prefs[4]) if prefs[4] else [],
        "duration": prefs[5]
    }

@app.get("/api/weather")
def weather(city: str = "Bengaluru"):
    try:
        return get_weather(city)
    except Exception as e:
        return {
            "error": str(e)
        }
    
@app.get("/api/highlights")
def get_highlights():
    try:
        with open(
    os.path.join(PODCAST_DIR, "highlights.json"),
    "r",
    encoding="utf-8"
) as f:
            return json.load(f)

    except Exception as e:
        return {
            "highlights": [],
            "error": str(e)
        }

@app.get("/api/transcript/{date}")
def transcript(date: str):

    try:
        with open(
           os.path.join(
    PODCAST_DIR,
    f"{date}.txt"
),
            "r",
            encoding="utf-8"
        ) as f:

            return {
                "transcript": f.read()
            }

    except Exception:
        return {
            "transcript": ""
        }