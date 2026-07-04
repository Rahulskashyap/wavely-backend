import os

def get_podcast_history():

    podcast_folder = "../podcasts"

    if not os.path.exists(podcast_folder):
        return []

    files = []

    for file in os.listdir(podcast_folder):

        # Only keep FINAL podcasts
        if file.endswith("_final.mp3"):
            files.append(file)

    files.sort(reverse=True)

    podcasts = []

    for i, file in enumerate(files):

        date = file.replace("_final.mp3", "")

        podcasts.append({
            "podcast_id": str(i + 1),
            "title": "Morning Brief",
            "date": date,
            "duration": 15,
            "audio_url": f"http://192.168.1.11:8000/podcasts/{file}",
            "categories": ["News"]
        })

    return podcasts