from news_v4.selector import select_master_episode


def make_story(
    title,
    score,
    confidence,
    sources,
    claim_status,
    scope,
    conflict=False,
    categories=None,
):
    articles = [
        {
            "title": title,
            "categories": categories or ["general"],
        }
    ]

    source_list = [
        {
            "name": f"Source {i + 1}",
            "url": f"https://example.com/{i + 1}",
        }
        for i in range(sources)
    ]

    return {
        "title": title,
        "ranking_score": score,
        "confidence": confidence,
        "independent_source_count": sources,
        "has_primary_source": False,
        "claim_status": claim_status,
        "claim_verification": {
            "agreement_count": 1
            if claim_status == "agreement"
            else 0,
            "partial_count": 1
            if claim_status == "partial"
            else 0,
            "conflict_count": 1
            if conflict
            else 0,
            "insufficient_count": 0,
        },
        "serious_conflict": conflict,
        "geography_scope": scope,
        "sources": source_list,
        "articles": articles,
    }


ranked_sections = {
    "preferred_state": [
        make_story(
            "Karnataka government announces major infrastructure project",
            95,
            "high",
            4,
            "agreement",
            "preferred_state",
            categories=["state"],
        ),
        make_story(
            "Bengaluru receives new public transport update",
            82,
            "medium",
            2,
            "agreement",
            "preferred_state",
            categories=["state"],
        ),
        make_story(
            "Local Karnataka development reported by one outlet",
            58,
            "low",
            1,
            "insufficient",
            "preferred_state",
            categories=["local"],
        ),
    ],

    "national": [
        make_story(
            "India announces major national policy decision",
            92,
            "high",
            4,
            "agreement",
            "national",
            categories=["national"],
        ),
        make_story(
            "Important Indian economy update announced today",
            84,
            "medium",
            3,
            "partial",
            "national",
            categories=["economy"],
        ),
        make_story(
            "Conflicting reports emerge about major national event",
            99,
            "high",
            4,
            "conflict",
            "national",
            conflict=True,
            categories=["national"],
        ),
    ],

    "other_state": [
        make_story(
            "Tamil Nadu announces major development project",
            75,
            "medium",
            2,
            "agreement",
            "other_state",
            categories=["state"],
        ),
    ],

    "world": [
        make_story(
            "Major international development reported by global outlets",
            88,
            "high",
            4,
            "agreement",
            "world",
            categories=["world"],
        ),
        make_story(
            "International update currently reported by one source",
            52,
            "low",
            1,
            "insufficient",
            "world",
            categories=["world"],
        ),
    ],
}


master = select_master_episode(
    ranked_sections
)


print("\n==============================")
print("WAVELY MASTER EPISODE TEST")
print("==============================")

print(
    "STORIES:",
    master["story_count"],
)

print(
    "ESTIMATED DURATION:",
    master["estimated_duration_minutes"],
    "minutes",
)

print(
    "LANGUAGE INDEPENDENT:",
    master["language_independent"],
)


print("\n==============================")
print("SELECTED STORIES")
print("==============================")

for story in master["stories"]:

    print("\n------------------------------")

    print(
        "ORDER:",
        story["episode_order"],
    )

    print(
        "TITLE:",
        story["title"],
    )

    print(
        "SCOPE:",
        story["geography_scope"],
    )

    print(
        "TIER:",
        story["verification_tier"],
    )

    print(
        "SCORE:",
        story["ranking_score"],
    )

    print(
        "PLANNED:",
        story["planned_duration_seconds"],
        "seconds",
    )


print("\n==============================")
print("SAFETY CHECK")
print("==============================")

selected_titles = {
    story["title"]
    for story in master["stories"]
}

conflict_title = (
    "Conflicting reports emerge "
    "about major national event"
)

if conflict_title in selected_titles:
    print("FAIL: CONFLICT STORY SELECTED")
else:
    print("PASS: CONFLICT STORY REJECTED")


limited = [
    story
    for story in master["stories"]
    if story["verification_tier"]
    == "limited"
]

print(
    "LIMITED STORIES:",
    len(limited),
)

print(
    "MASTER MANIFEST:",
    "PASS"
    if master["language_independent"]
    else "FAIL",
)