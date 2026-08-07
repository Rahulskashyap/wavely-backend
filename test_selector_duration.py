from news_v4.selector import (
    select_master_episode,
    MIN_DURATION_MINUTES,
    TARGET_DURATION_MINUTES,
    MAX_DURATION_MINUTES,
)


# =========================================================
# REALISTIC UNIQUE STORY TITLES
# =========================================================

STORY_TITLES = {
    "preferred_state": [
        "Karnataka cabinet approves major Bengaluru transport expansion",
        "Bengaluru Metro announces airport corridor construction milestone",
        "Karnataka government launches statewide irrigation modernization plan",
        "Mysuru receives major urban infrastructure development package",
        "Karnataka education department announces university reform programme",
        "Bengaluru technology sector reports major artificial intelligence investment",
        "Karnataka power department approves renewable energy expansion project",
        "Mangaluru port announces major cargo infrastructure development",
        "Karnataka health department launches statewide hospital modernization plan",
        "Bengaluru civic body announces major flood prevention infrastructure project",
        "Hubballi Dharwad transport network receives major expansion approval",
        "Karnataka agriculture department announces farmer support programme",
        "Shivamogga airport receives new regional connectivity expansion",
        "Karnataka industries department announces manufacturing investment programme",
        "Bengaluru suburban rail project reaches major construction milestone",
    ],

    "national": [
        "Union cabinet approves major national infrastructure policy",
        "Reserve Bank of India announces important monetary policy decision",
        "Parliament passes major national technology legislation",
        "Supreme Court delivers major constitutional ruling",
        "India announces nationwide renewable energy expansion programme",
        "Central government unveils major railway modernization plan",
        "India launches new national artificial intelligence initiative",
        "Election Commission announces important electoral reform measures",
        "National highway programme receives major government expansion",
        "India announces major semiconductor manufacturing investment",
        "Union government introduces nationwide education reform programme",
        "Indian economy records major quarterly growth development",
        "Central government announces national healthcare expansion",
        "India launches major satellite mission from Sriharikota",
        "Parliament debates major national cybersecurity legislation",
        "Government announces nationwide electric mobility programme",
        "India introduces major agricultural modernization initiative",
        "National disaster authority announces new emergency preparedness programme",
    ],

    "other_state": [
        "Tamil Nadu announces major industrial investment project",
        "Maharashtra cabinet approves Mumbai transport expansion",
        "Kerala launches major coastal infrastructure programme",
        "Telangana announces Hyderabad technology investment initiative",
        "Andhra Pradesh approves major power transmission project",
        "Gujarat announces large renewable energy development",
        "Rajasthan launches major water infrastructure programme",
        "Odisha announces new industrial development corridor",
        "Punjab government approves agriculture modernization programme",
        "West Bengal announces major Kolkata transport project",
    ],

    "world": [
        "European leaders announce major international security agreement",
        "Global markets react to major central bank policy decision",
        "United States announces significant technology regulation",
        "Japan launches major lunar exploration mission",
        "European Union approves major artificial intelligence legislation",
        "International ceasefire agreement announced after diplomatic talks",
        "Major earthquake triggers emergency response across coastal region",
        "Global energy markets react to major supply disruption",
        "International space mission reaches major scientific milestone",
        "World leaders announce major climate finance agreement",
        "Major cybersecurity attack disrupts international infrastructure",
        "Global trade negotiations produce major tariff agreement",
    ],
}


# =========================================================
# STORY FACTORY
# =========================================================

def make_story(
    number,
    scope,
    score,
    category,
    title,
):
    return {
        "title": title,

        "ranking_score": score,

        # Explicitly include the new ranking field.
        "newsworthiness_score": 12,

        "confidence": "high",

        "independent_source_count": 4,

        "has_primary_source": False,

        "claim_status": "agreement",

        "claim_verification": {
            "agreement_count": 2,
            "partial_count": 0,
            "conflict_count": 0,
            "insufficient_count": 0,
        },

        "serious_conflict": False,

        "sources": [
            {
                "name": f"Source {i}",
                "url": (
                    f"https://example.com/"
                    f"{number}/{i}"
                ),
            }
            for i in range(1, 5)
        ],

        "articles": [
            {
                "title": title,
                "categories": [
                    category
                ],
            }
        ],
    }


