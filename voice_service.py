import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

VOICE_MAP = {
    "Female": "XrExE9yKIg1WjnnlVkGX",  # Matilda
    "Male": "onwK4e9ZLuTAKqWW03F9",    # Daniel
    "Anchor": "onwK4e9ZLuTAKqWW03F9"   # Daniel
}



def generate_audio(text, voice="Female", output_file="podcast.mp3"):

    voice_id = VOICE_MAP.get(
        voice,
        VOICE_MAP["Female"]
    )

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2"
    )

    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_file