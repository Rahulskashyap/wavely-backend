from rss_service import get_google_news

articles = get_google_news("Karnataka")

print("Articles:", len(articles))

for article in articles[:5]:
    print(article["title"])