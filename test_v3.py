from news_service_v3 import get_all_news

data = get_all_news()

for category, news in data.items():

    articles = news.get("articles", [])

    print("\n")
    print("=" * 50)
    print(category.upper())
    print("=" * 50)

    print("Articles:", len(articles))

    if articles:
        print("First Article:")
        print(articles[0]["title"])