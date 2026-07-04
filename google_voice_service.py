
from google.cloud import texttospeech
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

LANGUAGE_VOICES = {
    "English": {
        "Male": ("en-IN", "en-IN-Standard-B"),
        "Female": ("en-IN", "en-IN-Standard-C"),
    },
    "Kannada": {
        "Male": ("kn-IN", "kn-IN-Standard-B"),
        "Female": ("kn-IN", "kn-IN-Standard-A"),
    },
    "Hindi": {
        "Male": ("hi-IN", "hi-IN-Standard-B"),
        "Female": ("hi-IN", "hi-IN-Standard-A"),
    },
    "Tamil": {
        "Male": ("ta-IN", "ta-IN-Standard-B"),
        "Female": ("ta-IN", "ta-IN-Standard-A"),
    },
    "Telugu": {
        "Male": ("te-IN", "te-IN-Standard-B"),
        "Female": ("te-IN", "te-IN-Standard-A"),
    },
    "Malayalam": {
        "Male": ("ml-IN", "ml-IN-Standard-B"),
        "Female": ("ml-IN", "ml-IN-Standard-A"),
    },
}


def split_text(text, max_chars=1000):

    chunks = []

    while len(text) > max_chars:

        split_index = text.rfind(".", 0, max_chars)

        if split_index == -1:
            split_index = max_chars

        chunks.append(text[:split_index])

        text = text[split_index:]

    chunks.append(text)

    return chunks


def generate_google_audio(text, language, voice, output_file):

    client = texttospeech.TextToSpeechClient()

    voice_map = LANGUAGE_VOICES.get(language)

    if voice_map:
        language_code, voice_name = voice_map.get(
            voice,
            voice_map["Male"]
        )
    else:
        language_code, voice_name = ("en-IN", "en-IN-Standard-B")

    print("Google TTS Language:", language)
    print("Voice:", voice_name)

    chunks = split_text(text)

    with open(output_file, "wb") as final_audio:

        for i, chunk in enumerate(chunks):

            print(f"Generating chunk {i+1}/{len(chunks)}")

            synthesis_input = texttospeech.SynthesisInput(
                text=chunk
            )

            selected_voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=selected_voice,
                audio_config=audio_config
            )

            final_audio.write(response.audio_content)

    print("Audio generation completed")

    return output_file