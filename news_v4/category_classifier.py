import re
from collections import Counter


# =========================================================
# CONFIG
# =========================================================

VALID_CATEGORIES = {
    "politics",
    "business",
    "technology",
    "sports",
    "entertainment",
    "health",
    "science",
    "crime",
    "weather",
    "education",
    "general",
}


# Geography labels are metadata, not topical categories.
GEOGRAPHY_LABELS = {
    "state",
    "local",
    "national",
    "india",
    "world",
    "international",
    "global",
}


CATEGORY_ALIASES = {
    "sport": "sports",
    "cricket": "sports",
    "football": "sports",
    "soccer": "sports",
    "tennis": "sports",
    "badminton": "sports",
    "hockey": "sports",

    "economy": "business",
    "economic": "business",
    "finance": "business",
    "financial": "business",
    "markets": "business",
    "market": "business",

    "tech": "technology",
    "ai": "technology",
    "artificial_intelligence": "technology",

    "space": "science",

    "political": "politics",
    "government": "politics",
    "policy": "politics",
    "election": "politics",
    "elections": "politics",

    "movie": "entertainment",
    "movies": "entertainment",
    "film": "entertainment",
    "films": "entertainment",
    "cinema": "entertainment",
    "television": "entertainment",
    "tv": "entertainment",

    "healthcare": "health",
    "medical": "health",
    "medicine": "health",

    "crime_news": "crime",

    "climate": "weather",

    "schools": "education",
    "school": "education",
    "college": "education",
    "universities": "education",
    "university": "education",
}


# =========================================================
# KEYWORDS
# =========================================================

CATEGORY_KEYWORDS = {
   "politics": {
    "parliament",
    "minister",
    "prime minister",
    "chief minister",
    "cabinet",
    "election",
    "elections",
    "electoral",
    "political",
    "politics",
    "legislation",
    "legislature",
    "mp",
    "mla",
    "president",
    "governor",
    "government policy",
    "public policy",
    "political policy",
    "election policy",
},
    "business": {
        "economy",
        "economic",
        "business",
        "finance",
        "financial",
        "market",
        "markets",
        "stock market",
        "sensex",
        "nifty",
        "rbi",
        "reserve bank",
        "inflation",
        "gdp",
        "revenue",
        "profit",
        "profits",
        "company",
        "companies",
        "startup",
        "startups",
        "investment",
        "investor",
        "investors",
        "bank",
        "banking",
    },

    "technology": {
        "technology",
        "tech",
        "artificial intelligence",
        " ai ",
        "machine learning",
        "software",
        "cybersecurity",
        "cyber security",
        "computer",
        "smartphone",
        "android",
        "iphone",
        "apple",
        "google",
        "microsoft",
        "openai",
        "chip",
        "semiconductor",
        "robot",
        "robotics",
        "digital",
    },

    "sports": {
        "sport",
        "sports",
        "cricket",
        "football",
        "soccer",
        "tennis",
        "badminton",
        "hockey",
        "ipl",
        "bcci",
        "icc",
        "test match",
        "odi",
        "t20",
        "world cup",
        "tournament",
        "match",
        "captain",
        "coach",
        "wicket",
        "innings",
        "goal",
        "league",
    },

    "entertainment": {
        "entertainment",
        "movie",
        "movies",
        "film",
        "films",
        "cinema",
        "actor",
        "actress",
        "director",
        "bollywood",
        "hollywood",
        "television",
        "tv show",
        "series",
        "singer",
        "music",
        "album",
        "box office",
        "ott",
    },

    "health": {
        "health",
        "healthcare",
        "hospital",
        "medical",
        "medicine",
        "doctor",
        "doctors",
        "patient",
        "patients",
        "disease",
        "virus",
        "vaccine",
        "vaccination",
        "infection",
        "cancer",
        "treatment",
        "surgery",
        "public health",
    },

    "science": {
        "science",
        "scientist",
        "scientists",
        "research",
        "researchers",
        "space",
        "nasa",
        "isro",
        "satellite",
        "rocket",
        "mission",
        "astronomy",
        "planet",
        "moon",
        "mars",
        "asteroid",
        "telescope",
    },

    "crime": {
        "crime",
        "police",
        "arrest",
        "arrested",
        "murder",
        "killed",
        "killing",
        "robbery",
        "theft",
        "fraud",
        "scam",
        "accused",
        "suspect",
        "investigation",
        "raid",
        "raided",
        "court",
        "convicted",
        "conviction",
        "charges",
        "terror",
        "terrorism",
        "attack",
    },

    "weather": {
        "weather",
        "rain",
        "rainfall",
        "heavy rain",
        "monsoon",
        "storm",
        "cyclone",
        "flood",
        "flooding",
        "temperature",
        "heatwave",
        "heat wave",
        "cold wave",
        "thunderstorm",
        "forecast",
        "imd",
        "meteorological",
    },

    "education": {
        "education",
        "school",
        "schools",
        "student",
        "students",
        "college",
        "colleges",
        "university",
        "universities",
        "exam",
        "exams",
        "teacher",
        "teachers",
        "academic",
        "admission",
        "admissions",
        "curriculum",
    },
}


# =========================================================
# NORMALIZATION
# =========================================================

def normalize(value):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .lower()
    )


def normalize_category(value):
    return (
        normalize(value)
        .replace("-", "_")
        .replace(" ", "_")
    )


