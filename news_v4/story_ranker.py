from datetime import datetime, timezone


# =========================================================
# STORY RANKING CONFIGURATION
# =========================================================

CONFIDENCE_SCORES = {
    "high": 30,
    "medium": 20,
    "low": 8,
}


CLAIM_STATUS_SCORES = {
    "agreement": 20,
    "partial": 10,
    "insufficient": 2,
    "conflict": -25,
}


GEOGRAPHY_SCORES = {
    "preferred_state": 20,
    "national": 16,
    "other_state": 10,
    "world": 8,
}


# Cap source bonus so stories reported by many feeds
# do not completely dominate ranking.
MAX_SOURCE_BONUS = 15


# =========================================================
# BASIC HELPERS
# =========================================================

def safe_number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_value(value):
    if not value:
        return ""

    return str(value).strip().lower()


# =========================================================
# CONFIDENCE SCORE
# =========================================================

def score_confidence(story):
    confidence = normalize_value(
        story.get("confidence", "low")
    )

    return CONFIDENCE_SCORES.get(
        confidence,
        0,
    )


# =========================================================
# INDEPENDENT SOURCE SCORE
# =========================================================

def score_sources(story):
    """
    Reward independent publisher confirmation.

    1 source  -> 0
    2 sources -> 5
    3 sources -> 10
    4+        -> capped at 15
    """

    count = int(
        safe_number(
            story.get(
                "independent_source_count",
                0,
            )
        )
    )

    if count <= 1:
        return 0

    bonus = (count - 1) * 5

    return min(
        bonus,
        MAX_SOURCE_BONUS,
    )


# =========================================================
# PRIMARY SOURCE SCORE
# =========================================================

def score_primary_source(story):
    """
    Official/primary-source confirmation is useful evidence,
    but should not dominate independent journalism.
    """

    if story.get("has_primary_source"):
        return 3

    return 0


# =========================================================
# CLAIM VERIFICATION SCORE
# =========================================================

def score_claim_verification(story):
    status = normalize_value(
        story.get(
            "claim_status",
            "insufficient",
        )
    )

    score = CLAIM_STATUS_SCORES.get(
        status,
        0,
    )

    claim_data = story.get(
        "claim_verification",
        {},
    ) or {}

    agreements = int(
        safe_number(
            claim_data.get(
                "agreement_count",
                0,
            )
        )
    )

    partials = int(
        safe_number(
            claim_data.get(
                "partial_count",
                0,
            )
        )
    )

    conflicts = int(
        safe_number(
            claim_data.get(
                "conflict_count",
                0,
            )
        )
    )

    # Additional evidence within a cluster.
    score += min(
        agreements * 3,
        9,
    )

    score += min(
        partials * 1,
        3,
    )

    # Conflicting factual claims are strongly penalized.
    score -= min(
        conflicts * 10,
        30,
    )

    return score


# =========================================================
# GEOGRAPHIC RELEVANCE SCORE
# =========================================================

def score_geography(scope):
    scope = normalize_value(scope)

    return GEOGRAPHY_SCORES.get(
        scope,
        0,
    )


# =========================================================
# RECENCY
# =========================================================

def get_story_datetime(story):
    """
    Find the newest publication time available in a story.

    verifier.py currently exposes story["sources"], each of
    which may contain published_at as an ISO string.
    """

    dates = []

    for source in story.get(
        "sources",
        [],
    ):
        published_at = source.get(
            "published_at"
        )

        if not published_at:
            continue

        try:
            if isinstance(
                published_at,
                datetime,
            ):
                parsed = published_at

            else:
                value = str(
                    published_at
                ).strip()

                # Support timestamps ending in Z.
                if value.endswith("Z"):
                    value = (
                        value[:-1]
                        + "+00:00"
                    )

                parsed = (
                    datetime.fromisoformat(
                        value
                    )
                )

            if parsed.tzinfo is None:
                parsed = parsed.replace(
                    tzinfo=timezone.utc
                )

            dates.append(parsed)

        except (
            TypeError,
            ValueError,
        ):
            continue

    if not dates:
        return None

    return max(dates)


def score_recency(
    story,
    now=None,
):
    """
    Strongly prefer recent stories.

    <= 6 hours  : 20
    <= 12 hours : 17
    <= 24 hours : 14
    <= 36 hours : 10
    <= 48 hours : 6
    <= 72 hours : 2
    older       : 0
    """

    published_at = get_story_datetime(
        story
    )

    if published_at is None:
        return 3

    if now is None:
        now = datetime.now(
            timezone.utc
        )

    if now.tzinfo is None:
        now = now.replace(
            tzinfo=timezone.utc
        )

    age_hours = (
        now - published_at
    ).total_seconds() / 3600

    # Future timestamps can happen because of bad feed
    # metadata. Treat them as fresh rather than allowing
    # them to create extra score.
    age_hours = max(
        age_hours,
        0,
    )

    if age_hours <= 6:
        return 20

    if age_hours <= 12:
        return 17

    if age_hours <= 24:
        return 14

    if age_hours <= 36:
        return 10

    if age_hours <= 48:
        return 6

    if age_hours <= 72:
        return 2

    return 0


# =========================================================
# STORY QUALITY
# =========================================================

def score_story_quality(story):
    """
    Small quality signals.

    These should never outweigh verification.
    """

    score = 0

    title = (
        story.get("title")
        or ""
    ).strip()

    sources = story.get(
        "sources",
        [],
    )

    # Useful, non-empty headline.
    if len(title) >= 20:
        score += 2

    # Slight reward when source URLs exist.
    valid_urls = sum(
        1
        for source in sources
        if source.get("url")
    )

    if valid_urls >= 1:
        score += 1

    return score


# =========================================================
# NEWSWORTHINESS
# =========================================================

