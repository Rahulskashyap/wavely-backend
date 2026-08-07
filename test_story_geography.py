from news_v4.geographic_ranker import classify_story


def run_test(
    name,
    story,
    expected,
    preferred_state="karnataka",
):
    result = classify_story(
        story,
        preferred_state,
    )

    actual = result["scope"]

    print("\n------------------------------")
    print("TEST:", name)
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)
    print("STATES:", result.get("states", []))

    passed = actual == expected

    print(
        "RESULT:",
        "PASS" if passed else "FAIL",
    )

    return passed


tests = []


# =========================================================
# TEST 1
# ONE KARNATAKA ARTICLE + TWO NATIONAL ARTICLES
#
# One Karnataka article must not hijack a national cluster.
# =========================================================

tests.append(
    run_test(
        "One Karnataka article in national cluster",
        {
            "articles": [
                {
                    "title":
                        "Major cricket announcement "
                        "made in India",

                    "summary":
                        "A major cricket announcement "
                        "was made nationally.",

                    "region": "national",

                    "categories": [
                        "sports",
                        "national",
                    ],
                },
                {
                    "title":
                        "Indian cricket receives "
                        "major update",

                    "summary":
                        "The announcement affects "
                        "Indian cricket.",

                    "region": "national",

                    "categories": [
                        "sports",
                        "national",
                    ],
                },
                {
                    "title":
                        "Cricket announcement receives "
                        "attention in Karnataka",

                    "summary":
                        "The national announcement "
                        "was also reported in Karnataka.",

                    "region": "karnataka",

                    "categories": [
                        "sports",
                    ],
                },
            ]
        },
        "national",
    )
)


# =========================================================
# TEST 2
# REAL KARNATAKA CLUSTER
#
# Majority explicit Karnataka evidence should remain
# preferred_state.
# =========================================================

tests.append(
    run_test(
        "Real Karnataka cluster",
        {
            "articles": [
                {
                    "title":
                        "Heavy rain hits Bengaluru",

                    "summary":
                        "Several Bengaluru areas "
                        "reported heavy rainfall.",

                    "region": "karnataka",

                    "categories": [
                        "state",
                        "local",
                    ],
                },
                {
                    "title":
                        "Karnataka rain alert issued",

                    "summary":
                        "Authorities issued a rain "
                        "alert across Karnataka.",

                    "region": "karnataka",

                    "categories": [
                        "state",
                    ],
                },
                {
                    "title":
                        "Bengaluru prepares for "
                        "more rainfall",

                    "summary":
                        "Rain is expected to continue "
                        "in Bengaluru.",

                    "region": None,

                    "categories": [
                        "local",
                    ],
                },
            ]
        },
        "preferred_state",
    )
)


# =========================================================
# TEST 3
# ENGLAND CRICKET
#
# A foreign cricket story must not become national merely
# because it appears in an Indian publisher/feed.
# =========================================================

tests.append(
    run_test(
        "England cricket story",
        {
            "articles": [
                {
                    "title":
                        "Fleming named new England "
                        "Test coach with Root captain",

                    "summary":
                        "England announce changes to "
                        "their Test cricket setup.",

                    "region": "world",

                    "categories": [
                        "sports",
                        "world",
                    ],
                },
                {
                    "title":
                        "England appoint Fleming as "
                        "new Test coach",

                    "summary":
                        "Joe Root will captain England "
                        "under the new coaching setup.",

                    "region": None,

                    "categories": [
                        "sports",
                    ],
                },
            ]
        },
        "world",
    )
)


# =========================================================
# TEST 4
# INDIA PARLIAMENT
#
# Explicit Indian Parliament evidence must remain national
# even if one source/category carries world-style metadata.
# =========================================================

tests.append(
    run_test(
        "Indian Parliament story",
        {
            "articles": [
                {
                    "title":
                        "India Parliament discusses "
                        "Gen Z participation",

                    "summary":
                        "Members of Parliament in India "
                        "discussed Gen Z and youth "
                        "participation.",

                    "region": "national",

                    "categories": [
                        "national",
                        "politics",
                    ],
                },
                {
                    "title":
                        "Gen Z discussion reaches "
                        "Indian Parliament",

                    "summary":
                        "The discussion took place "
                        "during proceedings in India's "
                        "Parliament.",

                    "region": None,

                    "categories": [
                        "politics",
                    ],
                },
            ]
        },
        "national",
    )
)


print("\n==============================")
print("SUMMARY")
print("==============================")

passed = sum(tests)
total = len(tests)

print("PASSED:", passed)
print("FAILED:", total - passed)
print("TOTAL:", total)

if passed == total:
    print(
        "\nALL STORY GEOGRAPHY TESTS PASSED"
    )
else:
    print(
        "\nSOME STORY GEOGRAPHY TESTS FAILED"
    )