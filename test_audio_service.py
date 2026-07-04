from audio_service import generate_podcast_audio

generate_podcast_audio(
    text="""
ನಮಸ್ಕಾರ.
ಇದು AI News Podcast.
ಇಂದಿನ ಪ್ರಮುಖ ಸುದ್ದಿಗಳಿಗೆ ಸ್ವಾಗತ.
""",
    language="Kannada",
    output_file="final_test.mp3"
)

print("Generated!")