HIGH_IMPACT_TERMS = {
    "government", "cabinet", "parliament", "supreme court", "policy",
    "bill", "law", "election", "budget", "minister", "prime minister",
    "president", "war", "attack", "terror", "terrorism", "missile",
    "military", "army", "ceasefire", "explosion", "bomb", "conflict",
    "earthquake", "flood", "cyclone", "storm", "wildfire", "landslide",
    "disaster", "emergency", "evacuation", "alert", "rbi", "reserve bank",
    "interest rate", "inflation", "gdp", "economy", "economic", "recession",
    "tariff", "launch", "mission", "satellite", "spacecraft",
    "artificial intelligence", "ai", "cyberattack", "outage", "convicted",
    "conviction", "arrested", "arrest", "raid", "investigation",
    "shutdown", "strike", "ban", "crisis", "shortage", "collapse",
}

ROUTINE_CONTENT_TERMS = {
    "photo of the day", "picture of the day", "apod", "horoscope",
    "daily horoscope", "gold rate today", "gold price today",
    "silver rate today", "silver price today", "weather today",
    "daily weather", "petrol price today", "diesel price today",
}


def get_story_text(story):
    parts = []
    title = story.get("canonical_title") or story.get("title") or ""
    if title:
        parts.append(str(title))

    for article in story.get("articles", []):
        article_title = (
            article.get("canonical_title")
            or article.get("title")
            or ""
        )
        summary = (
            article.get("canonical_summary")
            or article.get("summary")
            or ""
        )
        if article_title:
            parts.append(str(article_title))
        if summary:
            parts.append(str(summary))

    return " ".join(parts).lower()


def contains_phrase(text, phrase):
    import re

    pattern = (
        r"(?<!\w)"
        + re.escape(phrase.lower())
        + r"(?!\w)"
    )

    return re.search(pattern, text) is not None


def score_newsworthiness(story):
    text = get_story_text(story)

    if not text:
        return 0

    score = 0

    matched_high_impact = {
        term
        for term in HIGH_IMPACT_TERMS
        if contains_phrase(text, term)
    }

    impact_count = len(matched_high_impact)

    if impact_count >= 3:
        score += 16
    elif impact_count == 2:
        score += 12
    elif impact_count == 1:
        score += 7

    routine_matches = {
        term
        for term in ROUTINE_CONTENT_TERMS
        if contains_phrase(text, term)
    }

    if routine_matches:
        score -= 15

    source_count = int(
        safe_number(
            story.get("independent_source_count", 0)
        )
    )

    if source_count >= 4:
        score += 4
    elif source_count >= 3:
        score += 2

    return max(-15, min(score, 20))


# =========================================================
# CONFLICT SAFETY
# =========================================================

def has_serious_conflict(story):
    claim_data = story.get(
        "claim_verification",
        {},
    ) or {}

    conflict_count = int(
        safe_number(
            claim_data.get(
                "conflict_count",
                0,
            )
        )
    )

    status = normalize_value(
        story.get(
            "claim_status",
            "",
        )
    )

    return (
        status == "conflict"
        or conflict_count > 0
    )


# =========================================================
# FINAL STORY SCORE
# =========================================================

def calculate_story_score(
    story,
    geography_scope,
    now=None,
):
    """
    Calculate ranking score and expose the individual
    components for debugging and future tuning.
    """

    components = {
        "confidence": score_confidence(
            story
        ),

        "sources": score_sources(
            story
        ),

        "primary_source":
            score_primary_source(
                story
            ),

        "claims":
            score_claim_verification(
                story
            ),

        "geography":
            score_geography(
                geography_scope
            ),

        "recency":
            score_recency(
                story,
                now=now,
            ),

        "quality":
            score_story_quality(
                story
            ),

        "newsworthiness":
            score_newsworthiness(
                story
            ),
    }

    total = sum(
        components.values()
    )

    return {
        "score": total,
        "components": components,
        "newsworthiness_score":
            components["newsworthiness"],
        "serious_conflict":
            has_serious_conflict(
                story
            ),
    }


# =========================================================
# RANK ONE GEOGRAPHIC SECTION
# =========================================================

def rank_section(
    stories,
    geography_scope,
    now=None,
):
    """
    Rank stories within one geographic section.

    Does NOT remove stories.
    """

    ranked = []

    for story in stories:

        ranking = calculate_story_score(
            story,
            geography_scope,
            now=now,
        )

        ranked_story = {
            **story,

            "geography_scope":
                geography_scope,

            "ranking_score":
                ranking["score"],

            "ranking_components":
                ranking["components"],

            "newsworthiness_score":
                ranking.get(
                    "newsworthiness_score",
                    0,
                ),

            "serious_conflict":
                ranking[
                    "serious_conflict"
                ],
        }

        ranked.append(
            ranked_story
        )

    ranked.sort(
        key=lambda story: (
            story.get(
                "serious_conflict",
                False,
            ) is False,

            story.get(
                "ranking_score",
                0,
            ),

            story.get(
                "independent_source_count",
                0,
            ),
        ),
        reverse=True,
    )

    return ranked


# =========================================================
# RANK ALL GEOGRAPHIC SECTIONS
# =========================================================

def rank_stories(
    sections,
    now=None,
):
    """
    Input:

    {
        "preferred_state": [...],
        "other_state": [...],
        "national": [...],
        "world": [...]
    }

    Output has the same structure, but every story contains
    ranking_score and ranking_components.
    """

    ranked_sections = {}

    scopes = [
        "preferred_state",
        "other_state",
        "national",
        "world",
    ]

    for scope in scopes:

        stories = sections.get(
            scope,
            []
        )

        ranked_sections[scope] = (
            rank_section(
                stories,
                geography_scope=scope,
                now=now,
            )
        )

    return ranked_sections