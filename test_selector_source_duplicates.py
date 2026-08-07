from news_v4.selector import (
    is_duplicate_event,
    duplicate_of_selected,
)


def run_test(
    name,
    story_a,
    story_b,
    expected,
):
    actual = is_duplicate_event(
        story_a,
        story_b,
    )

    passed = actual == expected

    print("\n------------------------------")
    print("TEST:", name)
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)
    print(
        "RESULT:",
        "PASS" if passed else "FAIL",
    )

    return passed


tests = []


# =========================================================
# TEST 1
# SAME SOURCE ARTICLE, DIFFERENT STORY TITLES
#
# This reproduces the real V4 failure:
# two story objects contain the same underlying article,
# but their master titles are worded differently.
# =========================================================

tests.append(
    run_test(
        "Same source article with different story titles",
        {
            "title":
                "Vinay Kulkarni faces development "
                "in Yogesh Gowda murder case",

            "articles": [
                {
                    "publisher_id":
                        "indian_express",

                    "title":
                        "Court gives new order in "
                        "Yogesh Gowda murder case",

                    "url":
                        "https://example.com/"
                        "yogesh-gowda-case",
                },
            ],
        },
        {
            "title":
                "Former minister receives court "
                "relief in murder case",

            "articles": [
                {
                    "publisher_id":
                        "indian_express",

                    "title":
                        "Court gives new order in "
                        "Yogesh Gowda murder case",

                    "url":
                        "https://example.com/"
                        "yogesh-gowda-case",
                },
            ],
        },
        True,
    )
)


# =========================================================
# TEST 2
# SAME PUBLISHER + SAME ARTICLE TITLE, NO URL
# =========================================================

tests.append(
    run_test(
        "Same source article without URL",
        {
            "title":
                "Karnataka rain alert issued",

            "articles": [
                {
                    "publisher_id":
                        "public_tv",

                    "canonical_title":
                        "Heavy rain alert issued "
                        "across Karnataka",
                },
            ],
        },
        {
            "title":
                "Several Karnataka districts "
                "prepare for rainfall",

            "articles": [
                {
                    "publisher_id":
                        "public_tv",

                    "canonical_title":
                        "Heavy rain alert issued "
                        "across Karnataka",
                },
            ],
        },
        True,
    )
)


# =========================================================
# TEST 3
# SAME PERSON, DIFFERENT EVENTS
#
# Must NOT become a duplicate simply because the stories
# involve the same person.
# =========================================================

tests.append(
    run_test(
        "Same person but different events",
        {
            "title":
                "Minister announces new "
                "education programme",

            "articles": [
                {
                    "publisher_id":
                        "publisher_a",

                    "title":
                        "Minister launches "
                        "education programme",

                    "url":
                        "https://example.com/"
                        "education-programme",
                },
            ],
        },
        {
            "title":
                "Minister addresses "
                "technology conference",

            "articles": [
                {
                    "publisher_id":
                        "publisher_b",

                    "title":
                        "Minister speaks at "
                        "technology conference",

                    "url":
                        "https://example.com/"
                        "technology-conference",
                },
            ],
        },
        False,
    )
)


# =========================================================
# TEST 4
# COMPLETELY DIFFERENT STORIES
# =========================================================

tests.append(
    run_test(
        "Unrelated stories",
        {
            "title":
                "England announce new "
                "Test cricket coach",

            "articles": [
                {
                    "publisher_id": "bbc",
                    "url":
                        "https://example.com/"
                        "england-cricket",
                },
            ],
        },
        {
            "title":
                "Heavy rainfall hits Bengaluru",

            "articles": [
                {
                    "publisher_id":
                        "public_tv",

                    "url":
                        "https://example.com/"
                        "bengaluru-rain",
                },
            ],
        },
        False,
    )
)


# =========================================================
# TEST 5
# CHECK ACTUAL SELECTED-LIST GUARD
# =========================================================

selected_story = {
    "title":
        "Vinay Kulkarni faces development "
        "in Yogesh Gowda murder case",

    "articles": [
        {
            "publisher_id":
                "indian_express",

            "url":
                "https://example.com/"
                "shared-case",
        },
    ],
}

candidate_story = {
    "title":
        "Former minister gets court "
        "relief in murder case",

    "articles": [
        {
            "publisher_id":
                "indian_express",

            "url":
                "https://example.com/"
                "shared-case",
        },
    ],
}

duplicate = duplicate_of_selected(
    candidate_story,
    [selected_story],
)

test_5_passed = duplicate is selected_story

tests.append(
    test_5_passed
)

print("\n------------------------------")
print("TEST: Selected-list duplicate guard")
print("EXPECTED: duplicate detected")
print(
    "ACTUAL:",
    "duplicate detected"
    if duplicate
    else "not detected",
)
print(
    "RESULT:",
    "PASS"
    if test_5_passed
    else "FAIL",
)


# =========================================================
# SUMMARY
# =========================================================

print("\n==============================")
print("SOURCE DUPLICATE REGRESSION TEST")
print("==============================")

passed = sum(tests)
total = len(tests)

print("PASSED:", passed)
print("FAILED:", total - passed)
print("TOTAL:", total)

if passed == total:
    print(
        "\nALL SOURCE DUPLICATE TESTS PASSED"
    )
else:
    print(
        "\nSOURCE DUPLICATE REGRESSION DETECTED"
    )