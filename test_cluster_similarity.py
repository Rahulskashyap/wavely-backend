from news_v4.clusterer import (
    calculate_title_similarity,
    calculate_content_similarity,
    event_keyword_overlap,
    calculate_similarity,
    calculate_semantic_similarity,
    same_event,
)


articles = [
    {
        "name": "BBC",
        "title": "Salman Rushdie attacker convicted of terror offences",
        "summary": "",
        "categories": ["world"],
    },
    {
        "name": "Indian Express",
        "title": "Salman Rushdie stabbing convict terror charge",
        "summary": "",
        "categories": ["world"],
    },
    {
        "name": "Hindustan Times",
        "title": (
            "Salman Rushdie's stabbing suspect Hadi Matar "
            "convicted in New York terrorism trial"
        ),
        "summary": "",
        "categories": ["world"],
    },
    {
        "name": "NDTV",
        "title": (
            "Author Salman Rushdie's attacker Hadi Matar "
            "convicted on terrorism charges"
        ),
        "summary": "",
        "categories": ["world"],
    },
]


def compare(a, b):
    print("\n========================================")
    print(a["name"], "VS", b["name"])
    print("========================================")

    print(
        "TITLE:",
        round(calculate_title_similarity(a, b), 2),
    )

    print(
        "CONTENT:",
        round(calculate_content_similarity(a, b), 2),
    )

    print(
        "KEYWORD OVERLAP:",
        round(event_keyword_overlap(a, b), 3),
    )

    print(
        "LEXICAL:",
        round(calculate_similarity(a, b), 2),
    )

    print(
        "SEMANTIC:",
        round(calculate_semantic_similarity(a, b), 3),
    )

    print(
        "SAME EVENT:",
        same_event(a, b),
    )


for i in range(len(articles)):
    for j in range(i + 1, len(articles)):
        compare(
            articles[i],
            articles[j],
        )