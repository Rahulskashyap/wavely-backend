# news_v4/clusterer.py

import re
from functools import lru_cache

from rapidfuzz.fuzz import (
    token_set_ratio,
    token_sort_ratio,
)

from sentence_transformers import (
    SentenceTransformer,
    util,
)


# =========================================================
# CONFIGURATION
# =========================================================

TITLE_SIMILARITY_THRESHOLD = 76
FINAL_SIMILARITY_THRESHOLD = 72
MIN_KEYWORD_OVERLAP = 0.20

MAX_TIME_DIFFERENCE_HOURS = 30
MAX_CLUSTER_SIZE = 12

# Semantic thresholds
SEMANTIC_STRONG_THRESHOLD = 0.82
SEMANTIC_NORMAL_THRESHOLD = 0.72


# =========================================================
# SEMANTIC MODEL
# =========================================================

# Load once when the module starts.
SEMANTIC_MODEL = SentenceTransformer(
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# =========================================================
# STOP WORDS
# =========================================================

STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "from",
    "of",
    "with",
    "by",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "this",
    "that",
    "these",
    "those",
    "after",
    "before",
    "over",
    "under",
    "into",
    "about",
    "amid",
    "says",
    "said",
    "say",
    "news",
    "live",
    "latest",
    "update",
    "updates",
    "today",
    "breaking",
}


# =========================================================
# GEOGRAPHY-LIKE CATEGORY LABELS
# =========================================================

# These labels describe where a story belongs rather than
# what the story is about.
#
# Geography is handled by geo_classifier.py and
# geographic_ranker.py, so these labels should not make
# two articles topically compatible.

GEOGRAPHY_CATEGORIES = {
    "state",
    "local",
    "national",
    "india",
    "world",
    "international",
    "global",
}


# =========================================================
# TOPIC FAMILIES
# =========================================================

