from news_v4.geo_classifier import classify_geography


TEST_ARTICLES = [

    {
        "title": "Bengaluru announces new metro expansion",
        "summary": "The Karnataka government announced the project.",
    },

    {
        "title": "Chennai receives heavy rainfall",
        "summary": "Several parts of Tamil Nadu were affected.",
    },

    {
        "title": "India announces new national technology policy",
        "summary": "The Union government announced the policy today.",
    },

    {
        "title": "European leaders meet for major summit",
        "summary": "Several European countries attended the meeting.",
    },
]


for article in TEST_ARTICLES:

    result = classify_geography(
        article,
        preferred_state="Karnataka",
    )

    print()
    print(article["title"])
    print("→", result)