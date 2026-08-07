from news_v4.collector import collect_all_news


def main():
    print("\nCollecting raw articles...\n")

    articles = collect_all_news()

    matches = []

    for article in articles:

        title = str(
            article.get("title", "")
        )

        summary = str(
            article.get("summary", "")
        )

        text = f"{title} {summary}".lower()

        if (
            "rushdie" in text
            or "hadi matar" in text
        ):
            matches.append(article)

    print("\n==============================")
    print("RUSHDIE ARTICLES")
    print("==============================")
    print("FOUND:", len(matches))

    for index, article in enumerate(
        matches,
        start=1,
    ):
        print("\n------------------------------")
        print("ARTICLE:", index)

        print(
            "PUBLISHER:",
            article.get("publisher")
            or article.get("publisher_name")
            or article.get("publisher_id")
        )

        print(
            "TITLE:",
            article.get("title")
        )

        print(
            "SUMMARY:",
            article.get("summary")
        )

        print(
            "CATEGORIES:",
            article.get("categories")
        )

        print(
            "REGION:",
            article.get("region")
        )

        print(
            "FEED REGION:",
            article.get("feed_region")
        )

        print(
            "PUBLISHED:",
            article.get("published_at")
        )

        print(
            "URL:",
            article.get("url")
        )


if __name__ == "__main__":
    main()