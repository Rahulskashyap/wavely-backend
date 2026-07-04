from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

voices = client.voices.get_all()

for voice in voices.voices:
    print("Name:", voice.name)
    print("Voice ID:", voice.voice_id)

    try:
        print("Labels:", voice.labels)
    except:
        pass

    print("-" * 50)