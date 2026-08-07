from collections import Counter

from .geo_classifier import (
    classify_geography,
    normalize_state_name,
)


# =========================================================
# CONFIG
# =========================================================

SCOPES = (
    "preferred_state",
    "national",
    "other_state",
    "world",
)


# Evidence produced by geo_classifier.py that represents
# meaningful state evidence from the actual story.
STRONG_STATE_EVIDENCE = {
    "explicit_story_region",
    "single_state_text",
}


# Feed-region fallback is deliberately weak.
#
# Example:
# A Karnataka RSS feed can contain an Egypt story.
# feed_region therefore must never be treated the same
# as Karnataka being explicitly present in the story.
WEAK_STATE_EVIDENCE = {
    "feed_region_fallback",
}


# Strong world evidence.
STRONG_WORLD_EVIDENCE = {
    "explicit_story_region",
    "world_category",
}


# =========================================================
# BASIC HELPERS
# =========================================================

def unique_values(values):
    """
    Return unique non-empty values while preserving order.
    """

    result = []
    seen = set()

    for value in values:

        if not value:
            continue

        if value in seen:
            continue

        seen.add(value)
        result.append(value)

    return result


def empty_votes():
    return {
        scope: 0
        for scope in SCOPES
    }


def empty_evidence_counts():
    return Counter()


# =========================================================
# ARTICLE CLASSIFICATION
# =========================================================

def classify_articles(
    story,
    preferred_state,
):
    """
    Classify every article independently using
    geo_classifier.py.

    We preserve the evidence field because story-level
    classification needs to know WHY an article received
    a particular geography.
    """

    results = []

    for article in story.get(
        "articles",
        [],
    ):

        classification = (
            classify_geography(
                article,
                preferred_state,
            )
        )

        results.append(
            {
                "article":
                    article,

                "scope":
                    classification.get(
                        "scope",
                        "world",
                    ),

                "states":
                    classification.get(
                        "states",
                        [],
                    ),

                "evidence":
                    classification.get(
                        "evidence",
                        "",
                    ),
            }
        )

    return results


# =========================================================
# VOTE HELPERS
# =========================================================

def count_votes(
    article_results,
):
    votes = empty_votes()

    for result in article_results:

        scope = result.get(
            "scope"
        )

        if scope in votes:
            votes[scope] += 1

    return votes


def count_evidence(
    article_results,
):
    counts = empty_evidence_counts()

    for result in article_results:

        evidence = result.get(
            "evidence",
            "",
        )

        if evidence:
            counts[evidence] += 1

    return counts


def collect_detected_states(
    article_results,
):
    states = []

    for result in article_results:

        states.extend(
            result.get(
                "states",
                [],
            )
        )

    return unique_values(
        states
    )


# =========================================================
# EVIDENCE HELPERS
# =========================================================

def count_scope_with_evidence(
    article_results,
    scope,
    evidence_types,
):
    """
    Count votes for a particular scope only when their
    evidence belongs to evidence_types.
    """

    return sum(
        1
        for result in article_results
        if (
            result.get("scope") == scope
            and result.get("evidence")
            in evidence_types
        )
    )


def count_preferred_text_votes(
    article_results,
):
    """
    Preferred-state votes backed specifically by text.

    This is important for resolving cases where the story
    clearly says Karnataka but another article contains
    noisy national metadata.
    """

    return count_scope_with_evidence(
        article_results,
        "preferred_state",
        {
            "single_state_text",
        },
    )


def count_preferred_explicit_votes(
    article_results,
):
    return count_scope_with_evidence(
        article_results,
        "preferred_state",
        {
            "explicit_story_region",
        },
    )


def count_preferred_strong_votes(
    article_results,
):
    return count_scope_with_evidence(
        article_results,
        "preferred_state",
        STRONG_STATE_EVIDENCE,
    )


def count_preferred_feed_votes(
    article_results,
):
    return count_scope_with_evidence(
        article_results,
        "preferred_state",
        WEAK_STATE_EVIDENCE,
    )


