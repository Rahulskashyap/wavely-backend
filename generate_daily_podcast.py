import os
import json
import subprocess
import imageio_ffmpeg
from storage_service import upload_podcast_audio
from datetime import datetime
from zoneinfo import ZoneInfo

from news_service_v3 import get_all_news
from gemini_service import generate_podcast_script
from audio_service import generate_podcast_audio
from preferences_service import get_user_preferences
from highlights_service import generate_highlights
from firebase_service import db

IST = ZoneInfo("Asia/Kolkata")
# ============================================================
# CONFIGURATION
# ============================================================

PODCAST_DIR = "podcasts"

os.makedirs(PODCAST_DIR, exist_ok=True)


# ============================================================
# GENERATE PODCAST FOR ONE FIREBASE USER
# ============================================================

def generate_podcast_for_user(uid):

    print()
    print("=" * 60)
    print("GENERATING PODCAST")
    print("USER:", uid)
    print("=" * 60)

    # ========================================================
    # GET USER PREFERENCES FROM FIRESTORE
    # ========================================================

    prefs = get_user_preferences(uid)

    country = prefs.get(
        "country",
        "India",
    )

    state = prefs.get(
        "state",
        "Karnataka",
    )

    language = prefs.get(
        "language",
        "English",
    )

    voice = prefs.get(
        "voice",
        "Male",
    )

    selected_categories = prefs.get(
        "categories",
        ["Technology"],
    )

    podcast_length = prefs.get(
        "duration",
        20,
    )

    if not isinstance(selected_categories, list):
        selected_categories = []

    print()
    print("USER PREFERENCES")
    print("-------------------------")
    print("Country:", country)
    print("State:", state)
    print("Language:", language)
    print("Voice:", voice)
    print("Categories:", selected_categories)
    print("Duration:", podcast_length)

    # ========================================================
    # CREATE UNIQUE USER PODCAST DIRECTORY
    # ========================================================

    user_podcast_dir = os.path.join(
        PODCAST_DIR,
        uid,
    )

    os.makedirs(
        user_podcast_dir,
        exist_ok=True,
    )

    # ========================================================
    # FILE NAMES
    # ========================================================

    today = datetime.now(IST).strftime(
    "%Y-%m-%d"
)

    raw_audio = os.path.join(
        user_podcast_dir,
        f"{today}.mp3",
    )

    final_audio = os.path.join(
        user_podcast_dir,
        f"{today}_final.mp3",
    )

    transcript_file = os.path.join(
        user_podcast_dir,
        f"{today}.txt",
    )

    highlights_file = os.path.join(
        user_podcast_dir,
        f"{today}_highlights.json",
    )

    # ========================================================
    # FIRESTORE PODCAST DOCUMENT
    # ========================================================

    episode_ref = (
        db
        .collection("users")
        .document(uid)
        .collection("podcasts")
        .document(today)
    )

    # ========================================================
    # INITIAL GENERATION STATUS
    # ========================================================

    episode_ref.set(
        {
            "date": today,
            "title": "Morning Brief",
            "status": "starting",
            "country": country,
            "state": state,
            "language": language,
            "voice": voice,
            "duration": podcast_length,
            "categories": selected_categories,
           "created_at": datetime.now(IST),
        },
        merge=True,
    )

    try:

        # ====================================================
        # FETCH NEWS
        # ====================================================

        print()
        print("Fetching news...")

        episode_ref.update(
            {
                "status": "fetching_news"
            }
        )

        news = get_all_news(
            country,
            state,
        )

        print("News fetched successfully.")

        # ====================================================
        # BUILD NEWS SECTIONS
        # ====================================================

        news_sections = []

        # ----------------------------------------------------
        # STATE NEWS
        # ----------------------------------------------------

        if "State" in selected_categories:

            news_sections.append(
                f"""
STATE NEWS FROM {state.upper()} - HIGHEST PRIORITY:

{news.get("state", "")}
"""
            )

        # ----------------------------------------------------
        # NATIONAL NEWS
        # ----------------------------------------------------

        if "National" in selected_categories:

            news_sections.append(
                f"""
IMPORTANT {country.upper()} NATIONAL NEWS:

{news.get("india", "")}
"""
            )

        # ----------------------------------------------------
        # BUSINESS
        # ----------------------------------------------------

        if "Business" in selected_categories:

            news_sections.append(
                f"""
INDIA BUSINESS AND ECONOMY NEWS:

{news.get("economy", "")}
"""
            )

        # ----------------------------------------------------
        # TECHNOLOGY
        # ----------------------------------------------------

        if "Technology" in selected_categories:

            news_sections.append(
                f"""
INDIA TECHNOLOGY AND AI NEWS:

{news.get("technology", "")}
"""
            )

        # ----------------------------------------------------
        # SPORTS
        # ----------------------------------------------------

        if "Sports" in selected_categories:

            news_sections.append(
                f"""
INDIA SPORTS NEWS:

Give highest priority to cricket and major Indian sporting events.

{news.get("sports", "")}
"""
            )

        # ----------------------------------------------------
        # ENTERTAINMENT
        # ----------------------------------------------------

        if "Entertainment" in selected_categories:

            news_sections.append(
                f"""
INDIA ENTERTAINMENT NEWS:

{news.get("entertainment", "")}
"""
            )

        # ----------------------------------------------------
        # HEALTH
        # ----------------------------------------------------

        if "Health" in selected_categories:

            health_news = news.get(
                "health",
                "",
            )

            if health_news:

                news_sections.append(
                    f"""
IMPORTANT HEALTH NEWS:

{health_news}
"""
                )

        # ----------------------------------------------------
        # WORLD NEWS
        # ----------------------------------------------------

        if "World" in selected_categories:

            news_sections.append(
                f"""
IMPORTANT WORLD NEWS:

Include only major international developments that are important or relevant.

{news.get("world", "")}
"""
            )

        # ====================================================
        # FALLBACK IF NO CATEGORIES ARE SELECTED
        # ====================================================

        if not news_sections:

            print(
                "No categories selected. "
                "Using default State, National and World news."
            )

            news_sections.append(
                f"""
STATE NEWS FROM {state.upper()}:

{news.get("state", "")}

IMPORTANT {country.upper()} NATIONAL NEWS:

{news.get("india", "")}

IMPORTANT WORLD NEWS:

{news.get("world", "")}
"""
            )

        # ====================================================
        # COMBINE NEWS
        # ====================================================

        all_news = "\n\n".join(
            news_sections
        )

        # ====================================================
        # GENERATE PODCAST SCRIPT
        # ====================================================

        print()
        print("Generating podcast script...")

        episode_ref.update(
            {
                "status": "generating_script"
            }
        )

        script = generate_podcast_script(
            all_news,
            podcast_length,
            language,
        )

        if not script or not script.strip():

            raise RuntimeError(
                "Gemini returned an empty podcast script."
            )

        print("Podcast script generated.")

        # ====================================================
        # GENERATE AI HIGHLIGHTS
        # ====================================================

        print()
        print("Generating AI highlights...")

        episode_ref.update(
            {
                "status": "generating_highlights"
            }
        )

        try:

            highlights = generate_highlights(
                script
            )

            if not isinstance(
                highlights,
                list,
            ):
                highlights = []

        except Exception as e:

            print(
                "Highlights generation failed:",
                e,
            )

            highlights = []

        # ====================================================
        # SAVE HIGHLIGHTS
        # ====================================================

        with open(
            highlights_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                {
                    "highlights": highlights
                },
                file,
                ensure_ascii=False,
                indent=4,
            )

        print("Highlights saved.")

        # ====================================================
        # CLEAN SCRIPT FOR TTS
        # ====================================================

        clean_script = script

        clean_script = clean_script.replace(
            '"[PAUSE]"',
            "",
        )

        clean_script = clean_script.replace(
            "[PAUSE]",
            "\n\n",
        )

        clean_script = clean_script.replace(
            "PAUSE",
            "",
        )

        clean_script = clean_script.replace(
            "*",
            "",
        )

        clean_script = clean_script.replace(
            "#",
            "",
        )

        clean_script = clean_script.replace(
            "•",
            "",
        )

        # ====================================================
        # SAVE TRANSCRIPT
        # ====================================================

        with open(
            transcript_file,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                clean_script
            )

        print("Transcript saved.")

        # ====================================================
        # GENERATE AUDIO
        # ====================================================

        print()
        print("Generating audio...")
        print("Language:", language)
        print("Voice:", voice)

        episode_ref.update(
            {
                "status": "generating_audio"
            }
        )

        generate_podcast_audio(
            text=clean_script,
            language=language,
            voice=voice,
            output_file=raw_audio,
        )

        if not os.path.exists(
            raw_audio
        ):

            raise RuntimeError(
                "Audio generation completed but MP3 file was not created."
            )

        print("Raw audio generated.")

               # ====================================================
        # ADD INTRO / OUTRO
        # ====================================================

        print("Adding intro and outro...")

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        intro_audio = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "intro.mp3",
        )

        if not os.path.exists(intro_audio):
            raise FileNotFoundError(
                f"Intro audio not found: {intro_audio}"
            )

        command = [
            ffmpeg_path,

            "-i",
            intro_audio,

            "-i",
            raw_audio,

            "-i",
            intro_audio,

            "-filter_complex",
            (
                "[0:a]aresample=44100,"
                "aformat=sample_fmts=fltp:"
                "sample_rates=44100:"
                "channel_layouts=stereo[intro];"

                "[1:a]aresample=44100,"
                "aformat=sample_fmts=fltp:"
                "sample_rates=44100:"
                "channel_layouts=stereo[podcast];"

                "[2:a]aresample=44100,"
                "aformat=sample_fmts=fltp:"
                "sample_rates=44100:"
                "channel_layouts=stereo[outro];"

                "[intro][podcast][outro]"
                "concat=n=3:v=0:a=1[out]"
            ),

            "-map",
            "[out]",

            "-codec:a",
            "libmp3lame",

            "-b:a",
            "128k",

            final_audio,

            "-y",
        ]

        try:
            subprocess.run(
                command,
                check=True,
            )

            print("Intro/outro added successfully.")
            print("Final podcast:", final_audio)

        except Exception as ffmpeg_error:
            print(
                "FFmpeg failed:",
                ffmpeg_error,
            )

            print("Using raw podcast audio.")

            final_audio = raw_audio


        # ====================================================
        # VERIFY FINAL FILE
        # ====================================================

        if not os.path.exists(final_audio):

            raise RuntimeError(
                "Final podcast MP3 was not created."
            )


        print(
            "Final podcast file verified:",
            final_audio,
        )
       

                # ====================================================
        # GET ACTUAL PODCAST DURATION
        # ====================================================

        print("Calculating actual podcast duration...")

        probe_command = [
            ffmpeg_path,
            "-i",
            final_audio,
        ]

        probe_result = subprocess.run(
            probe_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        import re

        duration_match = re.search(
            r"Duration: (\d+):(\d+):(\d+\.\d+)",
            probe_result.stderr,
        )

        if duration_match:

            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = float(duration_match.group(3))

            actual_duration_seconds = int(
                hours * 3600
                + minutes * 60
                + seconds
            )

        else:

            print(
                "Could not detect actual duration. "
                "Using requested duration as fallback."
            )

            actual_duration_seconds = (
                podcast_length * 60
            )

        print(
            "Actual podcast duration:",
            actual_duration_seconds,
            "seconds",
        )

        # ====================================================
# UPLOAD FINAL AUDIO TO CLOUDINARY
# ====================================================

        # ====================================================
        # UPLOAD FINAL AUDIO TO CLOUDINARY
        # ====================================================

        print()
        print("Uploading final podcast to Cloudinary...")

        episode_ref.update(
            {
                "status": "uploading"
            }
        )

        upload_result = upload_podcast_audio(
            file_path=final_audio,
            uid=uid,
            date=today,
        )

        audio_url = upload_result["audio_url"]
        cloudinary_public_id = upload_result["public_id"]

        print("Permanent audio URL:", audio_url)

        # ====================================================
        # SAVE PODCAST METADATA TO FIRESTORE
        # ====================================================

        episode_data = {
            "podcast_id": today,
            "title": "Morning Brief",
            "date": today,
            "status": "completed",
            "country": country,
            "state": state,
            "language": language,
            "voice": voice,
             "duration": actual_duration_seconds,
            "categories": selected_categories,
            "cloudinary_public_id": cloudinary_public_id,
            "audio_url": audio_url,
            "transcript": clean_script,
            "highlights": highlights,
            "completed_at": datetime.now(IST),
        }

        episode_ref.set(
            episode_data,
            merge=True,
        )

        # ====================================================
        # CLEAN TEMPORARY LOCAL FILES
        # ====================================================

        temporary_files = [
            raw_audio,
            final_audio,
            transcript_file,
            highlights_file,
        ]

        for temporary_file in temporary_files:

            try:

                if os.path.exists(temporary_file):
                    os.remove(temporary_file)

            except Exception as cleanup_error:

                print(
                    "Temporary file cleanup failed:",
                    cleanup_error,
                )

        # ====================================================
        # SUCCESS
        # ====================================================

        print()
        print("=" * 60)
        print("PODCAST GENERATION SUCCESSFUL")
        print("USER:", uid)
        print("AUDIO URL:", audio_url)
        print("=" * 60)

        return episode_data

    # ========================================================
    # GENERATION FAILURE
    # ========================================================

    except Exception as e:

        print()
        print("=" * 60)
        print("PODCAST GENERATION FAILED")
        print("USER:", uid)
        print("ERROR:", str(e))
        print("=" * 60)

        episode_ref.set(
            {
                "status": "failed",
                "error": str(e),
                "failed_at": datetime.now(IST),
            },
            merge=True,
        )

        raise