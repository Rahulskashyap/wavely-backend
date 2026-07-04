import os

PODCAST_DIR = "podcasts"

BASE_URL = os.getenv(
    "BASE_URL",
    "https://wavely-backend-uet3.onrender.com"
)


def get_podcast_history():

    os.makedirs(PODCAST_DIR, exist_ok=True)

    files = []

    for file in os.listdir(PODCAST_DIR):

        if file.endswith("_final.mp3"):
            files.append(file)

        elif file.endswith(".mp3"):

            date = file.replace(".mp3", "")
            final_version = f"{date}_final.mp3"

            # Add raw audio only if final version does not exist
            if not os.path.exists(
                os.path.join(PODCAST_DIR, final_version)
            ):
                files.append(file)

    files.sort(reverse=True)

    podcasts = []

    for i, file in enumerate(files):

        date = file.replace("_final.mp3", "")
        date = date.replace(".mp3", "")

        podcasts.append({
            "podcast_id": str(i + 1),
            "title": "Morning Brief",
            "date": date,
            "duration": 25,
            "audio_url": f"{BASE_URL}/podcasts/{file}",
            "categories": ["News"]
        })

    return podcasts