
from google_voice_service import generate_google_audio

print("USING GOOGLE TTS")

def generate_podcast_audio(
    text,
    language,
    voice,
    output_file,
):
    return generate_google_audio(
        text=text,
        language=language,
        voice=voice,
        output_file=output_file,
    )