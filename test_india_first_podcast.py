from news_service import get_global_news
from gemini_service import generate_podcast_script

news_data = get_global_news()

articles = news_data.get("articles", [])

india_news = ""
world_news = ""

for article in articles:

    title = article.get("title", "")
    description = article.get("description", "")

    source = article.get("source", {}).get("name", "")

    text = f"Title: {title}\nDescription: {description}\n"

    # Basic India filtering
    if any(word in text.lower() for word in [
        "india", "indian", "delhi", "mumbai",
        "karnataka", "bengaluru", "chennai",
        "hyderabad", "kolkata"
    ]):
        india_news += text + "\n"
    else:
        world_news += text + "\n"

news_text = f"""
INDIA NEWS:

{india_news}

WORLD NEWS:

{world_news}
"""

script = generate_podcast_script(news_text)

with open("india_first_podcast.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("India-first podcast generated successfully!")