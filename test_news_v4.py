from news_v4.collector import collect_all_news
from news_v4.canonicalizer import canonicalize_articles
from news_v4.clusterer import cluster_articles
from news_v4.verifier import verify_clusters
from news_v4.geographic_ranker import organize_stories
from news_v4.story_ranker import rank_stories
from news_v4.selector import select_master_episode
from news_v4.category_classifier import classify_articles

def main():
    print("\n==============================")
    print("WAVELY NEWS V4 TEST")
    print("==============================\n")

    # =====================================================
    # 1. COLLECT NEWS
    # =====================================================

    articles = collect_all_news()

    print("\nCollected:", len(articles))

    # =====================================================
    # 2. CANONICALIZE MULTILINGUAL NEWS
    # =====================================================

    articles = canonicalize_articles(
        articles
    )
    # =====================================================
# 3. CLASSIFY ARTICLE TOPICS
# =====================================================

    articles = classify_articles(
    articles
)

    # =====================================================
    # 3. CLUSTER SAME EVENTS
    # =====================================================

    clusters = cluster_articles(
        articles
    )

    print(
        "Story clusters:",
        len(clusters),
    )

    # =====================================================
    # 4. VERIFY CLUSTERS
    # =====================================================

    verified = verify_clusters(
        clusters
    )

    # =====================================================
    # 5. GEOGRAPHIC PERSONALIZATION
    # =====================================================

    preferred_state = "karnataka"

    sections = organize_stories(
        verified,
        preferred_state=preferred_state,
    )

    print("\n==============================")
    print("GEOGRAPHIC PERSONALIZATION")
    print("==============================")

    print(
        "PREFERRED STATE:",
        len(sections["preferred_state"]),
    )

    print(
        "OTHER STATES:",
        len(sections["other_state"]),
    )

    print(
        "NATIONAL:",
        len(sections["national"]),
    )

    print(
        "WORLD:",
        len(sections["world"]),
    )

    geographic_total = sum(
        len(section)
        for section in sections.values()
    )

    print(
        "TOTAL GEOGRAPHIC STORIES:",
        geographic_total,
    )

    print(
        "MATCHES VERIFIED TOTAL:",
        geographic_total == len(verified),
    )

    # =====================================================
    # 6. VERIFICATION SUMMARY
    # =====================================================

    high = [
        story
        for story in verified
        if story["confidence"] == "high"
    ]

    medium = [
        story
        for story in verified
        if story["confidence"] == "medium"
    ]

    low = [
        story
        for story in verified
        if story["confidence"] == "low"
    ]

    multi_source = [
        story
        for story in verified
        if story["independent_source_count"] >= 2
    ]

    conflicts = [
        story
        for story in verified
        if story.get("claim_status") == "conflict"
    ]

    print("\n==============================")
    print("VERIFICATION SUMMARY")
    print("==============================")

    print("HIGH:", len(high))
    print("MEDIUM:", len(medium))
    print("LOW:", len(low))

    print(
        "MULTI-SOURCE STORIES:",
        len(multi_source),
    )

    print(
        "CONFLICT STORIES:",
        len(conflicts),
    )

    # =====================================================
    # 7. RANK STORIES
    # =====================================================

    ranked_sections = rank_stories(
        sections
    )

    print("\n==============================")
    print("RANKING COMPLETE")
    print("==============================")

    for scope in [
        "preferred_state",
        "national",
        "other_state",
        "world",
    ]:
        print(
            scope.upper(),
            ":",
            len(ranked_sections[scope]),
        )

    # =====================================================
    # 8. BUILD LANGUAGE-INDEPENDENT MASTER EPISODE
    # =====================================================

    master = select_master_episode(
        ranked_sections
    )

    print("\n==============================")
    print("MASTER EPISODE")
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
        "MINIMUM DURATION:",
        master["minimum_duration_minutes"],
        "minutes",
    )

    print(
        "TARGET DURATION:",
        master["target_duration_minutes"],
        "minutes",
    )

    print(
        "MAXIMUM DURATION:",
        master["maximum_duration_minutes"],
        "minutes",
    )

    print(
        "LANGUAGE INDEPENDENT:",
        master["language_independent"],
    )

    # =====================================================
    # 9. MASTER EPISODE SECTION COUNTS
    # =====================================================

    section_counts = {
        "preferred_state": 0,
        "national": 0,
        "other_state": 0,
        "world": 0,
    }

    strong_count = 0
    limited_count = 0

    for story in master["stories"]:

        scope = story.get(
            "geography_scope"
        )

        if scope in section_counts:
            section_counts[scope] += 1

        tier = story.get(
            "verification_tier"
        )

        if tier == "strong":
            strong_count += 1

        elif tier == "limited":
            limited_count += 1

    print("\n==============================")
    print("MASTER EPISODE BREAKDOWN")
    print("==============================")

    print(
        "PREFERRED STATE:",
        section_counts["preferred_state"],
    )

    print(
        "NATIONAL:",
        section_counts["national"],
    )

    print(
        "OTHER STATES:",
        section_counts["other_state"],
    )

    print(
        "WORLD:",
        section_counts["world"],
    )

    print(
        "STRONG STORIES:",
        strong_count,
    )

    print(
        "LIMITED STORIES:",
        limited_count,
    )

    # =====================================================
    # 10. DISPLAY SELECTED MASTER STORIES
    # =====================================================

    print("\n==============================")
    print("SELECTED MASTER STORIES")
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
            "GEOGRAPHY:",
            story["geography_scope"],
        )

        print(
            "CATEGORIES:",
            ", ".join(
                story.get(
                    "categories",
                    []
                )
            ),
        )

        print(
            "TIER:",
            story["verification_tier"],
        )

        print(
            "CONFIDENCE:",
            story.get(
                "confidence",
                "unknown",
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
            "SCORE:",
            story.get(
                "ranking_score",
                0,
            ),
        )

        print(
            "PLANNED DURATION:",
            story.get(
                "planned_duration_seconds",
                0,
            ),
            "seconds",
        )

        print(
            "BREAKDOWN:",
            story.get(
                "ranking_components",
                {},
            ),
        )

    # =====================================================
    # 11. FINAL SAFETY CHECKS
    # =====================================================

    selected_conflicts = [
        story
        for story in master["stories"]
        if (
            story.get("serious_conflict")
            or story.get("claim_status")
            == "conflict"
        )
    ]

    print("\n==============================")
    print("FINAL CHECKS")
    print("==============================")

    print(
        "CONFLICT STORIES SELECTED:",
        len(selected_conflicts),
    )

    if selected_conflicts:
        print(
            "FAIL: CONFLICT STORIES "
            "ENTERED MASTER EPISODE"
        )
    else:
        print(
            "PASS: NO CONFLICT STORIES "
            "SELECTED"
        )

    duration = master[
        "estimated_duration_minutes"
    ]

    if (
        master["minimum_duration_minutes"]
        <= duration
        <= master["maximum_duration_minutes"]
    ):
        print(
            "PASS: PLANNED DURATION "
            "WITHIN RANGE"
        )
    else:
        print(
            "WARNING: PLANNED DURATION "
            "OUTSIDE RANGE"
        )

    if master["language_independent"]:
        print(
            "PASS: ONE MASTER EPISODE "
            "FOR ALL LANGUAGES"
        )
    else:
        print(
            "FAIL: MASTER EPISODE "
            "IS LANGUAGE DEPENDENT"
        )


if __name__ == "__main__":
    main()