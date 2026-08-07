# news_v4/selector.py

import re
from collections import Counter


# =========================================================
# CONFIGURATION
# =========================================================

TARGET_DURATION_MINUTES = 39
MIN_DURATION_MINUTES = 35
MAX_DURATION_MINUTES = 42

DEFAULT_STORY_SECONDS = 70

SECTION_LIMITS = {
    "preferred_state": 10,
    "national": 12,
    "other_state": 6,
    "world": 8,
}

MAX_LIMITED_STORIES = 4

MIN_PREFERRED_STATE_STORIES = 3
PREFERRED_STATE_MIN_NEWSWORTHINESS = 0
GENERAL_MIN_NEWSWORTHINESS = 0

MAX_RELATED_TOPIC_STORIES = 1


# =========================================================
# EDITORIAL FILTER CONFIGURATION
# =========================================================

LOW_VALUE_PATTERNS = [
    r"\bprice drops?\b",
    r"\bprice cut\b",
    r"\bdiscount\b",
    r"\bdeal\b",
    r"\boffer\b",
    r"\bsale\b",
    r"\bamazon\b.*\bclaim\b",
    r"\bflipkart\b.*\bclaim\b",
    r"\bhow to claim\b",

    r"\bgold price today\b",
    r"\bgold rate today\b",
    r"\bsilver price today\b",
    r"\bsilver rate today\b",
    r"\bpetrol price today\b",
    r"\bdiesel price today\b",

    r"\bhoroscope\b",
    r"\bphoto of the day\b",
    r"\bpicture of the day\b",
    r"\bapod\b",
]

TRIVIAL_VIRAL_PATTERNS = [
    r"\bviral stunt\b",
    r"\bviral challenge\b",
    r"\bviral prank\b",
    r"\binternet reacts\b",
    r"\bsocial media reacts\b",
]


# =========================================================
# CATEGORY CONFIGURATION
# =========================================================

# Geography/feed labels must not become final topical
# categories. Geography is handled independently by
# geo_classifier.py and geographic_ranker.py.

GEOGRAPHY_CATEGORIES = {
    "state",
    "local",
    "national",
    "india",
    "world",
    "international",
    "global",
}


CATEGORY_FAMILIES = {
    "sports": {
        "sports",
        "sport",
        "cricket",
        "football",
        "soccer",
        "tennis",
        "badminton",
        "hockey",
    },

    "business": {
        "business",
        "economy",
        "economic",
        "finance",
        "financial",
        "market",
        "markets",
    },

    "technology": {
        "technology",
        "tech",
        "ai",
        "artificial_intelligence",
    },

    "science": {
        "science",
        "space",
    },

    "politics": {
        "politics",
        "political",
        "government",
        "policy",
        "election",
        "elections",
    },

    "entertainment": {
        "entertainment",
        "movie",
        "movies",
        "film",
        "films",
        "cinema",
        "television",
        "tv",
    },

    "health": {
        "health",
        "healthcare",
        "medical",
        "medicine",
    },
}


# =========================================================
# RELATED TOPIC CONFIGURATION
# =========================================================

TOPIC_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "was",
    "were",
    "will",
    "with",
    "after",
    "amid",
    "over",
    "new",
    "latest",
    "today",
    "update",
    "updates",
    "live",
    "watch",
    "video",
    "report",
    "reports",
    "says",
    "said",
}


# =========================================================
# DUPLICATE-EVENT CONFIGURATION
# =========================================================

DUPLICATE_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "was",
    "were",
    "will",
    "with",

    "after",
    "amid",
    "over",
    "new",
    "latest",
    "today",
    "update",
    "updates",
    "report",
    "reports",
    "says",
    "said",
}


# =========================================================
# BASIC HELPERS
# =========================================================

