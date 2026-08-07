from news_v4.claim_verifier import compare_articles


TESTS = [

    # -----------------------------------
    # TEST 1: AGREEMENT
    # -----------------------------------

    (
        {
            "title":
                "Three dead and several injured in Seattle shooting",

            "summary":
                "Three people were killed and several others "
                "injured at a festival in Seattle.",

            "publisher_id": "bbc",

            "source_name": "BBC News",
        },

        {
            "title":
                "Seattle festival shooting leaves 3 dead",

            "summary":
                "Three people died after a shooting near "
                "Seattle's Space Needle.",

            "publisher_id":
                "indian_express",

            "source_name":
                "The Indian Express",
        },
    ),

    # -----------------------------------
    # TEST 2: CONFLICT
    # -----------------------------------

    (
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
    ),

]


for article_a, article_b in TESTS:

    result = compare_articles(
        article_a,
        article_b,
    )

    print("\n==============================")

    print(
        article_a["source_name"],
        "VS",
        article_b["source_name"],
    )

    print(
        "STATUS:",
        result["status"].upper(),
    )

    print(
        "AGREEMENTS:",
        result["agreements"],
    )

    print(
        "CONFLICTS:",
        result["conflicts"],
    )