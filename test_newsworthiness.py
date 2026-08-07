from news_v4.story_ranker import score_newsworthiness
from news_v4.selector import (
    get_verification_tier,
    is_story_eligible,
)


def make_story(
    title,
    *,
    confidence="medium",
    sources=1,
    primary=False,
    claim_status="insufficient",
):
    return {
        "title": title,
        "confidence": confidence,
        "independent_source_count": sources,
        "has_primary_source": primary,
        "claim_status": claim_status,
        "claim_verification": {
            "agreement_count": 0,
            "partial_count": 0,
            "conflict_count": 0,
        },
        "sources": [
            {
                "name": "Test Source",
                "url": "https://example.com/test",
            }
        ],
        "articles": [
            {
                "title": title,
                "summary": "",
                "categories": [],
            }
        ],
    }


tests = [
    {
        "name": "Major government policy",
        "story": make_story(
            "Government cabinet announces major national policy decision",
            confidence="high",
            sources=3,
            claim_status="agreement",
        ),
        "min_news": 12,
        "tier": "strong",
        "eligible": True,
    },

    {
        "name": "Major security event",
        "story": make_story(
            "Military missile attack triggers emergency evacuation",
            confidence="high",
            sources=4,
            claim_status="agreement",
        ),
        "min_news": 16,
        "tier": "strong",
        "eligible": True,
    },

    {
        "name": "Major space mission",
        "story": make_story(
            "Satellite mission launch faces major spacecraft emergency",
            confidence="high",
            sources=3,
            primary=True,
            claim_status="agreement",
        ),
        "min_news": 16,
        "tier": "strong",
        "eligible": True,
    },

    {
        "name": "Routine NASA APOD",
        "story": make_story(
            "NASA Astronomy Picture of the Day APOD",
            confidence="medium",
            sources=1,
            primary=True,
        ),
        "max_news": -10,
        "tier": "limited",
        "eligible": False,
    },

    {
        "name": "Routine gold price",
        "story": make_story(
            "Gold price today in Bengaluru",
            confidence="medium",
            sources=1,
        ),
        "max_news": -10,
        "tier": "limited",
        "eligible": False,
    },

    {
        "name": "Primary source alone",
        "story": make_story(
            "Official organization publishes routine annual update",
            confidence="medium",
            sources=1,
            primary=True,
        ),
        "tier": "limited",
        "eligible": True,
    },

    {
        "name": "Multi-source verified",
        "story": make_story(
            "Important regional development reported by several outlets",
            confidence="medium",
            sources=3,
            claim_status="agreement",
        ),
        "tier": "strong",
        "eligible": True,
    },

    {
        "name": "Conflict rejected",
        "story": {
            **make_story(
                "Major policy claim disputed by reporting outlets",
                confidence="medium",
                sources=3,
                claim_status="conflict",
            ),
            "serious_conflict": True,
        },
        "tier": "rejected",
        "eligible": False,
    },
]


passed = 0


for test in tests:

    story = test["story"]

    news_score = score_newsworthiness(
        story
    )

    # The real pipeline adds this in story_ranker.
    story["newsworthiness_score"] = (
        news_score
    )

    tier = get_verification_tier(
        story
    )

    eligible = is_story_eligible(
        story
    )

    success = True

    if (
        "min_news" in test
        and news_score
        < test["min_news"]
    ):
        success = False

    if (
        "max_news" in test
        and news_score
        > test["max_news"]
    ):
        success = False

    if tier != test["tier"]:
        success = False

    if eligible != test["eligible"]:
        success = False

    print("\n------------------------------")
    print("TEST:", test["name"])
    print("NEWSWORTHINESS:", news_score)
    print("TIER:", tier)
    print("ELIGIBLE:", eligible)

    print(
        "RESULT:",
        "PASS" if success else "FAIL",
    )

    if success:
        passed += 1


print("\n==============================")
print("SUMMARY")
print("==============================")

print("PASSED:", passed)
print("FAILED:", len(tests) - passed)
print("TOTAL:", len(tests))

if passed == len(tests):
    print(
        "\nALL NEWSWORTHINESS TESTS PASSED"
    )
else:
    print(
        "\nSOME NEWSWORTHINESS TESTS FAILED"
    )