from news_v4.geo_classifier import classify_geography


def run_test(
    name,
    article,
    expected,
    preferred_state="karnataka",
):
    result = classify_geography(
        article,
        preferred_state=preferred_state,
    )

    actual = result["scope"]

    passed = actual == expected

    print("\n------------------------------")
    print("TEST:", name)
    print("TITLE:", article["title"])
    print("REGION:", article.get("region"))
    print("FEED REGION:", article.get("feed_region"))
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)
    print("STATES:", result.get("states", []))
    print("EVIDENCE:", result.get("evidence"))
    print(
        "RESULT:",
        "PASS" if passed else "FAIL",
    )

    return passed


tests = []


# =========================================================
# 1. INTERNATIONAL STORY FROM KARNATAKA FEED
# =========================================================

tests.append(
    run_test(
        "Egypt story from Karnataka feed",
        {
            "title":
                "US LNG tanker attacked at Egypt port",

            "summary":
                "The tanker was attacked while "
                "docked at a port in Egypt.",

            "region": None,
            "feed_region": "karnataka",

            "categories": [
                "world",
            ],

            "language": "kn",
            "publisher_id": "tv9_kannada",
        },
        "world",
    )
)


# =========================================================
# 2. AYODHYA STORY FROM KARNATAKA FEED
# =========================================================

tests.append(
    run_test(
        "Ayodhya story from Karnataka feed",
        {
            "title":
                "Ayodhya mosque project gets new update",

            "summary":
                "A new development has been announced "
                "regarding the Ayodhya mosque project "
                "in India.",

            "region": None,
            "feed_region": "karnataka",

            "categories": [
                "national",
            ],

            "language": "kn",
            "publisher_id": "kannada_oneindia",
        },
        "other_state",
    )
)


# =========================================================
# 3. ANDHRA PRADESH FROM KARNATAKA FEED
# =========================================================

tests.append(
    run_test(
        "Andhra Pradesh story",
        {
            "title":
                "Andhra Pradesh announces major "
                "transmission project",

            "summary":
                "The state approved a major power "
                "transmission project.",

            "region": None,
            "feed_region": "karnataka",

            "categories": [
                "state",
            ],

            "language": "kn",
            "publisher_id": "kannada_oneindia",
        },
        "other_state",
    )
)


# =========================================================
# 4. GADAG LOCAL STORY
#
# No explicit Karnataka word is necessary if Gadag is
# present in STATE_KEYWORDS for Karnataka.
# =========================================================

tests.append(
    run_test(
        "Gadag local story",
        {
            "title":
                "Heavy rainfall affects several "
                "areas of Gadag",

            "summary":
                "Residents faced disruption following "
                "heavy rain.",

            "region": None,
            "feed_region": "karnataka",

            "categories": [
                "state",
                "local",
            ],

            "language": "kn",
            "publisher_id": "public_tv",
        },
        "preferred_state",
    )
)


# =========================================================
# 5. BALLARI LOCAL STORY
# =========================================================

tests.append(
    run_test(
        "Ballari local story",
        {
            "title":
                "New development project announced "
                "in Ballari",

            "summary":
                "Local authorities announced details "
                "of the project.",

            "region": None,
            "feed_region": "karnataka",

            "categories": [
                "state",
                "local",
            ],

            "language": "kn",
            "publisher_id": "tv9_kannada",
        },
        "preferred_state",
    )
)

# =========================================================
# 6. MULTI-STATE STORY
#
# Karnataka is mentioned, but the story covers several
# Indian states/cities. It must be NATIONAL, not
# preferred_state.
# =========================================================

tests.append(
    run_test(
        "Multi-state gold price story",
        {
            "title":
                "Gold prices today in Bengaluru, "
                "Mumbai, Chennai and Delhi",

            "summary":
                "Gold rates were updated across "
                "major Indian cities including "
                "Bengaluru, Mumbai, Chennai and Delhi.",

            "region": None,
            "feed_region": None,

            "categories": [
                "national",
            ],

            "language": "en",
            "publisher_id": "test_source",
        },
        "national",
    )
)


# =========================================================
# SUMMARY
# =========================================================

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
        "\nALL FEED REGION TESTS PASSED"
    )
else:
    print(
        "\nSOME FEED REGION TESTS FAILED"
    )