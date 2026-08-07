from news_v4.collector import collect_all_news
from news_v4.canonicalizer import canonicalize_articles
from news_v4.category_classifier import classify_articles
from news_v4.clusterer import cluster_articles
from news_v4.verifier import verify_clusters
from news_v4.geographic_ranker import organize_stories
from news_v4.story_ranker import rank_stories
from news_v4.selector import select_master_episode


# =========================================================
# WAVELY NEWS V4 PIPELINE
# =========================================================

def build_master_episode(
    preferred_state="karnataka",
):
    """
    Run the complete Wavely News V4 pipeline and return
    one language-independent master episode.

    Pipeline:

        collect
        -> canonicalize
        -> classify topics
        -> cluster events
        -> verify clusters
        -> organize geography
        -> rank stories
        -> select master episode
    """

    print("\n========================================")
    print("WAVELY NEWS V4 PIPELINE")
    print("========================================")

    # =====================================================
    # 1. COLLECT
    # =====================================================

    articles = collect_all_news()

    print(
        "\nCollected articles:",
        len(articles),
    )

    if not articles:
        raise RuntimeError(
            "Wavely V4 collected no news articles."
        )

    # =====================================================
    # 2. CANONICALIZE
    # =====================================================

    articles = canonicalize_articles(
        articles
    )

    # =====================================================
    # 3. CLASSIFY TOPICS
    # =====================================================

    articles = classify_articles(
        articles
    )

    # =====================================================
    # 4. CLUSTER SAME EVENTS
    # =====================================================

    clusters = cluster_articles(
        articles
    )

    print(
        "\nStory clusters:",
        len(clusters),
    )

    if not clusters:
        raise RuntimeError(
            "Wavely V4 produced no story clusters."
        )

    # =====================================================
    # 5. VERIFY
    # =====================================================

    verified = verify_clusters(
        clusters
    )

    print(
        "Verified stories:",
        len(verified),
    )

    if not verified:
        raise RuntimeError(
            "Wavely V4 produced no verified stories."
        )

    # =====================================================
    # 6. GEOGRAPHIC PERSONALIZATION
    # =====================================================

    sections = organize_stories(
        verified,
        preferred_state=preferred_state,
    )

    geographic_total = sum(
        len(stories)
        for stories in sections.values()
    )

    if geographic_total != len(verified):
        raise RuntimeError(
            "Geographic organization lost or "
            "duplicated stories."
        )

    print("\nGEOGRAPHIC SECTIONS")

    for scope in (
        "preferred_state",
        "national",
        "other_state",
        "world",
    ):
        print(
            f"{scope}:",
            len(
                sections.get(
                    scope,
                    [],
                )
            ),
        )

    # =====================================================
    # 7. RANK
    # =====================================================

    ranked_sections = rank_stories(
        sections
    )

    # =====================================================
    # 8. SELECT MASTER EPISODE
    # =====================================================

    master = select_master_episode(
        ranked_sections
    )

    # =====================================================
    # 9. BASIC PRODUCTION SAFETY
    # =====================================================

    stories = master.get(
        "stories",
        [],
    )

    if not stories:
        raise RuntimeError(
            "Wavely V4 selected no stories."
        )

    selected_conflicts = [
        story
        for story in stories
        if (
            story.get(
                "serious_conflict"
            )
            or story.get(
                "claim_status"
            ) == "conflict"
        )
    ]

    if selected_conflicts:
        raise RuntimeError(
            "Wavely V4 master episode contains "
            "a conflicting story."
        )

    # =====================================================
    # 10. PIPELINE SUMMARY
    # =====================================================

        print("\n========================================")
    print("V4 MASTER READY")
    print("========================================")

    print(
        "Stories:",
        master.get(
            "story_count",
            len(stories),
        ),
    )

    print(
        "Duration:",
        master.get(
            "estimated_duration_minutes",
            0,
        ),
        "minutes",
    )

    print(
        "Language independent:",
        master.get(
            "language_independent",
            False,
        ),
    )

    # =====================================================
    # DEBUG — SELECTED MASTER STORIES
    # =====================================================

    print("\n========================================")
    print("SELECTED V4 MASTER STORIES")
    print("========================================")

    for story in stories:

        print("\n----------------------------------------")

        print(
            "ORDER:",
            story.get("episode_order"),
        )

        print(
            "TITLE:",
            story.get("title"),
        )

        print(
            "SCOPE:",
            story.get("geography_scope"),
        )

        print(
            "CATEGORIES:",
            story.get(
                "categories",
                [],
            ),
        )

        print(
            "DURATION:",
            story.get(
                "planned_duration_seconds",
                0,
            ),
            "seconds",
        )

        print(
            "CONFIDENCE:",
            story.get("confidence"),
        )

        print(
            "CLAIM STATUS:",
            story.get("claim_status"),
        )

        print(
            "SOURCES:",
            story.get(
                "independent_source_count",
                0,
            ),
        )

        print("SOURCE ARTICLES:")

        for article in story.get(
            "articles",
            [],
        ):

            print(
                "  -",
                article.get("publisher_id"),
                "|",
                article.get("canonical_title")
                or article.get("title"),
            )

    return master

# =========================================================
# OPTIONAL DIRECT TEST
# =========================================================

if __name__ == "__main__":

    result = build_master_episode(
        preferred_state="karnataka",
    )

    print(
        "\nPipeline completed successfully."
    )

    print(
        "Selected stories:",
        result.get(
            "story_count",
            0,
        ),
    )