def canonical_category(value):
    category = normalize_category(
        value
    )

    if not category:
        return None

    if category in GEOGRAPHY_LABELS:
        return None

    category = CATEGORY_ALIASES.get(
        category,
        category,
    )

    if category in VALID_CATEGORIES:
        return category

    return None


# =========================================================
# ARTICLE TEXT
# =========================================================

def get_article_text(article):
    """
    Prefer canonical English text when available.

    Original title/summary/body remain available as
    additional evidence.
    """

    parts = []

    canonical_title = normalize(
        article.get(
            "canonical_title"
        )
    )

    canonical_summary = normalize(
        article.get(
            "canonical_summary"
        )
    )

    title = normalize(
        article.get(
            "title"
        )
    )

    summary = normalize(
        article.get(
            "summary"
        )
    )

    body = normalize(
        article.get(
            "article_body"
        )
    )

    section = normalize(
        article.get(
            "article_section"
        )
    )

    if canonical_title:
        parts.append(
            canonical_title
        )

    if canonical_summary:
        parts.append(
            canonical_summary
        )

    if title:
        parts.append(
            title
        )

    if summary:
        parts.append(
            summary
        )

    if section:
        parts.append(
            section
        )

    # Article body can be very large.
    if body:
        parts.append(
            body[:3000]
        )

    return " ".join(parts)


# =========================================================
# KEYWORD MATCHING
# =========================================================

def keyword_present(
    text,
    keyword,
):
    """
    Match phrases and individual words conservatively.
    """

    keyword = normalize(
        keyword
    )

    if not keyword:
        return False

    if " " in keyword:
        return keyword in text

    pattern = (
        r"\b"
        + re.escape(keyword)
        + r"\b"
    )

    return (
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
        is not None
    )


def get_keyword_scores(text):
    scores = Counter()

    for category, keywords in (
        CATEGORY_KEYWORDS.items()
    ):

        for keyword in keywords:

            if keyword_present(
                text,
                keyword,
            ):
                scores[
                    category
                ] += 1

    return scores


# =========================================================
# SOURCE CATEGORY EVIDENCE
# =========================================================

def get_source_category_scores(
    article,
):
    scores = Counter()

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
        return scores

    for category in categories:

        canonical = (
            canonical_category(
                category
            )
        )

        if canonical:
            scores[
                canonical
            ] += 1

    return scores


# =========================================================
# CLASSIFICATION
# =========================================================

def classify_article_category(
    article,
):
    """
    Determine one primary topical category.

    Text evidence is primary.

    Publisher/source categories are supporting evidence,
    not absolute truth.
    """

    text = get_article_text(
        article
    )

    keyword_scores = (
        get_keyword_scores(
            text
        )
    )

    source_scores = (
        get_source_category_scores(
            article
        )
    )

    final_scores = Counter()

    # Actual article text gets stronger weight.
    for category, score in (
        keyword_scores.items()
    ):
        final_scores[
            category
        ] += score * 3

    # Feed/source metadata is supporting evidence.
    for category, score in (
        source_scores.items()
    ):
        final_scores[
            category
        ] += score

    if not final_scores:
        return {
            "category":
                "general",

            "categories": [
                "general"
            ],

            "category_confidence":
                "low",

            "category_scores": {},
        }

    ranked = sorted(
        final_scores.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    )

    best_category = (
        ranked[0][0]
    )

    best_score = (
        ranked[0][1]
    )

    second_score = (
        ranked[1][1]
        if len(ranked) > 1
        else 0
    )

    if best_score >= 6:
        confidence = "high"

    elif best_score >= 3:
        confidence = "medium"

    else:
        confidence = "low"

    # Only expose a secondary category when it has
    # meaningful evidence and is close to the winner.
    final_categories = [
        best_category
    ]

    if len(ranked) > 1:

        second_category = (
            ranked[1][0]
        )

        if (
            second_score >= 3
            and second_score
            >= best_score * 0.75
        ):
            final_categories.append(
                second_category
            )

    return {
        "category":
            best_category,

        "categories":
            final_categories[:2],

        "category_confidence":
            confidence,

        "category_scores":
            dict(ranked),
    }


# =========================================================
# APPLY TO ARTICLE
# =========================================================

def classify_article(
    article,
):
    """
    Classify an article while preserving the original
    feed/source categories separately.
    """

    original_categories = (
        article.get(
            "categories",
            [],
        )
    )

    if isinstance(
        original_categories,
        str,
    ):
        original_categories = [
            original_categories
        ]

    article[
        "source_categories"
    ] = list(
        original_categories
        or []
    )

    result = (
        classify_article_category(
            article
        )
    )

    article[
        "category"
    ] = result[
        "category"
    ]

    article[
        "categories"
    ] = result[
        "categories"
    ]

    article[
        "category_confidence"
    ] = result[
        "category_confidence"
    ]

    article[
        "category_scores"
    ] = result[
        "category_scores"
    ]

    return article


# =========================================================
# BATCH
# =========================================================

def classify_articles(
    articles,
):
    print("\n==============================")
    print("CATEGORY CLASSIFICATION")
    print("==============================")

    category_counts = Counter()

    for article in articles:

        classify_article(
            article
        )

        category_counts[
            article.get(
                "category",
                "general",
            )
        ] += 1

    print(
        "Articles:",
        len(articles),
    )

    print("\nCATEGORY COUNTS")

    for category, count in sorted(
        category_counts.items()
    ):
        print(
            f"{category}: {count}"
        )

    return articles