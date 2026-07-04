from gtts import gTTS
from datetime import datetime

with open("india_first_podcast_v2.txt", "r", encoding="utf-8") as file:
    text = file.read()

tts = gTTS(
    text=text,
    lang="en",
    slow=False
)

today = datetime.now().strftime("%Y-%m-%d")

filename = f"../podcasts/{today}.mp3"

tts.save(filename)

print("Saved:", filename)