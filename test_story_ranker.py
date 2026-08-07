from news_v4.collector import collect_all_news
from news_v4.canonicalizer import canonicalize_articles
from news_v4.clusterer import cluster_articles
from news_v4.verifier import verify_clusters
from news_v4.geographic_ranker import organize_stories
from news_v4.story_ranker import rank_stories


def main():

    print("\n==============================")
    print("WAVELY STORY RANKER TEST")
    print("==============================")

    articles = collect_all_news()

    print(
        "\nCollected:",
        len(articles),
    )

    articles = canonicalize_articles(
        articles
    )

    clusters = cluster_articles(
        articles
    )

    print(
        "Clusters:",
        len(clusters),
    )

    verified = verify_clusters(
        clusters
    )

    preferred_state = "karnataka"

    sections = organize_stories(
        verified,
        preferred_state=preferred_state,
    )

    ranked = rank_stories(
        sections
    )

    # -----------------------------------
    # DISPLAY TOP STORIES
    # -----------------------------------

    for scope in [
        "preferred_state",
        "other_state",
        "national",
        "world",
    ]:

        print(
            "\n=============================="
        )

        print(
            scope.upper()
        )

        print(
            "=============================="
        )

        stories = ranked.get(
            scope,
            []
        )

        print(
            "TOTAL:",
            len(stories),
        )

        for story in stories[:10]:

            print(
                "\n------------------------------"
            )

            print(
                "SCORE:",
                story[
                    "ranking_score"
                ],
            )

            print(
                "TITLE:",
                story.get(
                    "title",
                    "",
                ),
            )

            print(
                "CONFIDENCE:",
                story.get(
                    "confidence",
                    "",
                ),
            )

            print(
                "SOURCES:",
                story.get(
                    "independent_source_count",
                    0,
                ),
            )

            print(
                "CLAIM:",
                story.get(
                    "claim_status",
                    "unknown",
                ),
            )

            print(
                "CONFLICT:",
                story.get(
                    "serious_conflict",
                    False,
                ),
            )

            print(
                "BREAKDOWN:",
                story.get(
                    "ranking_components",
                    {},
                ),
            )


if __name__ == "__main__":
    main()