import os
import json
from generate_daily_podcast import generate_podcast_for_user
from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles

from models import PreferenceUpdate
from news_service import get_global_news
from weather_service import get_weather

from firebase_service import verify_firebase_token

from preferences_service import (
    get_user_preferences,
    update_user_preferences,
)

from history_service import (
    get_podcast_history,
    get_latest_podcast,
    get_podcast_details,
)


# -----------------------------------
# APP SETUP
# -----------------------------------

PODCAST_DIR = "podcasts"

os.makedirs(PODCAST_DIR, exist_ok=True)

app = FastAPI()

app.mount(
    "/podcasts",
    StaticFiles(directory=PODCAST_DIR),
    name="podcasts",
)


# -----------------------------------
# FIREBASE AUTHENTICATION
# -----------------------------------

def get_current_user_uid(
    authorization: str = Header(None)
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    token = authorization.replace(
        "Bearer ",
        "",
        1,
    )

    try:
        decoded_token = verify_firebase_token(token)

        return decoded_token["uid"]

    except Exception as e:

        print("Firebase authentication error:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid Firebase token",
        )


# -----------------------------------
# HOME
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "Wavely Backend Running"
    }


# -----------------------------------
# GET PREFERENCES
# -----------------------------------

@app.get("/preferences")
def preferences(
    authorization: str = Header(None)
):

    uid = get_current_user_uid(authorization)

    prefs = get_user_preferences(uid)

    return prefs


# -----------------------------------
# UPDATE PREFERENCES
# -----------------------------------

@app.post("/preferences")
def update_preferences(
    prefs: PreferenceUpdate,
    authorization: str = Header(None),
):

    uid = get_current_user_uid(authorization)

    updated_preferences = update_user_preferences(
        uid,
        prefs.country,
        prefs.state,
        prefs.language,
        prefs.voice,
        prefs.categories,
        prefs.duration,
    )

    return {
        "success": True,
        "message": "Preferences Updated",
        "preferences": updated_preferences,
    }

@app.post("/api/podcasts/generate")
def generate_podcast(
    authorization: str = Header(None),
):

    uid = get_current_user_uid(
        authorization
    )

    try:

        podcast = generate_podcast_for_user(
            uid
        )

        return {
            "success": True,
            "status": "completed",
            "message": "Podcast generated successfully",
            "podcast": podcast,
        }

    except Exception as e:

        print(
            "Podcast generation error:",
            e,
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
# -----------------------------------
# WEATHER
# -----------------------------------

@app.get("/api/weather")
def weather(city: str = "Bengaluru"):

    try:

        return get_weather(city)

    except Exception as e:

        print("Weather error:", e)

        raise HTTPException(
            status_code=500,
            detail="Weather service failed",
        )


# -----------------------------------
# NEWS
# -----------------------------------

@app.get("/news")
def news():

    return get_global_news()


# -----------------------------------
# PODCAST HISTORY
# TEMPORARY LOCAL VERSION
# -----------------------------------

@app.get("/history")
def history(
    authorization: str = Header(None),
):

    uid = get_current_user_uid(authorization)

    return {
        "podcasts": get_podcast_history(uid)
    }


@app.get("/api/podcasts/latest")
def latest_podcast(
    authorization: str = Header(None),
):

    uid = get_current_user_uid(authorization)

    podcast = get_latest_podcast(uid)

    if podcast is None:
        raise HTTPException(
            status_code=404,
            detail="No podcast found",
        )

    return podcast


@app.get("/api/podcasts/list")
def podcast_list(
    authorization: str = Header(None),
):

    uid = get_current_user_uid(authorization)

    return get_podcast_history(uid)


# -----------------------------------
# HIGHLIGHTS
# TEMPORARY LOCAL VERSION
# -----------------------------------

@app.get("/api/highlights")
def get_highlights(
    authorization: str = Header(None),
):

    uid = get_current_user_uid(authorization)

    podcast = get_latest_podcast(uid)

    if podcast is None:
        return {
            "highlights": []
        }

    details = get_podcast_details(
        uid,
        podcast["date"],
    )

    return {
        "highlights": details.get(
            "highlights",
            [],
        )
    }

# -----------------------------------
# TRANSCRIPT
# TEMPORARY LOCAL VERSION
# -----------------------------------

@app.get("/api/transcript/{date}")
def transcript(
    date: str,
    authorization: str = Header(None),
):

    uid = get_current_user_uid(authorization)

    details = get_podcast_details(
        uid,
        date,
    )

    if details is None:
        return {
            "transcript": ""
        }

    return {
        "transcript": details.get(
            "transcript",
            "",
        )
    }