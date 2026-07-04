from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "roamora-490516-f082168bf524.json  "

client = texttospeech.TextToSpeechClient()

text = """
ನಮಸ್ಕಾರ.
ಇದು AI News Podcast.
ಇಂದಿನ ಕರ್ನಾಟಕ ಮತ್ತು ಭಾರತದ ಪ್ರಮುಖ ಸುದ್ದಿಗಳಿಗೆ ಸ್ವಾಗತ.
"""

synthesis_input = texttospeech.SynthesisInput(text=text)

voice = texttospeech.VoiceSelectionParams(
    language_code="kn-IN",
    name="kn-IN-Standard-A"
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

with open("google_kannada.mp3", "wb") as out:
    out.write(response.audio_content)

print("Google Kannada voice generated!")