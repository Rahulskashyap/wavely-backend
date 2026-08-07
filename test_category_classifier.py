from news_v4.category_classifier import (
    classify_article,
)


def run_test(
    name,
    article,
    expected,
):
    classify_article(
        article
    )

    actual = article[
        "category"
    ]

    passed = (
        actual == expected
    )

    print("\n------------------------------")
    print("TEST:", name)
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)
    print(
        "CATEGORIES:",
        article["categories"],
    )
    print(
        "CONFIDENCE:",
        article[
            "category_confidence"
        ],
    )
    print(
        "RESULT:",
        "PASS" if passed else "FAIL",
    )

    return passed


tests = []


tests.append(
    run_test(
        "Karnataka rainfall",
        {
            "title":
                "Heavy rainfall alert issued "
                "across Karnataka",

            "summary":
                "IMD forecasts heavy rain "
                "for several districts.",

            "categories": [
                "state",
                "local",
            ],
        },
        "weather",
    )
)


tests.append(
    run_test(
        "India technology policy",
        {
            "title":
                "India announces new "
                "technology policy",

            "summary":
                "The government announced "
                "a national technology policy.",

            "categories": [
                "national",
            ],
        },
        "technology",
    )
)


tests.append(
    run_test(
        "England cricket",
        {
            "title":
                "England appoint new "
                "Test cricket coach",

            "summary":
                "The England cricket team "
                "announced its new coach.",

            "categories": [
                "world",
                "sports",
            ],
        },
        "sports",
    )
)


tests.append(
    run_test(
        "Stock market",
        {
            "title":
                "Sensex and Nifty rise "
                "after market rally",

            "summary":
                "Indian stock markets gained "
                "during today's session.",

            "categories": [
                "business",
            ],
        },
        "business",
    )
)


tests.append(
    run_test(
        "ISRO mission",
        {
            "title":
                "ISRO announces new "
                "space mission",

            "summary":
                "The mission will launch "
                "a satellite into orbit.",

            "categories": [
                "national",
            ],
        },
        "science",
    )
)


tests.append(
    run_test(
        "Police arrest",
        {
            "title":
                "Police arrest suspect "
                "after Bengaluru robbery",

            "summary":
                "Police arrested the accused "
                "following an investigation.",

            "categories": [
                "state",
                "local",
            ],
        },
        "crime",
    )
)


tests.append(
    run_test(
        "University admissions",
        {
            "title":
                "University announces "
                "new admission process",

            "summary":
                "Students can apply for "
                "college admissions online.",

            "categories": [
                "national",
            ],
        },
        "education",
    )
)


tests.append(
    run_test(
        "Film release",
        {
            "title":
                "New film opens strongly "
                "at box office",

            "summary":
                "The movie recorded a strong "
                "opening in cinemas.",

            "categories": [
                "entertainment",
            ],
        },
        "entertainment",
    )
)


tests.append(
    run_test(
        "Hospital health update",
        {
            "title":
                "Doctors announce new "
                "cancer treatment",

            "summary":
                "Researchers and doctors "
                "reported new treatment results.",

            "categories": [
                "health",
            ],
        },
        "health",
    )
)


tests.append(
    run_test(
        "Unknown generic story",
        {
            "title":
                "Major development "
                "announced today",

            "summary":
                "Officials shared more "
                "details about the development.",

            "categories": [
                "national",
            ],
        },
        "general",
    )
)
# =========================================================
# AMBIGUITY TESTS
# =========================================================

tests.append(
    run_test(
        "AI regulation",
        {
            "title":
                "Government announces new AI regulation",

            "summary":
                "New artificial intelligence rules "
                "will govern technology companies.",

            "categories": [
                "technology",
                "national",
            ],
        },
        "technology",
    )
)


tests.append(
    run_test(
        "Sports ministry decision",
        {
            "title":
                "Sports ministry announces new "
                "cricket development programme",

            "summary":
                "The programme will support cricket "
                "players and national sports training.",

            "categories": [
                "sports",
                "national",
            ],
        },
        "sports",
    )
)


tests.append(
    run_test(
        "National health policy",
        {
            "title":
                "Government announces new "
                "national health policy",

            "summary":
                "The healthcare policy will improve "
                "hospitals and patient treatment.",

            "categories": [
                "health",
                "national",
            ],
        },
        "health",
    )
)


tests.append(
    run_test(
        "Cybercrime arrest",
        {
            "title":
                "Police arrest suspect in "
                "major cybercrime case",

            "summary":
                "Investigators arrested the accused "
                "after a cybersecurity fraud probe.",

            "categories": [
                "technology",
                "national",
            ],
        },
        "crime",
    )
)


tests.append(
    run_test(
        "Climate research",
        {
            "title":
                "Scientists publish new "
                "climate research",

            "summary":
                "Researchers studied climate change "
                "and rising global temperatures.",

            "categories": [
                "science",
                "world",
            ],
        },
        "science",
    )
)


tests.append(
    run_test(
        "Corporate fraud",
        {
            "title":
                "Major company faces corporate "
                "fraud investigation",

            "summary":
                "Financial investigators are examining "
                "fraud allegations involving the company.",

            "categories": [
                "business",
                "national",
            ],
        },
        "business",
    )
)


print("\n==============================")
print("SUMMARY")
print("==============================")

passed = sum(
    tests
)

total = len(
    tests
)

print(
    "PASSED:",
    passed,
)

print(
    "FAILED:",
    total - passed,
)

print(
    "TOTAL:",
    total,
)


if passed == total:

    print(
        "\nALL CATEGORY "
        "CLASSIFIER TESTS PASSED"
    )

else:

    print(
        "\nCATEGORY CLASSIFIER "
        "TEST FAILED"
    )

    raise SystemExit(1)