from news_service_v3 import get_all_news
from gemini_service import generate_podcast_script

data = get_all_news()

news_text = ""

for category, news in data.items():

    news_text += f"\n\n===== {category.upper()} NEWS =====\n\n"

    articles = news.get("articles", [])

    for article in articles:

        title = article.get("title", "")
        description = article.get("description", "")

        news_text += f"""
Title: {title}
Description: {description}

"""

script = generate_podcast_script(news_text)

with open("india_first_podcast_v2.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("Podcast generated successfully!")