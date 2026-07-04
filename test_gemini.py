from gemini_service import generate_podcast_script

sample_news = """
India's economy grew this quarter.
A major AI company released a new model.
India won a cricket series.
"""

script = generate_podcast_script(sample_news)

print(script)