def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def normalize(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def get_story_text(story):
    parts = []

    title = (
        story.get("canonical_title")
        or story.get("title")
        or ""
    )

    if title:
        parts.append(
            str(title)
        )

    for article in story.get(
        "articles",
        [],
    ):
        article_title = (
            article.get(
                "canonical_title"
            )
            or article.get(
                "title"
            )
            or ""
        )

        summary = (
            article.get(
                "canonical_summary"
            )
            or article.get(
                "summary"
            )
            or ""
        )

        if article_title:
            parts.append(
                str(article_title)
            )

        if summary:
            parts.append(
                str(summary)
            )

    return " ".join(
        parts
    ).lower()


def matches_any_pattern(
    text,
    patterns,
):
    return any(
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
        is not None
        for pattern in patterns
    )


# =========================================================
# EDITORIAL VALUE
# =========================================================

def is_low_value_editorial_story(
    story,
):
    text = get_story_text(
        story
    )

    if not text:
        return False

    if matches_any_pattern(
        text,
        LOW_VALUE_PATTERNS,
    ):
        return True

    if matches_any_pattern(
        text,
        TRIVIAL_VIRAL_PATTERNS,
    ):
        return True

    return False


# =========================================================
# DUPLICATE-EVENT HELPERS
# =========================================================

def normalize_event_text(value):
    text = normalize(
        value
    )

    text = text.replace(
        "’",
        "'",
    )

    text = text.replace(
        "–",
        "-",
    )

    text = text.replace(
        "—",
        "-",
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def normalize_event_token(token):
    token = normalize(
        token
    )

    variants = {
        "terrorism": "terror",
        "terrorist": "terror",
        "terrorists": "terror",

        "offence": "charge",
        "offences": "charge",
        "offense": "charge",
        "offenses": "charge",
        "charged": "charge",
        "charges": "charge",

        "conviction": "convict",
        "convictions": "convict",
        "convicted": "convict",
        "convicts": "convict",

        "attacked": "attack",
        "attacking": "attack",
        "attacks": "attack",
        "attackers": "attacker",

        "raided": "raid",
        "raiding": "raid",
        "raids": "raid",

        "arrested": "arrest",
        "arrests": "arrest",

        "banned": "ban",
        "banning": "ban",
        "bans": "ban",

        "warned": "warn",
        "warning": "warn",
        "warnings": "warn",
        "warns": "warn",

        "announced": "announce",
        "announces": "announce",
        "announcement": "announce",
        "announcements": "announce",

        "died": "death",
        "dies": "death",
        "dead": "death",

        "won": "win",
        "wins": "win",
        "winning": "win",

        "beat": "defeat",
        "beaten": "defeat",
        "beats": "defeat",
        "defeated": "defeat",
        "defeats": "defeat",
    }

    return variants.get(
        token,
        token,
    )


def get_event_tokens(title):
    text = normalize_event_text(
        title
    )

    tokens = set()

    for token in text.split():

        if token in DUPLICATE_STOPWORDS:
            continue

        if (
            len(token) < 3
            and not token.isdigit()
        ):
            continue

        token = normalize_event_token(
            token
        )

        if token:
            tokens.add(
                token
            )

    return tokens


def get_event_numbers(title):
    text = normalize(
        title
    )

    return set(
        re.findall(
            r"\d+(?:\.\d+)?",
            text,
        )
    )


def get_event_identifiers(title):
    text = normalize_event_text(
        title
    )

    identifiers = set()

    ordinal_map = {
        "first": "1",
        "1st": "1",
        "second": "2",
        "2nd": "2",
        "third": "3",
        "3rd": "3",
        "fourth": "4",
        "4th": "4",
        "fifth": "5",
        "5th": "5",
    }

    words = text.split()

    for word in words:

        if word in ordinal_map:
            identifiers.add(
                "ordinal:"
                + ordinal_map[word]
            )

    stages = {
        "quarterfinal":
            "quarterfinal",

        "quarterfinals":
            "quarterfinal",

        "semifinal":
            "semifinal",

        "semifinals":
            "semifinal",

        "final":
            "final",

        "finals":
            "final",
    }

    for word in words:

        if word in stages:
            identifiers.add(
                "stage:"
                + stages[word]
            )

    return identifiers


def event_identifiers_conflict(
    title_a,
    title_b,
):
    identifiers_a = (
        get_event_identifiers(
            title_a
        )
    )

    identifiers_b = (
        get_event_identifiers(
            title_b
        )
    )

    if (
        not identifiers_a
        or not identifiers_b
    ):
        return False

    ordinals_a = {
        value
        for value
        in identifiers_a
        if value.startswith(
            "ordinal:"
        )
    }

    ordinals_b = {
        value
        for value
        in identifiers_b
        if value.startswith(
            "ordinal:"
        )
    }

    if (
        ordinals_a
        and ordinals_b
        and ordinals_a.isdisjoint(
            ordinals_b
        )
    ):
        return True

    stages_a = {
        value
        for value
        in identifiers_a
        if value.startswith(
            "stage:"
        )
    }

    stages_b = {
        value
        for value
        in identifiers_b
        if value.startswith(
            "stage:"
        )
    }

    if (
        stages_a
        and stages_b
        and stages_a.isdisjoint(
            stages_b
        )
    ):
        return True

    return False


def token_overlap_score(
    title_a,
    title_b,
):
    tokens_a = get_event_tokens(
        title_a
    )

    tokens_b = get_event_tokens(
        title_b
    )

    if (
        not tokens_a
        or not tokens_b
    ):
        return 0.0

    common = (
        tokens_a
        & tokens_b
    )

    denominator = min(
        len(tokens_a),
        len(tokens_b),
    )

    if denominator == 0:
        return 0.0

    return (
        len(common)
        / denominator
    )


def jaccard_event_score(
    title_a,
    title_b,
):
    tokens_a = get_event_tokens(
        title_a
    )

    tokens_b = get_event_tokens(
        title_b
    )

    if (
        not tokens_a
        or not tokens_b
    ):
        return 0.0

    union = (
        tokens_a
        | tokens_b
    )

    if not union:
        return 0.0

    return (
        len(
            tokens_a
            & tokens_b
        )
        / len(union)
    )


def numbers_compatible(
    title_a,
    title_b,
):
    numbers_a = get_event_numbers(
        title_a
    )

    numbers_b = get_event_numbers(
        title_b
    )

    if (
        not numbers_a
        or not numbers_b
    ):
        return True

    return bool(
        numbers_a
        & numbers_b
    )
def get_story_article_keys(story):
    """
    Build stable identifiers for the source articles inside a story.

    URL is preferred because two clusters containing the same article
    are definitely overlapping. If URL is unavailable, use publisher
    + normalized article title.
    """

    keys = set()

    for article in story.get("articles", []):

        url = (
            article.get("url")
            or article.get("link")
            or article.get("article_url")
            or ""
        )

        url = str(url).strip()

        if url:
            keys.add(
                "url:" + url
            )
            continue

        publisher = normalize_event_text(
            article.get("publisher_id")
            or article.get("publisher")
            or article.get("source")
            or ""
        )

        title = normalize_event_text(
            article.get("canonical_title")
            or article.get("title")
            or ""
        )

        if publisher and title:
            keys.add(
                "article:"
                + publisher
                + "|"
                + title
            )

    return keys


def has_same_source_article(
    story_a,
    story_b,
):
    """
    Return True when two story objects contain at least one
    identical underlying source article.
    """

    keys_a = get_story_article_keys(
        story_a
    )

    keys_b = get_story_article_keys(
        story_b
    )

    if not keys_a or not keys_b:
        return False

    return bool(
        keys_a & keys_b
    )


def is_duplicate_event(
    story_a,
    story_b,
):
    """
    Conservative final duplicate-event guard.

    Duplicate evidence priority:

    1. Same underlying source article
    2. Same normalized story title
    3. Strong event-token similarity

    Source-article identity is deterministic and takes
    priority over fuzzy title comparison.
    """

    # =====================================================
    # 1. SAME UNDERLYING SOURCE ARTICLE
    # =====================================================

    if has_same_source_article(
        story_a,
        story_b,
    ):
        return True

    # =====================================================
    # 2. TITLE-BASED EVENT COMPARISON
    # =====================================================

    title_a = (
        story_a.get("title")
        or story_a.get("canonical_title")
        or ""
    )

    title_b = (
        story_b.get("title")
        or story_b.get("canonical_title")
        or ""
    )

    if (
        not title_a
        or not title_b
    ):
        return False

    if event_identifiers_conflict(
        title_a,
        title_b,
    ):
        return False

    normalized_a = (
        normalize_event_text(
            title_a
        )
    )

    normalized_b = (
        normalize_event_text(
            title_b
        )
    )

    if (
        normalized_a
        and normalized_a
        == normalized_b
    ):
        return True

    tokens_a = get_event_tokens(
        title_a
    )

    tokens_b = get_event_tokens(
        title_b
    )

    if (
        not tokens_a
        or not tokens_b
    ):
        return False

    common_tokens = (
        tokens_a
        & tokens_b
    )

    common_count = len(
        common_tokens
    )

    if common_count < 3:
        return False

    overlap = token_overlap_score(
        title_a,
        title_b,
    )

    jaccard = jaccard_event_score(
        title_a,
        title_b,
    )

    numbers_a = get_event_numbers(
        title_a
    )

    numbers_b = get_event_numbers(
        title_b
    )

    shared_numbers = (
        numbers_a
        & numbers_b
    )

    numeric_compatible = (
        numbers_compatible(
            title_a,
            title_b,
        )
    )

    if (
        common_count >= 5
        and overlap >= 0.72
    ):
        return True

    if (
        common_count >= 5
        and overlap >= 0.62
        and jaccard >= 0.45
    ):
        return True

    smaller_size = min(
        len(tokens_a),
        len(tokens_b),
    )

    if (
        smaller_size <= 6
        and common_count >= 4
        and overlap >= 0.75
    ):
        return True

    if (
        shared_numbers
        and common_count >= 5
    ):
        return True

    if (
        shared_numbers
        and common_count >= 4
        and overlap >= 0.55
    ):
        return True

    if (
        numeric_compatible
        and common_count >= 4
        and overlap >= 0.68
        and jaccard >= 0.42
    ):
        return True

    return False


def duplicate_of_selected(
    candidate,
    selected,
):
    for existing in selected:

        if is_duplicate_event(
            candidate,
            existing,
        ):
            return existing

    return None


# =========================================================
# RELATED-TOPIC DIVERSITY
# =========================================================

def get_topic_tokens(story):
    title = (
        story.get(
            "canonical_title"
        )
        or story.get(
            "title"
        )
        or ""
    )

    text = normalize_event_text(
        title
    )

    tokens = set()

    for token in text.split():

        if token in TOPIC_STOPWORDS:
            continue

        if len(token) < 4:
            continue

        token = normalize_event_token(
            token
        )

        tokens.add(
            token
        )

    return tokens


def related_topic_score(
    story_a,
    story_b,
):
    tokens_a = get_topic_tokens(
        story_a
    )

    tokens_b = get_topic_tokens(
        story_b
    )

    if (
        not tokens_a
        or not tokens_b
    ):
        return 0.0

    common = (
        tokens_a
        & tokens_b
    )

    if len(common) < 2:
        return 0.0

    smaller = min(
        len(tokens_a),
        len(tokens_b),
    )

    if smaller == 0:
        return 0.0

    return (
        len(common)
        / smaller
    )


def is_related_topic(
    story_a,
    story_b,
):
    if is_duplicate_event(
        story_a,
        story_b,
    ):
        return True

    tokens_a = get_topic_tokens(
        story_a
    )

    tokens_b = get_topic_tokens(
        story_b
    )

    common = (
        tokens_a
        & tokens_b
    )

    score = related_topic_score(
        story_a,
        story_b,
    )

    if (
        len(common) >= 3
        and score >= 0.50
    ):
        return True

    return False


def related_topic_count(
    candidate,
    selected,
):
    return sum(
        1
        for existing in selected
        if is_related_topic(
            candidate,
            existing,
        )
    )


# =========================================================
# VERIFICATION TIER
# =========================================================

def get_verification_tier(story):
    if story.get(
        "serious_conflict",
        False,
    ):
        return "rejected"

    claim_status = normalize(
        story.get(
            "claim_status",
            "insufficient",
        )
    )

    if claim_status == "conflict":
        return "rejected"

    confidence = normalize(
        story.get(
            "confidence",
            "low",
        )
    )

    independent_sources = safe_int(
        story.get(
            "independent_source_count",
            0,
        )
    )

    if (
        independent_sources >= 2
        and claim_status in {
            "agreement",
            "partial",
        }
    ):
        return "strong"

    if confidence == "high":
        return "strong"

    return "limited"


# =========================================================
# STORY ELIGIBILITY
# =========================================================

def is_story_eligible(story):
    tier = get_verification_tier(
        story
    )

    if tier == "rejected":
        return False

    title = (
        story.get(
            "title"
        )
        or ""
    ).strip()

    if len(title) < 10:
        return False

    sources = story.get(
        "sources",
        [],
    )

    if not sources:
        return False

    newsworthiness = safe_int(
        story.get(
            "newsworthiness_score",
            0,
        )
    )

    if newsworthiness <= -10:
        return False

    if is_low_value_editorial_story(
        story
    ):
        return False

    return True


# =========================================================
# DURATION ESTIMATION
# =========================================================

def estimate_story_seconds(story):
    score = safe_int(
        story.get(
            "ranking_score",
            0,
        )
    )

    tier = get_verification_tier(
        story
    )

    if score >= 90:
        seconds = 150

    elif score >= 75:
        seconds = 120

    elif score >= 60:
        seconds = 90

    else:
        seconds = DEFAULT_STORY_SECONDS

    if tier == "limited":
        seconds = min(
            seconds,
            60,
        )

    return seconds


# =========================================================
# CATEGORY HELPERS
# =========================================================

def normalize_story_category(
    category,
):
    """
    Normalize category labels from different publishers.
    """

    normalized = normalize(
        category
    )

    return (
        normalized
        .replace(" ", "_")
        .replace("-", "_")
    )


def canonical_category(
    category,
):
    """
    Convert publisher-specific category labels into one
    canonical podcast topic.

    Geography/feed labels return None because geography
    is stored independently.
    """

    category = (
        normalize_story_category(
            category
        )
    )

    if not category:
        return None

    if category in GEOGRAPHY_CATEGORIES:
        return None

    for canonical, aliases in (
        CATEGORY_FAMILIES.items()
    ):

        if category in aliases:
            return canonical

    # Preserve legitimate categories that are not yet
    # represented in CATEGORY_FAMILIES.
    return category


def get_story_categories(story):
    """
    Determine meaningful topical categories for a story.

    Categories are counted once per article so a single
    feed cannot artificially boost a category by repeating
    labels.

    Geography labels such as state/national/world/local
    are excluded.

    Multi-article clusters prefer topics supported by at
    least two articles.

    When publishers disagree on labels, the strongest
    available category is retained.

    Final stories contain at most two topical categories.
    """

    category_counts = Counter()

    articles = story.get(
        "articles",
        [],
    )

    if not isinstance(
        articles,
        list,
    ):
        articles = []

    for article in articles:

        if not isinstance(
            article,
            dict,
        ):
            continue

        article_categories = set()

        categories = article.get(
            "categories",
            [],
        )

        if isinstance(
            categories,
            str,
        ):
            categories = [
                categories
            ]

        if not isinstance(
            categories,
            (
                list,
                tuple,
                set,
            ),
        ):
            continue

        for category in categories:

            canonical = (
                canonical_category(
                    category
                )
            )

            if canonical:
                article_categories.add(
                    canonical
                )

        for category in (
            article_categories
        ):
            category_counts[
                category
            ] += 1

    if not category_counts:
        return [
            "general"
        ]

    article_count = max(
        len(articles),
        1,
    )

    # Single article:
    # one category vote is enough.
    #
    # Multi-article cluster:
    # prefer categories supported by at least two articles.
    minimum_support = (
        1
        if article_count == 1
        else 2
    )

    supported = [
        (
            category,
            count,
        )
        for category, count
        in category_counts.items()
        if count >= minimum_support
    ]

    # No consensus:
    # retain only the strongest category/categories instead
    # of returning the union of all source metadata.
    if not supported:

        highest_count = max(
            category_counts.values()
        )

        supported = [
            (
                category,
                count,
            )
            for category, count
            in category_counts.items()
            if count == highest_count
        ]

    # Highest article support first.
    # Alphabetical order provides deterministic tie
    # handling for tests and manifests.
    supported.sort(
        key=lambda item: (
            -item[1],
            item[0],
        )
    )

    final_categories = [
        category
        for category, _
        in supported[:2]
    ]

    return (
        final_categories
        or ["general"]
    )


# =========================================================
# PREPARE CANDIDATES
# =========================================================

def prepare_candidates(
    ranked_sections,
):
    candidates = []

    for scope, stories in (
        ranked_sections.items()
    ):

        for story in stories:

            if not is_story_eligible(
                story
            ):
                continue

            candidate = {
                **story,

                "geography_scope":
                    scope,

                "verification_tier":
                    get_verification_tier(
                        story
                    ),

                "categories":
                    get_story_categories(
                        story
                    ),
            }

            candidates.append(
                candidate
            )

    candidates.sort(
        key=lambda story: (
            story[
                "verification_tier"
            ] == "strong",

            story.get(
                "newsworthiness_score",
                0,
            ),

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

    return candidates


# =========================================================
# SELECTION HELPERS
# =========================================================

def can_select_story(
    story,
    selected,
    section_counts,
    limited_count,
    enforce_topic_diversity=True,
    enforce_section_limits=True,
):
    if duplicate_of_selected(
        story,
        selected,
    ) is not None:
        return (
            False,
            "duplicate",
        )

    scope = story.get(
        "geography_scope",
        "",
    )

    limit = SECTION_LIMITS.get(
        scope,
        5,
    )

    if (
    enforce_section_limits
    and section_counts[scope] >= limit
):
     return (
        False,
        "section_limit",
    )

    tier = story.get(
        "verification_tier",
        "limited",
    )

    if (
        tier == "limited"
        and limited_count
        >= MAX_LIMITED_STORIES
    ):
        return (
            False,
            "limited_limit",
        )

    if (
        enforce_topic_diversity
        and related_topic_count(
            story,
            selected,
        )
        >= MAX_RELATED_TOPIC_STORIES
    ):
        return (
            False,
            "related_topic",
        )

    return (
        True,
        "",
    )


def append_selected_story(
    story,
    selected,
    section_counts,
):
    story_seconds = (
        estimate_story_seconds(
            story
        )
    )

    selected_story = {
        **story,

        "episode_order":
            len(selected) + 1,

        "planned_duration_seconds":
            story_seconds,
    }

    selected.append(
        selected_story
    )

    scope = story.get(
        "geography_scope",
        "",
    )

    section_counts[
        scope
    ] += 1

    return story_seconds


# =========================================================
# MASTER EPISODE SELECTION
# =========================================================

def select_master_episode(
    ranked_sections,
):
    """
    Select one language-independent master episode.

    Pass 1:
        Reserve meaningful preferred-state coverage.

    Pass 2:
        Fill using global editorial ranking.

    Pass 3:
        If necessary, relax only topic diversity to reach
        minimum episode duration.

    Duplicate, conflict, section and limited-story
    protections remain active.
    """

    candidates = prepare_candidates(
        ranked_sections
    )

    selected = []

    section_counts = Counter()

    limited_count = 0

    estimated_seconds = 0

    duplicate_rejections = 0
    related_topic_rejections = 0
    editorial_rejections = 0

    target_seconds = (
        TARGET_DURATION_MINUTES
        * 60
    )

    # =====================================================
    # PASS 1 — PREFERRED STATE
    # =====================================================

    preferred_candidates = [
        story
        for story in candidates
        if (
            story.get(
                "geography_scope"
            )
            == "preferred_state"
            and safe_int(
                story.get(
                    "newsworthiness_score",
                    0,
                )
            )
            >= PREFERRED_STATE_MIN_NEWSWORTHINESS
        )
    ]

    for story in (
        preferred_candidates
    ):

        if (
            section_counts[
                "preferred_state"
            ]
            >= MIN_PREFERRED_STATE_STORIES
        ):
            break

        allowed, reason = (
            can_select_story(
                story,
                selected,
                section_counts,
                limited_count,
                enforce_topic_diversity=True,
            )
        )

        if not allowed:

            if reason == "duplicate":
                duplicate_rejections += 1

            elif reason == "related_topic":
                related_topic_rejections += 1

            continue

        story_seconds = (
            append_selected_story(
                story,
                selected,
                section_counts,
            )
        )

        if (
            story.get(
                "verification_tier"
            )
            == "limited"
        ):
            limited_count += 1

        estimated_seconds += (
            story_seconds
        )

    # =====================================================
    # PASS 2 — GENERAL EDITORIAL SELECTION
    # =====================================================

    for story in candidates:

        if story in selected:
            continue

        newsworthiness = safe_int(
            story.get(
                "newsworthiness_score",
                0,
            )
        )

        if (
            newsworthiness
            < GENERAL_MIN_NEWSWORTHINESS
        ):
            editorial_rejections += 1
            continue

        allowed, reason = (
            can_select_story(
                story,
                selected,
                section_counts,
                limited_count,
                enforce_topic_diversity=True,
            )
        )

        if not allowed:

            if reason == "duplicate":
                duplicate_rejections += 1

            elif reason == "related_topic":
                related_topic_rejections += 1

            continue

        story_seconds = (
            append_selected_story(
                story,
                selected,
                section_counts,
            )
        )

        if (
            story.get(
                "verification_tier"
            )
            == "limited"
        ):
            limited_count += 1

        estimated_seconds += (
            story_seconds
        )

        if (
            estimated_seconds
            >= target_seconds
        ):
            break

    # =====================================================
    # PASS 3 — DURATION FALLBACK
    # =====================================================

    minimum_seconds = (
        MIN_DURATION_MINUTES
        * 60
    )

    if (
        estimated_seconds
        < minimum_seconds
    ):

        for story in candidates:

            if story in selected:
                continue

            if is_low_value_editorial_story(
                story
            ):
                continue

            newsworthiness = safe_int(
                story.get(
                    "newsworthiness_score",
                    0,
                )
            )

            if newsworthiness < 0:
                continue

            allowed, reason = (
                can_select_story(
                    story,
                    selected,
                    section_counts,
                    limited_count,
                    enforce_topic_diversity=False,
                )
            )

            if not allowed:

                if reason == "duplicate":
                    duplicate_rejections += 1

                continue

            story_seconds = (
                append_selected_story(
                    story,
                    selected,
                    section_counts,
                )
            )

            if (
                story.get(
                    "verification_tier"
                )
                == "limited"
            ):
                limited_count += 1

            estimated_seconds += (
                story_seconds
            )

            if (
                estimated_seconds
                >= minimum_seconds
            ):
                break

                # =====================================================
    # PASS 4 — MINIMUM DURATION RESCUE
    # =====================================================
    #
    # Pass 3 may still fail to reach the minimum when all
    # useful remaining stories belong to sections that
    # already reached their normal editorial limits.
    #
    # For minimum-duration rescue only, relax section
    # limits while preserving:
    #
    #   - duplicate protection
    #   - conflict / eligibility protection
    #   - limited-story cap
    #   - low-value editorial filtering
    #
    # Topic diversity is already relaxed in Pass 3.
    # =====================================================

    if estimated_seconds < minimum_seconds:

        for story in candidates:

            if story in selected:
                continue

            if is_low_value_editorial_story(
                story
            ):
                continue

            newsworthiness = safe_int(
                story.get(
                    "newsworthiness_score",
                    0,
                )
            )

            if newsworthiness < 0:
                continue

            allowed, reason = (
                can_select_story(
                    story,
                    selected,
                    section_counts,
                    limited_count,
                    enforce_topic_diversity=False,
                    enforce_section_limits=False,
                )
            )

            if not allowed:

                if reason == "duplicate":
                    duplicate_rejections += 1

                continue

            story_seconds = (
                append_selected_story(
                    story,
                    selected,
                    section_counts,
                )
            )

            if (
                story.get(
                    "verification_tier"
                )
                == "limited"
            ):
                limited_count += 1

            estimated_seconds += (
                story_seconds
            )

            if (
                estimated_seconds
                >= minimum_seconds
            ):
                break

    return build_master_manifest(
        selected,
        estimated_seconds,
        duplicate_rejections,
        related_topic_rejections,
        editorial_rejections,
    )


# =========================================================
# MASTER MANIFEST
# =========================================================

def build_master_manifest(
    selected,
    estimated_seconds,
    duplicate_rejections=0,
    related_topic_rejections=0,
    editorial_rejections=0,
):
    """
    Source of truth for every language version.
    """

    return {
        "story_count":
            len(selected),

        "estimated_duration_seconds":
            estimated_seconds,

        "estimated_duration_minutes":
            round(
                estimated_seconds / 60,
                2,
            ),

        "minimum_duration_minutes":
            MIN_DURATION_MINUTES,

        "target_duration_minutes":
            TARGET_DURATION_MINUTES,

        "maximum_duration_minutes":
            MAX_DURATION_MINUTES,

        "language_independent":
            True,

        "duplicate_rejections":
            duplicate_rejections,

        "related_topic_rejections":
            related_topic_rejections,

        "editorial_rejections":
            editorial_rejections,

        "stories":
            selected,
    }