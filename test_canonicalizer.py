from news_v4.canonicalizer import canonicalize_articles


articles = [
    {
        "title": (
            "ತಮಿಳುನಾಡಿಗೆ ಕಾವೇರಿ ನೀರು ಬಿಡಲು "
            "CWRC ಆದೇಶ"
        ),
        "summary": "",
        "categories": ["state"],
    },

    {
        "title": (
            "India announces new "
            "technology policy"
        ),
        "summary": "",
        "categories": ["national"],
    },
]


result = canonicalize_articles(
    articles
)


print("\n==============================")
print("RESULT")
print("==============================")


for article in result:

    print("\nORIGINAL:")
    print(
        article["title"]
    )

    print("\nCANONICAL:")
    print(
        article["canonical_title"]
    )

    print(
        "\nCANONICALIZED:",
        article["canonicalized"],
    )

    print("------------------------------")