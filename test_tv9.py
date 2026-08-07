from news_v4.collector import collect_source
from news_v4.news_sources import get_source


def main():

    source = get_source(
        "tv9_kannada_karnataka"
    )

    if source is None:
        print("TV9 source not found")
        return

    articles = collect_source(
        source
    )

    print("\n==============================")
    print("TV9 KANNADA TEST")
    print("==============================")

    print(
        "\nTOTAL ARTICLES:",
        len(articles),
    )

    for article in articles[:20]:

        print("\n------------------------------")

        print(
            "TITLE:",
            article.get("title"),
        )

        print(
            "URL:",
            article.get("url"),
        )

        print(
            "DATE:",
            article.get(
                "published_at"
            ),
        )

        print(
            "REGION:",
            article.get("region"),
        )

        print(
            "CATEGORIES:",
            article.get(
                "categories"
            ),
        )


if __name__ == "__main__":
    main()