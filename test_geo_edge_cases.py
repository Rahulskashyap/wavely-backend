from news_v4.geo_classifier import classify_geography


TEST_ARTICLES = [
    # =====================================================
    # KARNATAKA
    # =====================================================
    {
        "title": "Bengaluru metro expansion announced",
        "summary": "New metro routes will be developed in Bengaluru.",
        "region": "karnataka",
        "categories": ["state", "local"],
        "publisher_id": "tv9_kannada",
        "expected": "preferred_state",
    },

    # =====================================================
    # MAHARASHTRA
    # =====================================================
    {
        "title": "Mumbai receives heavy rainfall",
        "summary": "Heavy rain affected parts of Mumbai today.",
        "region": "maharashtra",
        "categories": ["state", "local"],
        "publisher_id": "indian_express",
        "expected": "other_state",
    },

    # =====================================================
    # INDIA NATIONAL
    # =====================================================
    {
        "title": "India announces new national technology policy",
        "summary": "The Union government announced the policy today.",
        "region": "india",
        "categories": ["national", "technology"],
        "publisher_id": "hindustan_times",
        "expected": "national",
    },

    # =====================================================
    # BBC WORLD
    # =====================================================
    {
        "title": "European leaders meet for major summit",
        "summary": "European leaders are meeting to discuss regional issues.",
        "region": "world",
        "categories": ["world"],
        "publisher_id": "bbc",
        "expected": "world",
    },

    # =====================================================
    # INDIAN PUBLISHER REPORTING WORLD NEWS
    # =====================================================
    {
        "title": "Earthquake hits southern Japan",
        "summary": "A strong earthquake struck southern Japan.",
        "region": "world",
        "categories": ["world"],
        "publisher_id": "indian_express",
        "expected": "world",
    },

    # =====================================================
    # NDTV WORLD
    # =====================================================
    {
        "title": "US President meets European leaders",
        "summary": "The meeting took place during an international summit.",
        "region": "world",
        "categories": ["world"],
        "publisher_id": "ndtv",
        "expected": "world",
    },

    # =====================================================
    # NASA / WORLD
    # =====================================================
    {
        "title": "NASA announces new space mission",
        "summary": "NASA announced details of a future space mission.",
        "region": "world",
        "categories": ["science", "technology", "world"],
        "publisher_id": "nasa",
        "expected": "world",
    },

    # =====================================================
    # INDIAN PUBLISHER WITHOUT INDIA IN HEADLINE
    # =====================================================
    {
        "title": "Government approves new education scheme",
        "summary": "The scheme was approved following a cabinet meeting.",
        "region": "india",
        "categories": ["national"],
        "publisher_id": "indian_express",
        "expected": "national",
    },

    # =====================================================
    # WORLD STORY WITH WORD 'CENTER'
    # =====================================================
    {
        "title": "New research center opens in London",
        "summary": "The research facility opened in the UK capital.",
        "region": "world",
        "categories": ["world", "technology"],
        "publisher_id": "bbc",
        "expected": "world",
    },

    # =====================================================
    # WORLD STORY FROM INDIAN PUBLISHER
    # =====================================================
    {
        "title": "West Indies win cricket series",
        "summary": "West Indies completed a series victory.",
        "region": "world",
        "categories": ["world", "sports"],
        "publisher_id": "hindustan_times",
        "expected": "world",
    },
]


def main():

    preferred_state = "karnataka"

    print("\n==============================")
    print("GEOGRAPHY EDGE CASE TEST")
    print("==============================")

    passed = 0
    failed = 0

    for index, article in enumerate(
        TEST_ARTICLES,
        start=1,
    ):

        result = classify_geography(
            article,
            preferred_state=preferred_state,
        )

        actual = result["scope"]
        expected = article["expected"]

        success = actual == expected

        if success:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"

        print("\n------------------------------")
        print("TEST:", index)
        print("TITLE:", article["title"])
        print("REGION:", article["region"])
        print("EXPECTED:", expected)
        print("ACTUAL:", actual)
        print("STATES:", result["states"])
        print("RESULT:", status)

    print("\n==============================")
    print("SUMMARY")
    print("==============================")

    print("PASSED:", passed)
    print("FAILED:", failed)
    print("TOTAL:", len(TEST_ARTICLES))

    if failed == 0:
        print("\nALL GEOGRAPHY TESTS PASSED")
    else:
        print(
            "\nSome geography tests failed."
        )


if __name__ == "__main__":
    main()