# =========================================================
# BUILD RANKED SECTIONS
# =========================================================

ranked_sections = {
    "preferred_state": [],
    "national": [],
    "other_state": [],
    "world": [],
}


story_number = 1


def add_stories(
    scope,
    count,
    start_score,
    category,
):
    global story_number

    titles = STORY_TITLES[
        scope
    ]

    if count > len(titles):
        raise ValueError(
            f"Not enough unique titles "
            f"for {scope}"
        )

    for i in range(count):

        ranked_sections[
            scope
        ].append(
            make_story(
                story_number,
                scope,
                start_score - i,
                category,
                titles[i],
            )
        )

        story_number += 1


# =========================================================
# ADD TEST CANDIDATES
# =========================================================

add_stories(
    "preferred_state",
    15,
    95,
    "state",
)

add_stories(
    "national",
    18,
    94,
    "national",
)

add_stories(
    "other_state",
    10,
    85,
    "state",
)

add_stories(
    "world",
    12,
    90,
    "world",
)


# =========================================================
# SELECT MASTER EPISODE
# =========================================================

master = select_master_episode(
    ranked_sections
)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n==============================")
print("DURATION TEST")
print("==============================")

print(
    "SELECTED:",
    master["story_count"],
)

print(
    "ESTIMATED:",
    master[
        "estimated_duration_minutes"
    ],
    "minutes",
)

print(
    "MINIMUM:",
    MIN_DURATION_MINUTES,
)

print(
    "TARGET:",
    TARGET_DURATION_MINUTES,
)

print(
    "MAXIMUM:",
    MAX_DURATION_MINUTES,
)


# =========================================================
# SECTION COUNTS
# =========================================================

print("\n==============================")
print("SECTION COUNTS")
print("==============================")

section_counts = {
    "preferred_state": 0,
    "national": 0,
    "other_state": 0,
    "world": 0,
}

for story in master["stories"]:

    scope = story[
        "geography_scope"
    ]

    section_counts[
        scope
    ] += 1


for scope, count in (
    section_counts.items()
):
    print(
        scope,
        ":",
        count,
    )


# =========================================================
# DUPLICATE CHECK
# =========================================================

titles = [
    story["title"]
    for story in master["stories"]
]

unique_titles = set(
    titles
)

no_exact_duplicates = (
    len(titles)
    == len(unique_titles)
)


# =========================================================
# RESULT
# =========================================================

print("\n==============================")
print("RESULT")
print("==============================")

duration = master[
    "estimated_duration_minutes"
]


if (
    MIN_DURATION_MINUTES
    <= duration
    <= MAX_DURATION_MINUTES
):

    print(
        "PASS: DURATION WITHIN "
        "35-42 MINUTE RANGE"
    )

else:

    print(
        "FAIL: DURATION OUTSIDE "
        "35-42 MINUTE RANGE"
    )


if master[
    "language_independent"
]:

    print(
        "PASS: SAME MASTER FOR "
        "ALL LANGUAGES"
    )

else:

    print(
        "FAIL: MASTER IS "
        "LANGUAGE DEPENDENT"
    )


if no_exact_duplicates:

    print(
        "PASS: NO EXACT DUPLICATE "
        "STORIES"
    )

else:

    print(
        "FAIL: DUPLICATE STORIES "
        "FOUND"
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

all_passed = (
    MIN_DURATION_MINUTES
    <= duration
    <= MAX_DURATION_MINUTES

    and master[
        "language_independent"
    ]

    and no_exact_duplicates
)


print("\n==============================")
print("FINAL")
print("==============================")


if all_passed:

    print(
        "ALL MASTER EPISODE "
        "TESTS PASSED"
    )

else:

    print(
        "MASTER EPISODE TEST "
        "FAILED"
    )