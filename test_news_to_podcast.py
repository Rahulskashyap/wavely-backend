from news_service import get_global_news
from gemini_service import generate_podcast_script

news_data = get_global_news()

articles = news_data.get("articles", [])

news_text = ""

for article in articles:
    title = article.get("title", "")
    description = article.get("description", "")

    news_text += f"""
Title: {title}
Description: {description}

"""

print("Fetched", len(articles), "articles")

script = generate_podcast_script(news_text)

with open("podcast_script.txt", "w", encoding="utf-8") as file:
    file.write(script)

print("Podcast script generated successfully!")