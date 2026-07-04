import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",  # Bella
    text="Good morning. Welcome to AI News Podcast. This is a test of the ElevenLabs voice system.",
    model_id="eleven_multilingual_v2"
)

with open("test_voice.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("Voice generated successfully!")