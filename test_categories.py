from news_service_v2 import get_all_india_news

data = get_all_india_news()

for category, news in data.items():

    print("\n")
    print("=" * 50)
    print(category.upper())
    print("=" * 50)

    print(news)

    articles = news.get("articles", [])

    print("Articles:", len(articles))

    if articles:
        print("First Article:")
        print(articles[0]["title"])