TOPIC_FAMILIES = [
    {
        "sports",
        "sport",
        "cricket",
        "football",
        "soccer",
        "tennis",
        "badminton",
        "hockey",
    },

    {
        "business",
        "economy",
        "economic",
        "finance",
        "financial",
        "markets",
        "market",
    },

    {
        "technology",
        "tech",
        "science",
        "ai",
        "artificial_intelligence",
    },

    {
        "politics",
        "political",
        "government",
        "policy",
        "elections",
        "election",
    },

    {
        "entertainment",
        "movies",
        "movie",
        "film",
        "films",
        "cinema",
        "television",
        "tv",
    },

    {
        "health",
        "healthcare",
        "medicine",
        "medical",
    },
]


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    if not text:
        return ""

    text = str(
        text
    ).lower()

    text = re.sub(
        r"https?://\S+",
        " ",
        text,
    )

    text = "".join(
        char
        if (
            char.isalnum()
            or char.isspace()
        )
        else " "
        for char in text
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


# =========================================================
# SEMANTIC TEXT
# =========================================================

def get_semantic_text(article):
    """
    Build a compact representation of the event.

    Canonical text is preferred when available because
    multilingual articles may otherwise have very
    different surface wording.

    Title is always included.

    Summary provides additional event context when
    publishers use different headlines.
    """

    title = str(
        article.get(
            "canonical_title"
        )
        or article.get(
            "title",
            "",
        )
        or ""
    ).strip()

    summary = str(
        article.get(
            "canonical_summary"
        )
        or article.get(
            "summary",
            "",
        )
        or ""
    ).strip()

    # Avoid sending unnecessarily large descriptions
    # through the embedding model.
    if len(summary) > 700:
        summary = summary[:700]

    if summary:
        return (
            f"{title}. {summary}"
        )

    return title


# =========================================================
# SEMANTIC EMBEDDINGS
# =========================================================

@lru_cache(maxsize=10000)
def encode_semantic_text(text):
    if not text:
        return None

    return SEMANTIC_MODEL.encode(
        text,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )


def calculate_semantic_similarity(
    article_a,
    article_b,
):
    text_a = get_semantic_text(
        article_a
    )

    text_b = get_semantic_text(
        article_b
    )

    if (
        not text_a
        or not text_b
    ):
        return 0.0

    embedding_a = (
        encode_semantic_text(
            text_a
        )
    )

    embedding_b = (
        encode_semantic_text(
            text_b
        )
    )

    if (
        embedding_a is None
        or embedding_b is None
    ):
        return 0.0

    score = util.cos_sim(
        embedding_a,
        embedding_b,
    ).item()

    return float(
        score
    )


# =========================================================
# IMPORTANT WORDS
# =========================================================

def important_words(text):
    text = clean_text(
        text
    )

    words = text.split()

    return {
        word
        for word in words
        if (
            len(word) > 2
            and word
            not in STOP_WORDS
        )
    }


def keyword_overlap(
    text_a,
    text_b,
):
    words_a = important_words(
        text_a
    )

    words_b = important_words(
        text_b
    )

    if (
        not words_a
        or not words_b
    ):
        return 0.0

    intersection = (
        words_a.intersection(
            words_b
        )
    )

    union = (
        words_a.union(
            words_b
        )
    )

    if not union:
        return 0.0

    return (
        len(intersection)
        / len(union)
    )


# =========================================================
# TIME CHECK
# =========================================================

def time_compatible(
    article_a,
    article_b,
):
    time_a = article_a.get(
        "published_at"
    )

    time_b = article_b.get(
        "published_at"
    )

    # Missing timestamps should not automatically prevent
    # clustering. Other event signals still need to pass.
    if (
        time_a is None
        or time_b is None
    ):
        return True

    try:
        difference = abs(
            (
                time_a
                - time_b
            ).total_seconds()
        )

    except (
        TypeError,
        AttributeError,
    ):
        return True

    hours = (
        difference
        / 3600
    )

    return (
        hours
        <= MAX_TIME_DIFFERENCE_HOURS
    )


# =========================================================
# CATEGORY NORMALIZATION
# =========================================================

def normalize_category(category):
    if category is None:
        return ""

    return (
        str(category)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def get_categories(article):
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
        return set()

    result = set()

    for category in categories:
        normalized = (
            normalize_category(
                category
            )
        )

        if normalized:
            result.add(
                normalized
            )

    return result


def get_topical_categories(article):
    """
    Return topic categories only.

    Geography-like labels are removed because they are
    handled separately by the geography system.
    """

    return (
        get_categories(
            article
        )
        - GEOGRAPHY_CATEGORIES
    )


# =========================================================
# CATEGORY COMPATIBILITY
# =========================================================

def categories_compatible(
    article_a,
    article_b,
):
    """
    Determine whether two articles are topically
    compatible.

    IMPORTANT:

    state/local/national/world/etc. are geography labels,
    not event topics.

    They must therefore NOT make two articles compatible.

    Example:

        article A:
            ["sports", "world"]

        article B:
            ["technology", "world"]

    The shared "world" label does NOT mean these are the
    same kind of story.

    Geography is classified later by geo_classifier.py
    and geographic_ranker.py.
    """

    categories_a = get_categories(
        article_a
    )

    categories_b = get_categories(
        article_b
    )

    # No category information available.
    # Do not reject based on missing metadata.
    if (
        not categories_a
        or not categories_b
    ):
        return True

    topical_a = (
        categories_a
        - GEOGRAPHY_CATEGORIES
    )

    topical_b = (
        categories_b
        - GEOGRAPHY_CATEGORIES
    )

    # A source may provide only:
    #
    # ["world"]
    # ["national"]
    # ["state"]
    #
    # In that case categories cannot safely decide whether
    # the events differ, so similarity logic handles it.
    if (
        not topical_a
        or not topical_b
    ):
        return True

    # =====================================================
    # EXACT TOPIC OVERLAP
    # =====================================================

    if topical_a.intersection(
        topical_b
    ):
        return True

    # =====================================================
    # RELATED TOPIC FAMILIES
    # =====================================================

    for family in TOPIC_FAMILIES:
        a_matches = bool(
            topical_a.intersection(
                family
            )
        )

        b_matches = bool(
            topical_b.intersection(
                family
            )
        )

        if (
            a_matches
            and b_matches
        ):
            return True

    return False


# =========================================================
# TITLE SIMILARITY
# =========================================================

def calculate_title_similarity(
    article_a,
    article_b,
):
    title_a = clean_text(
        article_a.get(
            "canonical_title"
        )
        or article_a.get(
            "title",
            "",
        )
    )

    title_b = clean_text(
        article_b.get(
            "canonical_title"
        )
        or article_b.get(
            "title",
            "",
        )
    )

    if (
        not title_a
        or not title_b
    ):
        return 0.0

    set_score = token_set_ratio(
        title_a,
        title_b,
    )

    sort_score = token_sort_ratio(
        title_a,
        title_b,
    )

    return max(
        set_score,
        sort_score,
    )


# =========================================================
# CONTENT SIMILARITY
# =========================================================

def calculate_content_similarity(
    article_a,
    article_b,
):
    title_a = clean_text(
        article_a.get(
            "canonical_title"
        )
        or article_a.get(
            "title",
            "",
        )
    )

    title_b = clean_text(
        article_b.get(
            "canonical_title"
        )
        or article_b.get(
            "title",
            "",
        )
    )

    summary_a = clean_text(
        article_a.get(
            "canonical_summary"
        )
        or article_a.get(
            "summary",
            "",
        )
    )

    summary_b = clean_text(
        article_b.get(
            "canonical_summary"
        )
        or article_b.get(
            "summary",
            "",
        )
    )

    content_a = (
        f"{title_a} {summary_a}"
    ).strip()

    content_b = (
        f"{title_b} {summary_b}"
    ).strip()

    if (
        not content_a
        or not content_b
    ):
        return 0.0

    return token_set_ratio(
        content_a,
        content_b,
    )


# =========================================================
# EVENT KEYWORD OVERLAP
# =========================================================

def event_keyword_overlap(
    article_a,
    article_b,
):
    title_a = (
        article_a.get(
            "canonical_title"
        )
        or article_a.get(
            "title",
            "",
        )
    )

    title_b = (
        article_b.get(
            "canonical_title"
        )
        or article_b.get(
            "title",
            "",
        )
    )

    return keyword_overlap(
        title_a,
        title_b,
    )


# =========================================================
# LEXICAL SIMILARITY
# =========================================================

def calculate_similarity(
    article_a,
    article_b,
):
    title_score = (
        calculate_title_similarity(
            article_a,
            article_b,
        )
    )

    content_score = (
        calculate_content_similarity(
            article_a,
            article_b,
        )
    )

    overlap = (
        event_keyword_overlap(
            article_a,
            article_b,
        )
    )

    keyword_score = (
        overlap
        * 100
    )

    return (
        title_score * 0.65
        + content_score * 0.25
        + keyword_score * 0.10
    )


# =========================================================
# SAME EVENT
# =========================================================

def same_event(
    article_a,
    article_b,
):
    """
    Determine whether two articles represent the same
    underlying news event.

    Gates:
        1. Time compatibility
        2. Topic compatibility
        3. Lexical / semantic event similarity
    """

    # =====================================================
    # TIME GATE
    # =====================================================

    if not time_compatible(
        article_a,
        article_b,
    ):
        return False

    # =====================================================
    # TOPIC GATE
    # =====================================================

    if not categories_compatible(
        article_a,
        article_b,
    ):
        return False

    # =====================================================
    # LEXICAL SCORES
    # =====================================================

    title_score = (
        calculate_title_similarity(
            article_a,
            article_b,
        )
    )

    content_score = (
        calculate_content_similarity(
            article_a,
            article_b,
        )
    )

    overlap = (
        event_keyword_overlap(
            article_a,
            article_b,
        )
    )

    lexical_score = (
        calculate_similarity(
            article_a,
            article_b,
        )
    )

    # =====================================================
    # VERY STRONG LEXICAL MATCH
    # =====================================================

    if title_score >= 90:
        return True

    # =====================================================
    # NORMAL LEXICAL MATCH
    # =====================================================

    if (
        title_score
        >= TITLE_SIMILARITY_THRESHOLD
        and overlap
        >= MIN_KEYWORD_OVERLAP
        and lexical_score
        >= FINAL_SIMILARITY_THRESHOLD
    ):
        return True

    # =====================================================
    # STRONG CONTENT MATCH
    # =====================================================

    if (
        title_score >= 72
        and content_score >= 82
        and overlap >= 0.15
    ):
        return True

    # =====================================================
    # MULTILINGUAL SEMANTIC MATCH
    # =====================================================

    semantic_score = (
        calculate_semantic_similarity(
            article_a,
            article_b,
        )
    )

    # Extremely strong semantic similarity can stand on
    # its own AFTER time + topical compatibility gates.
    if (
        semantic_score
        >= SEMANTIC_STRONG_THRESHOLD
    ):
        return True

    # Normal semantic similarity requires at least one
    # supporting lexical/content signal.
    if (
        semantic_score
        >= SEMANTIC_NORMAL_THRESHOLD
        and (
            title_score >= 45
            or content_score >= 55
            or overlap >= 0.08
        )
    ):
        return True

    return False


# =========================================================
# CLUSTER COMPATIBILITY
# =========================================================

def cluster_compatible(
    article,
    cluster,
):
    """
    Determine whether an article belongs to an existing
    event cluster.

    The article does not need to match only the first
    cluster article.

    It can connect to an existing member representing the
    same event.

    For larger clusters, support from at least two members
    is required to reduce chain-merging.
    """

    articles = cluster.get(
        "articles",
        [],
    )

    if not articles:
        return (
            False,
            0.0,
        )

    best_score = 0.0
    matching_articles = 0

    # Limit comparisons for performance.
    comparison_articles = (
        articles[:6]
    )

    for existing_article in (
        comparison_articles
    ):
        if not same_event(
            article,
            existing_article,
        ):
            continue

        matching_articles += 1

        lexical_score = (
            calculate_similarity(
                article,
                existing_article,
            )
        )

        semantic_score = (
            calculate_semantic_similarity(
                article,
                existing_article,
            )
            * 100
        )

        best_score = max(
            best_score,
            lexical_score,
            semantic_score,
        )

    # No cluster member represents the same event.
    if matching_articles == 0:
        return (
            False,
            best_score,
        )

    # Small cluster:
    # one strong connection is sufficient.
    if len(articles) <= 2:
        return (
            True,
            best_score,
        )

    # Larger cluster:
    # require support from at least two members to reduce
    # accidental chain merging.
    if matching_articles >= 2:
        return (
            True,
            best_score,
        )

    return (
        False,
        best_score,
    )


# =========================================================
# MAIN CLUSTERING
# =========================================================

def cluster_articles(articles):
    """
    Group articles representing the same underlying event.

    Cluster objects intentionally contain the original
    articles only.

    Category/geography aggregation is handled elsewhere.
    """

    clusters = []

    for article in articles:
        best_cluster = None
        best_score = 0.0

        for cluster in clusters:
            if (
                len(
                    cluster.get(
                        "articles",
                        [],
                    )
                )
                >= MAX_CLUSTER_SIZE
            ):
                continue

            compatible, score = (
                cluster_compatible(
                    article,
                    cluster,
                )
            )

            if (
                compatible
                and score > best_score
            ):
                best_cluster = (
                    cluster
                )

                best_score = score

        if best_cluster is not None:
            best_cluster[
                "articles"
            ].append(
                article
            )

        else:
            clusters.append(
                {
                    "articles": [
                        article
                    ]
                }
            )

    return clusters