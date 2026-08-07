from .regions import STATE_KEYWORDS

INDIA_KEYWORDS = [
    "india",
    "indian",
    "new delhi",
    "central government",
    "union government",
    "parliament",
    "supreme court of india",
    "prime minister of india",
]


def get_article_text(article):
    """
    Prefer canonical English text when available.
    """

    title = (
        article.get("canonical_title")
        or article.get("title", "")
    )

    summary = (
        article.get("canonical_summary")
        or article.get("summary", "")
    )

    return f"{title} {summary}".lower()


def normalize_state_name(state):
    """
    Normalize state identifiers so values such as
    Karnataka, KARNATAKA and karnataka compare equally.
    """

    if not state:
        return ""

    return (
        str(state)
        .strip()
        .lower()
        .replace(" ", "_")
    )


def detect_indian_states(article):
    """
    Return every Indian state/UT detected from:

    1. Article region metadata
    2. Canonical/original article text

    State names are returned in normalized form:
    karnataka
    tamil_nadu
    maharashtra
    etc.
    """

    text = get_article_text(article)

    detected_states = []

    # -----------------------------------------
    # 1. CHECK REGION METADATA
    # -----------------------------------------

    article_region = normalize_state_name(
        article.get("region", "")
    )

    normalized_state_names = {
        normalize_state_name(state)
        for state in STATE_KEYWORDS
    }

    if article_region in normalized_state_names:
        detected_states.append(article_region)

    # -----------------------------------------
    # 2. CHECK ARTICLE TEXT
    # -----------------------------------------

    for state, keywords in STATE_KEYWORDS.items():

        normalized_state = normalize_state_name(
            state
        )

        normalized_keywords = [
            str(keyword).lower()
            for keyword in keywords
        ]

        if any(
            keyword in text
            for keyword in normalized_keywords
        ):
            if normalized_state not in detected_states:
                detected_states.append(
                    normalized_state
                )

    return detected_states


def is_india_story(article):
    text = get_article_text(article)

    if any(
        keyword in text
        for keyword in INDIA_KEYWORDS
    ):
        return True

    if detect_indian_states(article):
        return True

    return False


def classify_geography(
    article,
    preferred_state,
):
    """
    Geography priority:

    preferred_state
        -> other_state
        -> national
        -> world
    """

    preferred_state = normalize_state_name(
        preferred_state
    )

    detected_states = detect_indian_states(
        article
    )

    # -----------------------------------------
    # USER'S SELECTED STATE
    # -----------------------------------------

    if preferred_state in detected_states:
        return {
            "scope": "preferred_state",
            "states": detected_states,
        }

    # -----------------------------------------
    # ANOTHER INDIAN STATE
    # -----------------------------------------

    if detected_states:
        return {
            "scope": "other_state",
            "states": detected_states,
        }

    # -----------------------------------------
    # INDIA / NATIONAL
    # -----------------------------------------

    if is_india_story(article):
        return {
            "scope": "national",
            "states": [],
        }

    # -----------------------------------------
    # WORLD
    # -----------------------------------------

    return {
        "scope": "world",
        "states": [],
    }