from news_v4.geographic_ranker import classify_story


def run_test(name, story, expected):
    result = classify_story(
        story,
        preferred_state="karnataka",
    )

    actual = result["scope"]

    print("\n------------------------------")
    print("TEST:", name)
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)
    print("STATES:", result.get("states", []))

    passed = actual == expected
    print("RESULT:", "PASS" if passed else "FAIL")

    return passed


tests = []


# =========================================================
# TEST 1
# KARNATAKA RAIN + NOISY NATIONAL METADATA
# =========================================================

tests.append(
    run_test(
        "Karnataka rain cluster with national noise",
        {
            "articles": [
                {
                    "title":
                        "Karnataka Rains: ರಾಜ್ಯದಲ್ಲಿ "
                        "ಮತ್ತೆ 5 ದಿನ ಭಾರೀ ಮಳೆ",

                    "summary":
                        "Heavy rainfall is expected "
                        "across Karnataka for the "
                        "next five days.",

                    "region": None,

                    "feed_region": "karnataka",

                    "categories": [
                        "state",
                        "local",
                    ],
                },
                {
                    "title":
                        "Heavy rain alert issued "
                        "across Karnataka",

                    "summary":
                        "Several Karnataka districts "
                        "may receive heavy rainfall.",

                    # Intentionally noisy metadata
                    "region": "national",

                    "categories": [
                        "national",
                    ],
                },
            ]
        },
        "preferred_state",
    )
)


# =========================================================
# TEST 2
# ENGLAND CRICKET + NOISY NATIONAL METADATA
# =========================================================

tests.append(
    run_test(
        "England cricket cluster with national noise",
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
                        "world",
                        "sports",
                        "cricket",
                    ],
                },
                {
                    "title":
                        "England make major Test "
                        "cricket changes",

                    "summary":
                        "England's Test team gets "
                        "a new coaching setup.",

                    # Intentionally noisy metadata
                    "region": "national",

                    "categories": [
                        "sports",
                        "cricket",
                    ],
                },
            ]
        },
        "world",
    )
)


# =========================================================
# SUMMARY
# =========================================================

print("\n==============================")
print("REAL GEOGRAPHY REGRESSION TEST")
print("==============================")

passed = sum(tests)
total = len(tests)

print("PASSED:", passed)
print("FAILED:", total - passed)
print("TOTAL:", total)


if passed == total:
    print(
        "\nALL REAL GEOGRAPHY "
        "REGRESSION TESTS PASSED"
    )
else:
    print(
        "\nREAL GEOGRAPHY "
        "REGRESSION DETECTED"
    )

    raise SystemExit(1)