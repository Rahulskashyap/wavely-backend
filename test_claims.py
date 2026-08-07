from news_v4.claim_extractor import extract_claims


articles = [

    {
        "title":
            "Three dead and several injured in Seattle shooting",

        "summary":
            "Three people were killed and several others "
            "injured at a food festival in Seattle.",

        "publisher_id": "bbc",

        "source_name": "BBC News",
    },

    {
        "title":
            "Seattle festival shooting leaves 3 dead",

        "summary":
            "Three people died after a shooting near "
            "Seattle's Space Needle.",

        "publisher_id": "indian_express",

        "source_name": "The Indian Express",
    },

    {
        "title":
            "Company reports $2 billion profit",

        "summary":
            "The company announced its financial results.",

        "publisher_id": "source_a",

        "source_name": "Source A",
    },

    {
        "title":
            "Company reports $2 billion loss",

        "summary":
            "The company released its financial results.",

        "publisher_id": "source_b",

        "source_name": "Source B",
    },

]


for article in articles:

    claims = extract_claims(article)

    print("\n==============================")

    print(
        "SOURCE:",
        claims["source_name"],
    )

    print(
        "TITLE:",
        claims["title"],
    )

    print(
        "NUMBERS:",
        claims["numbers"],
    )

    print(
        "MONEY:",
        claims["money"],
    )

    print(
        "PERCENTAGES:",
        claims["percentages"],
    )

    print(
        "ACTIONS:",
        claims["actions"],
    )
    print(
    "DIRECTIONS:",
    claims["directions"],
)