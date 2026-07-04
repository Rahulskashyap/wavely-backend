from news_engine import get_news_by_mode

data = get_news_by_mode()

print("\nSELECTED FEEDS\n")

for category in data:

    articles = data[category].get("articles", [])

    print(category.upper(), ":", len(articles))