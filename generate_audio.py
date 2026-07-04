from datetime import datetime
from audio_service import generate_podcast_audio

# Read podcast script
with open("india_first_podcast_v2.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Clean script

text = text.replace("[PAUSE]", "\n\n")

text = text.replace("[INTRO]", "")
text = text.replace("[OUTRO]", "")

text = text.replace("ENTRY THEME", "")
text = text.replace("ENTRY THEME FADING OUT", "")
text = text.replace("INTRO MUSIC", "")
text = text.replace("OUTRO MUSIC", "")

text = text.replace("*", "")
text = text.replace("#", "")
text = text.replace("•", "")

# Change this later to read from database/preferences
selected_language = "Kannada"

today = datetime.now().strftime("%Y-%m-%d")

filename = f"../podcasts/{today}.mp3"

print("Generating audio...")
print("Language:", selected_language)

generate_podcast_audio(
    text=text,
    language=selected_language,
    output_file=filename
)

print("Saved:", filename)