def count_other_state_strong_votes(
    article_results,
):
    return count_scope_with_evidence(
        article_results,
        "other_state",
        STRONG_STATE_EVIDENCE,
    )


def count_world_strong_votes(
    article_results,
):
    return count_scope_with_evidence(
        article_results,
        "world",
        STRONG_WORLD_EVIDENCE,
    )


def count_explicit_scope_votes(
    article_results,
    scope,
):
    return count_scope_with_evidence(
        article_results,
        scope,
        {
            "explicit_story_region",
        },
    )


# =========================================================
# WORLD PROTECTION
# =========================================================

def has_strong_world_evidence(
    article_results,
):
    """
    True when at least one article has explicit world
    geography or a world category.

    Used to stop Indian publisher/feed noise from turning
    foreign events into national stories.
    """

    return (
        count_world_strong_votes(
            article_results
        )
        > 0
    )


# =========================================================
# STORY CLASSIFICATION
# =========================================================

def classify_story(
    story,
    preferred_state,
):
    """
    Classify a clustered story into:

        preferred_state
        national
        other_state
        world

    Important principles:

    1. Feed geography is weak evidence.
    2. Actual article text is stronger than feed context.
    3. One state article cannot hijack a clearly national
       cluster.
    4. A genuine state story can survive one noisy national
       metadata signal.
    5. Foreign stories must not become national merely
       because an Indian source reported them.
    """

    preferred_state = (
        normalize_state_name(
            preferred_state
        )
    )

    article_results = (
        classify_articles(
            story,
            preferred_state,
        )
    )
        # =====================================================
    # DEBUG
    # =====================================================

    print("\n====================")
    print("STORY:", story.get("title"))

    for r in article_results:
        print(
            r["scope"],
            "|",
            r["evidence"],
            "|",
            r["article"].get("publisher_id"),
        )

    # No articles -> safest generic fallback.
    if not article_results:

        return {
            "scope":
                "world",

            "states": [],
        }

    votes = count_votes(
        article_results
    )

    detected_states = (
        collect_detected_states(
            article_results
        )
    )

    preferred_votes = votes[
        "preferred_state"
    ]

    national_votes = votes[
        "national"
    ]

    other_state_votes = votes[
        "other_state"
    ]

    world_votes = votes[
        "world"
    ]

    preferred_text_votes = (
        count_preferred_text_votes(
            article_results
        )
    )

    preferred_explicit_votes = (
        count_preferred_explicit_votes(
            article_results
        )
    )

    preferred_strong_votes = (
        count_preferred_strong_votes(
            article_results
        )
    )

    preferred_feed_votes = (
        count_preferred_feed_votes(
            article_results
        )
    )

    other_state_strong_votes = (
        count_other_state_strong_votes(
            article_results
        )
    )

    strong_world_votes = (
        count_world_strong_votes(
            article_results
        )
    )

    explicit_preferred_votes = (
        count_explicit_scope_votes(
            article_results,
            "preferred_state",
        )
    )

    explicit_national_votes = (
        count_explicit_scope_votes(
            article_results,
            "national",
        )
    )

    explicit_other_state_votes = (
        count_explicit_scope_votes(
            article_results,
            "other_state",
        )
    )

    explicit_world_votes = (
        count_explicit_scope_votes(
            article_results,
            "world",
        )
    )


    # =====================================================
    # RULE 1
    # EXPLICIT REGION MAJORITY
    #
    # If multiple articles explicitly agree on actual
    # geography, trust that consensus first.
    # =====================================================

    explicit_votes = {
        "preferred_state":
            explicit_preferred_votes,

        "national":
            explicit_national_votes,

        "other_state":
            explicit_other_state_votes,

        "world":
            explicit_world_votes,
    }

    explicit_total = sum(
        explicit_votes.values()
    )

    if explicit_total >= 2:

        explicit_winner = max(
            explicit_votes,
            key=explicit_votes.get,
        )

        winner_votes = (
            explicit_votes[
                explicit_winner
            ]
        )

        competing_votes = [
            count
            for scope, count
            in explicit_votes.items()
            if scope != explicit_winner
        ]

        highest_competitor = max(
            competing_votes,
            default=0,
        )

        if (
            winner_votes >= 2
            and winner_votes
            > highest_competitor
        ):

            if (
                explicit_winner
                == "preferred_state"
            ):

                return {
                    "scope":
                        "preferred_state",

                    "states":
                        unique_values(
                            detected_states
                            or [preferred_state]
                        ),
                }

            if (
                explicit_winner
                == "other_state"
            ):

                return {
                    "scope":
                        "other_state",

                    "states":
                        detected_states,
                }

            return {
                "scope":
                    explicit_winner,

                "states": [],
            }


    # =====================================================
    # RULE 2
    # WORLD MAJORITY
    # =====================================================

    if (
        world_votes >= 2
        and world_votes > national_votes
        and world_votes > preferred_votes
        and world_votes > other_state_votes
    ):

        return {
            "scope":
                "world",

            "states": [],
        }


    # =====================================================
    # RULE 3
    # NATIONAL MAJORITY
    #
    # This preserves:
    #
    # 2 national + 1 Karnataka
    # -> national
    # =====================================================

    if (
        national_votes >= 2
        and national_votes > preferred_votes
        and national_votes > other_state_votes
        and national_votes > world_votes
    ):

        return {
            "scope":
                "national",

            "states": [],
        }


    # =====================================================
    # RULE 4
    # OTHER-STATE MAJORITY
    # =====================================================

    if (
        other_state_votes >= 2
        and other_state_votes > national_votes
        and other_state_votes > preferred_votes
        and other_state_votes > world_votes
    ):

        return {
            "scope":
                "other_state",

            "states":
                detected_states,
        }


    # =====================================================
    # RULE 5
    # PREFERRED-STATE MAJORITY
    # =====================================================

    if (
        preferred_votes >= 2
        and preferred_votes > national_votes
        and preferred_votes > world_votes
        and preferred_votes >= other_state_votes
    ):

        return {
            "scope":
                "preferred_state",

            "states":
                unique_values(
                    detected_states
                    or [preferred_state]
                ),
        }


    # =====================================================
    # RULE 6
    # GENUINE PREFERRED-STATE VS NATIONAL TIE
    #
    # This fixes the real regression:
    #
    # Karnataka story text
    #       +
    # one article incorrectly marked national
    #
    # -> preferred_state
    #
    # CRITICAL:
    #
    # feed_region_fallback alone is NOT enough.
    #
    # We require actual state evidence from article text
    # or explicit story-region metadata.
    # =====================================================

    if (
        preferred_votes > 0
        and preferred_votes == national_votes
        and preferred_votes > world_votes
        and preferred_votes >= other_state_votes

        and preferred_strong_votes > 0

        and (
            preferred_text_votes > 0
            or preferred_explicit_votes > 0
        )

        and strong_world_votes == 0

        and other_state_strong_votes == 0
    ):

        return {
            "scope":
                "preferred_state",

            "states":
                unique_values(
                    detected_states
                    or [preferred_state]
                ),
        }


    # =====================================================
    # RULE 7
    # WORLD VS NATIONAL TIE
    #
    # Example:
    #
    # BBC:
    #   England cricket -> world
    #
    # Indian source:
    #   England cricket -> noisy national metadata
    #
    # -> world
    # =====================================================

    if (
        world_votes > 0
        and world_votes == national_votes
        and world_votes >= preferred_votes
        and world_votes >= other_state_votes
        and has_strong_world_evidence(
            article_results
        )
    ):

        return {
            "scope":
                "world",

            "states": [],
        }


    # =====================================================
    # RULE 8
    # STRONG WORLD PROTECTION
    #
    # World evidence should beat weak state/feed evidence
    # when world already has at least as many votes.
    # =====================================================

    if (
        strong_world_votes > 0
        and world_votes >= preferred_votes
        and world_votes >= other_state_votes
        and world_votes >= national_votes
    ):

        return {
            "scope":
                "world",

            "states": [],
        }


    # =====================================================
    # RULE 9
    # PREFERRED STATE WITH STRONG EVIDENCE
    #
    # Allows a single strong preferred-state article when
    # there is no competing national/world/state evidence.
    #
    # Feed fallback is deliberately excluded.
    # =====================================================

    if (
        preferred_votes > 0
        and preferred_strong_votes > 0
        and national_votes == 0
        and world_votes == 0
        and other_state_votes == 0
    ):

        return {
            "scope":
                "preferred_state",

            "states":
                unique_values(
                    detected_states
                    or [preferred_state]
                ),
        }


    # =====================================================
    # RULE 10
    # WEAK FEED-REGION ONLY
    #
    # A feed fallback can classify a story as preferred
    # state only when NOTHING else conflicts with it.
    # =====================================================

    if (
        preferred_votes > 0
        and preferred_votes
        == preferred_feed_votes
        and national_votes == 0
        and world_votes == 0
        and other_state_votes == 0
    ):

        return {
            "scope":
                "preferred_state",

            "states":
                unique_values(
                    detected_states
                    or [preferred_state]
                ),
        }


    # =====================================================
    # RULE 11
    # OTHER STATE WITH NO COMPETING EVIDENCE
    # =====================================================

    if (
        other_state_votes > 0
        and national_votes == 0
        and world_votes == 0
        and preferred_votes == 0
    ):

        return {
            "scope":
                "other_state",

            "states":
                detected_states,
        }


    # =====================================================
    # RULE 12
    # NATIONAL FALLBACK
    #
    # Any unresolved cluster with genuine national votes
    # stays national unless world protection already won.
    # =====================================================

    if national_votes > 0:

        return {
            "scope":
                "national",

            "states": [],
        }


    # =====================================================
    # RULE 13
    # WORLD FALLBACK
    # =====================================================

    if world_votes > 0:

        return {
            "scope":
                "world",

            "states": [],
        }


    # =====================================================
    # RULE 14
    # PREFERRED-STATE FALLBACK
    # =====================================================

    if preferred_votes > 0:

        return {
            "scope":
                "preferred_state",

            "states":
                unique_values(
                    detected_states
                    or [preferred_state]
                ),
        }


    # =====================================================
    # RULE 15
    # OTHER-STATE FALLBACK
    # =====================================================

    if other_state_votes > 0:

        return {
            "scope":
                "other_state",

            "states":
                detected_states,
        }


    # =====================================================
    # RULE 16
    # FINAL FALLBACK
    # =====================================================

    return {
        "scope":
            "world",

        "states": [],
    }
# =========================================================
# ORGANIZE VERIFIED STORIES BY GEOGRAPHY
# =========================================================

def organize_stories(
    stories,
    preferred_state,
):
    """
    Classify every verified story and organize it into
    geographic sections used by the ranking/selection
    pipeline.

    Sections:
        preferred_state
        national
        other_state
        world
    """

    sections = {
        "preferred_state": [],
        "national": [],
        "other_state": [],
        "world": [],
    }

    for story in stories:

        result = classify_story(
            story,
            preferred_state,
        )

        scope = result.get(
            "scope",
            "world",
        )

        states = result.get(
            "states",
            [],
        )

        # Preserve geography on the story itself so later
        # pipeline stages can inspect it.
        story[
            "geography_scope"
        ] = scope

        story[
            "geography_states"
        ] = states

        # Defensive fallback for unexpected scope values.
        if scope not in sections:
            scope = "world"

            story[
                "geography_scope"
            ] = scope

        sections[
            scope
        ].append(
            story
        )

    return sections