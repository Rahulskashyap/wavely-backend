from voice_service import generate_audio

generate_audio(
    text="""
ನಮಸ್ಕಾರ.
ಇದು AI News Podcast.
ಇಂದಿನ ಕರ್ನಾಟಕ ಮತ್ತು ಭಾರತದ ಪ್ರಮುಖ ಸುದ್ದಿಗಳಿಗೆ ಸ್ವಾಗತ.
""",
    voice="Anchor",
    output_file="kannada_test.mp3"
)

print("Audio Generated!")