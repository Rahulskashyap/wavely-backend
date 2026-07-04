
import os
import json
from google.cloud import texttospeech
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()


def get_google_tts_client():

    credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT")

    # Render / production
    if credentials_json:
        credentials_dict = json.loads(credentials_json)

        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict
        )

        return texttospeech.TextToSpeechClient(
            credentials=credentials
        )

    # Local development: use GOOGLE_APPLICATION_CREDENTIALS
    local_credentials_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )

    if local_credentials_path:
        return texttospeech.TextToSpeechClient.from_service_account_file(
            local_credentials_path
        )

    raise RuntimeError(
        "Google TTS credentials not found. "
        "Set GOOGLE_SERVICE_ACCOUNT on Render or "
        "GOOGLE_APPLICATION_CREDENTIALS locally."
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

    client = get_google_tts_client()


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