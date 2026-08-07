from news_v4.geographic_ranker import organize_stories


def make_story(
    title,
    region,
    confidence="medium",
):
    article = {
        "title": title,
        "summary": "",
        "canonical_title": title,
        "canonical_summary": "",
        "region": region,
    }

    return {
        "title": title,
        "confidence": confidence,
        "independent_source_count": 2,
        "has_primary_source": False,
        "claim_status": "agreement",
        "articles": [article],
    }


stories = [
    make_story(
        "Bengaluru announces new metro expansion",
        "karnataka",
    ),

    make_story(
        "Chennai receives heavy rainfall",
        "tamil_nadu",
    ),

    make_story(
        "India announces new national technology policy",
        "india",
    ),

    make_story(
        "European leaders meet for major summit",
        "world",
    ),
]


sections = organize_stories(
    stories,
    preferred_state="maharashtra",
)


print("\n==============================")
print("PREFERRED STATE")
print("==============================")

for story in sections["preferred_state"]:
    print(story["title"])


print("\n==============================")
print("OTHER STATES")
print("==============================")

for story in sections["other_state"]:
    print(story["title"])


print("\n==============================")
print("NATIONAL")
print("==============================")

for story in sections["national"]:
    print(story["title"])


print("\n==============================")
print("WORLD")
print("==============================")

for story in sections["world"]:
    print(story["title"])