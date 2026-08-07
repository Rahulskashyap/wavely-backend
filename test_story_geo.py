from news_v4.geographic_ranker import classify_story


# =========================================================
# TEST HELPER
# =========================================================

def test(
    name,
    story,
    expected,
):
    result = classify_story(
        story,
        preferred_state="karnataka",
    )

    actual = result["scope"]

    status = (
        "PASS"
        if actual == expected
        else "FAIL"
    )

    print("\n------------------------------")
    print("TEST:", name)
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)
    print(
        "STATES:",
        result.get("states", []),
    )
    print("RESULT:", status)

    return actual == expected


tests = []


# =========================================================
# TEST 1
# WORLD CLUSTER
#
# Indian publisher must NOT make a foreign story national.
# =========================================================

tests.append(
    test(
        "European wildfire cluster",
        {
            "articles": [
                {
                    "title":
                        "European wildfires spread "
                        "across region",

                    "summary":
                        "Wildfires continue across "
                        "several parts of Europe.",

                    "region":
                        "world",

                    "categories": [
                        "world",
                    ],

                    "publisher_id":
                        "bbc",
                },
                {
                    "title":
                        "Europe battles major "
                        "wildfires",

                    "summary":
                        "Emergency crews are fighting "
                        "wildfires across Europe.",

                    "region":
                        "world",

                    "categories": [
                        "world",
                    ],

                    "publisher_id":
                        "hindustan_times",
                },
            ]
        },
        "world",
    )
)


# =========================================================
# TEST 2
# KARNATAKA CLUSTER
#
# Multiple explicit Karnataka articles should produce
# preferred_state.
# =========================================================

tests.append(
    test(
        "Karnataka cluster",
        {
            "articles": [
                {
                    "title":
                        "Bengaluru metro expansion "
                        "announced",

                    "summary":
                        "New metro expansion plans "
                        "were announced in Bengaluru.",

                    "region":
                        "karnataka",

                    "categories": [
                        "state",
                    ],

                    "publisher_id":
                        "tv9_kannada",
                },
                {
                    "title":
                        "New Bengaluru metro routes "
                        "announced",

                    "summary":
                        "The Karnataka capital will "
                        "receive new metro routes.",

                    "region":
                        "karnataka",

                    "categories": [
                        "state",
                    ],

                    "publisher_id":
                        "public_tv",
                },
            ]
        },
        "preferred_state",
    )
)


# =========================================================
# TEST 3
# OTHER STATE
#
# Tamil Nadu article must remain other_state for a
# Karnataka user.
# =========================================================

tests.append(
    test(
        "Tamil Nadu cluster",
        {
            "articles": [
                {
                    "title":
                        "Heavy rain hits Chennai",

                    "summary":
                        "Heavy rainfall affected "
                        "several areas of Chennai.",

                    "region":
                        "tamil_nadu",

                    "categories": [
                        "state",
                    ],

                    "publisher_id":
                        "indian_express",
                },
            ]
        },
        "other_state",
    )
)


# =========================================================
# TEST 4
# NATIONAL
# =========================================================

tests.append(
    test(
        "India national cluster",
        {
            "articles": [
                {
                    "title":
                        "India announces new "
                        "technology policy",

                    "summary":
                        "The Government of India "
                        "announced a national "
                        "technology policy.",

                    "region":
                        "india",

                    "categories": [
                        "national",
                    ],

                    "publisher_id":
                        "hindustan_times",
                },
            ]
        },
        "national",
    )
)


# =========================================================
# TEST 5
# WORLD + FALSE STATE/SOURCE SIGNAL
#
# Publisher location must not affect story geography.
# =========================================================

tests.append(
    test(
        "World cluster with noisy article",
        {
            "articles": [
                {
                    "title":
                        "International ocean rescue "
                        "caught on video",

                    "summary":
                        "A rescue operation took place "
                        "during an international "
                        "ocean incident.",

                    "region":
                        "world",

                    "categories": [
                        "world",
                    ],

                    "publisher_id":
                        "bbc",
                },
                {
                    "title":
                        "Teen lifeguard performs "
                        "dramatic ocean rescue",

                    "summary":
                        "A lifeguard carried out a "
                        "rescue during the overseas "
                        "incident.",

                    "region":
                        "world",

                    "categories": [
                        "world",
                    ],

                    "publisher_id":
                        "ndtv",
                },
            ]
        },
        "world",
    )
)


# =========================================================
# TEST 6
# REAL PIPELINE REGRESSION:
# KARNATAKA RAIN + NATIONAL NOISE
#
# A genuine Karnataka event should not become national
# simply because another article carries national metadata.
# =========================================================

tests.append(
    test(
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

                    "region":
                        None,

                    "feed_region":
                        "karnataka",

                    "categories": [
                        "state",
                        "local",
                    ],

                    "publisher_id":
                        "tv9_kannada",
                },
                {
                    "title":
                        "Heavy rain alert issued "
                        "across Karnataka",

                    "summary":
                        "Several districts of "
                        "Karnataka may receive "
                        "heavy rainfall.",

                    # Deliberately noisy metadata.
                    "region":
                        "national",

                    "categories": [
                        "national",
                    ],

                    "publisher_id":
                        "hindustan_times",
                },
            ]
        },
        "preferred_state",
    )
)


# =========================================================
# TEST 7
# REAL PIPELINE REGRESSION:
# ENGLAND CRICKET + NATIONAL NOISE
#
# England cricket is a foreign event for geography
# classification. One noisy national article must not
# convert the cluster to Indian national news.
# =========================================================

tests.append(
    test(
        "England cricket cluster with national noise",
        {
            "articles": [
                {
                    "title":
                        "Fleming named new England "
                        "Test coach with Root captain",

                    "summary":
                        "England announce changes "
                        "to their Test cricket setup.",

                    "region":
                        "world",

                    "categories": [
                        "world",
                        "sports",
                        "cricket",
                    ],

                    "publisher_id":
                        "bbc",
                },
                {
                    "title":
                        "England make major Test "
                        "cricket changes",

                    "summary":
                        "England's Test team gets "
                        "a new coaching setup.",

                    # Deliberately noisy metadata.
                    "region":
                        "national",

                    "categories": [
                        "sports",
                        "cricket",
                    ],

                    "publisher_id":
                        "hindustan_times",
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
print("SUMMARY")
print("==============================")

passed = sum(tests)
failed = len(tests) - passed

print(
    f"PASSED: {passed}/{len(tests)}"
)

print(
    f"FAILED: {failed}/{len(tests)}"
)


# =========================================================
# FINAL
# =========================================================

if passed == len(tests):

    print(
        "\nALL STORY GEOGRAPHY "
        "TESTS PASSED"
    )

else:

    print(
        "\nSTORY GEOGRAPHY "
        "REGRESSION DETECTED"
    )

    raise SystemExit(1)