import re

from .regions import STATE_KEYWORDS


# =========================================================
# INDIA / NATIONAL SIGNALS
# =========================================================

INDIA_KEYWORDS = [
    "india",
    "indian",
    "new delhi",
    "delhi",
    "central government",
    "union government",
    "union cabinet",
    "parliament",
    "lok sabha",
    "rajya sabha",
    "supreme court of india",
    "prime minister of india",
    "president of india",
    "election commission of india",
    "reserve bank of india",
    "rbi",
]


INDIA_REGIONS = {
    "india",
    "national",
}


WORLD_REGIONS = {
    "world",
    "international",
    "global",
}
# =========================================================
# FOREIGN COUNTRY DETECTION
# =========================================================

FOREIGN_COUNTRIES = {
    "afghanistan",
    "albania",
    "algeria",
    "argentina",
    "armenia",
    "australia",
    "austria",
    "azerbaijan",
    "bangladesh",
    "belarus",
    "belgium",
    "bhutan",
    "bolivia",
    "brazil",
    "bulgaria",
    "canada",
    "chile",
    "china",
    "colombia",
    "croatia",
    "cuba",
    "cyprus",
    "czech republic",
    "denmark",
    "egypt",
    "england",
    "estonia",
    "ethiopia",
    "finland",
    "france",
    "georgia",
    "germany",
    "ghana",
    "greece",
    "hungary",
    "iceland",
    "indonesia",
    "iran",
    "iraq",
    "ireland",
    "israel",
    "italy",
    "japan",
    "jordan",
    "kazakhstan",
    "kenya",
    "kuwait",
    "kyrgyzstan",
    "latvia",
    "lebanon",
    "libya",
    "lithuania",
    "luxembourg",
    "malaysia",
    "maldives",
    "mexico",
    "mongolia",
    "morocco",
    "myanmar",
    "nepal",
    "netherlands",
    "new zealand",
    "nigeria",
    "north korea",
    "norway",
    "oman",
    "pakistan",
    "palestine",
    "peru",
    "philippines",
    "poland",
    "portugal",
    "qatar",
    "romania",
    "russia",
    "saudi arabia",
    "scotland",
    "serbia",
    "singapore",
    "slovakia",
    "slovenia",
    "south africa",
    "south korea",
    "spain",
    "sri lanka",
    "sudan",
    "sweden",
    "switzerland",
    "syria",
    "taiwan",
    "thailand",
    "turkey",
    "uganda",
    "uk",
    "ukraine",
    "united kingdom",
    "united states",
    "usa",
    "uae",
    "uruguay",
    "uzbekistan",
    "venezuela",
    "vietnam",
    "wales",
    "yemen",
    "zimbabwe",
}


# =========================================================
# BASIC HELPERS
# =========================================================

def normalize_value(value):
    if not value:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def normalize_state_name(state):
    return normalize_value(state)


def normalized_state_names():
    return {
        normalize_state_name(state)
        for state in STATE_KEYWORDS
    }


def get_article_text(article):
    """
    Prefer canonical English text when available.

    If canonicalization failed, fall back to the
    original title and summary.
    """

    title = (
        article.get("canonical_title")
        or article.get("title")
        or ""
    )

    summary = (
        article.get("canonical_summary")
        or article.get("summary")
        or ""
    )

    return f"{title} {summary}".lower()


def phrase_in_text(phrase, text):
    """
    Match complete words/phrases instead of arbitrary
    substrings.
    """

    if not phrase:
        return False

    phrase = str(
        phrase
    ).strip().lower()

    if not phrase:
        return False

    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return (
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
        is not None
    )


# =========================================================
# ARTICLE METADATA
# =========================================================

def get_region(article):
    """
    Actual story geography.

    This must NOT be confused with feed_region.
    """

    return normalize_value(
        article.get(
            "region",
            ""
        )
    )


def get_feed_region(article):
    """
    Geographic context of the feed/source.

    Example:

    TV9 Karnataka feed:
        feed_region = karnataka

    This does NOT prove every article is about Karnataka.
    """

    return normalize_value(
        article.get(
            "feed_region",
            ""
        )
    )


def get_categories(article):
    return {
        normalize_value(category)
        for category in article.get(
            "categories",
            []
        )
        if category
    }


def get_language(article):
    return normalize_value(
        article.get(
            "language",
            ""
        )
    )


# =========================================================
# STATE DETECTION
# =========================================================

def detect_indian_states(article):
    """
    Detect Indian states/UTs from:

    1. Actual story region, when already known.
    2. Canonical/original article text.

    IMPORTANT:
    feed_region is NOT automatically treated as the
    story's state.
    """

    detected_states = []

    known_states = (
        normalized_state_names()
    )

    # =====================================================
    # 1. ACTUAL STORY REGION
    # =====================================================

    region = get_region(
        article
    )

    if region in known_states:
        detected_states.append(
            region
        )

    # =====================================================
    # 2. ARTICLE TEXT
    # =====================================================

    text = get_article_text(
        article
    )

    for state, keywords in STATE_KEYWORDS.items():

        normalized_state = (
            normalize_state_name(
                state
            )
        )

        search_terms = []

        # -------------------------------------------------
        # CONFIGURED STATE/CITY KEYWORDS
        # -------------------------------------------------

        for keyword in keywords:

            if not keyword:
                continue

            keyword = (
                str(keyword)
                .strip()
                .lower()
            )

            if len(keyword) < 3:
                continue

            search_terms.append(
                keyword
            )

        # -------------------------------------------------
        # STATE NAME ITSELF
        # -------------------------------------------------

        state_text = (
            str(state)
            .replace("_", " ")
            .strip()
            .lower()
        )

        if state_text:
            search_terms.append(
                state_text
            )

        # -------------------------------------------------
        # MATCH
        # -------------------------------------------------

        matched = any(
            phrase_in_text(
                term,
                text,
            )
            for term in search_terms
        )

        if (
            matched
            and normalized_state
            not in detected_states
        ):
            detected_states.append(
                normalized_state
            )

    return detected_states
# =========================================================
# FOREIGN COUNTRY DETECTION
# =========================================================

def detect_foreign_countries(article):
    """
    Detect explicit foreign countries mentioned in the
    article title or summary.

    India is intentionally excluded because it has its own
    classification logic.
    """

    text = get_article_text(article)

    detected = []

    for country in FOREIGN_COUNTRIES:

        if phrase_in_text(
            country,
            text,
        ):
            detected.append(
                country
            )

    return detected

# =========================================================
# INDIA DETECTION
# =========================================================

def has_india_keyword(article):
    text = get_article_text(
        article
    )

    return any(
        phrase_in_text(
            keyword,
            text,
        )
        for keyword in INDIA_KEYWORDS
    )


def has_explicit_india_region(article):
    """
    Check actual story region only.

    feed_region is deliberately excluded.
    """

    region = get_region(
        article
    )

    if region in INDIA_REGIONS:
        return True

    if region in normalized_state_names():
        return True

    return False


def has_explicit_world_region(article):
    region = get_region(
        article
    )

    return region in WORLD_REGIONS


# =========================================================
# CATEGORY SIGNALS
# =========================================================

def has_world_category(article):
    categories = get_categories(
        article
    )

    return (
        "world" in categories
        or "international" in categories
        or "global" in categories
    )


def has_national_category(article):
    categories = get_categories(
        article
    )

    return (
        "national" in categories
        or "india" in categories
    )


# =========================================================
# FEED REGION SUPPORT
# =========================================================

def get_feed_state(article):
    """
    Return feed_region only when it represents an
    Indian state.

    This is WEAK supporting evidence.
    """

    feed_region = get_feed_region(
        article
    )

    if (
        feed_region
        in normalized_state_names()
    ):
        return feed_region

    return ""


def should_use_feed_state(article):
    """
    Determine whether a regional feed can be used as a
    fallback for state classification.

    feed_region is used only when stronger evidence
    does not indicate world/national/another state.

    This allows local Kannada headlines that contain no
    explicit 'Karnataka' word to remain useful while
    preventing obvious Egypt/India/world stories from
    automatically becoming Karnataka stories.
    """

    feed_state = get_feed_state(
        article
    )

    if not feed_state:
        return False

    # Explicit story geography always wins.
    if get_region(article):
        return False

    # Explicit world category beats feed context.
    if has_world_category(article):
        return False

    # Explicit national category beats feed context.
    if has_national_category(article):
        return False

    # India-wide textual evidence beats feed context.
    if has_india_keyword(article):
        return False

    detected_states = detect_indian_states(
        article
    )

    # Another state was explicitly detected in text.
    if (
        detected_states
        and feed_state
        not in detected_states
    ):
        return False

    return True


# =========================================================
# INDIA STORY
# =========================================================

def is_india_story(article):
    """
    Determine whether the story is Indian.

    Publisher identity is deliberately NOT used.

    NDTV / Indian Express / Hindustan Times can report
    international news, so publisher alone cannot make
    an article National.
    """

    if has_explicit_world_region(
        article
    ):
        return False

    if has_world_category(
        article
    ):
        return False

    if has_explicit_india_region(
        article
    ):
        return True

    if detect_indian_states(
        article
    ):
        return True

    if has_india_keyword(
        article
    ):
        return True

    if has_national_category(
        article
    ):
        return True

    return False


# =========================================================
# GEOGRAPHIC CLASSIFICATION
# =========================================================

def classify_geography(
    article,
    preferred_state,
):
    """
    Classify an article into:

        preferred_state
        other_state
        national
        world

    Evidence priority:

    1. Explicit actual story region
    2. Explicit world/national category
    3. State detection from article text
    4. India detection from article text
    5. Regional feed fallback
    6. World fallback

    Language NEVER determines geography.
    """

    preferred_state = (
        normalize_state_name(
            preferred_state
        )
    )

    region = get_region(
        article
    )

    known_states = (
        normalized_state_names()
    )

    # =====================================================
    # 1. EXPLICIT ACTUAL STATE REGION
    # =====================================================

    if region in known_states:

        if region == preferred_state:

            return {
                "scope":
                    "preferred_state",

                "states": [
                    region
                ],

                "evidence":
                    "explicit_story_region",
            }

        return {
            "scope":
                "other_state",

            "states": [
                region
            ],

            "evidence":
                "explicit_story_region",
        }

    # =====================================================
    # 2. EXPLICIT ACTUAL WORLD REGION
    # =====================================================

    if region in WORLD_REGIONS:

        return {
            "scope":
                "world",

            "states": [],

            "evidence":
                "explicit_story_region",
        }

    # =====================================================
    # 3. EXPLICIT ACTUAL NATIONAL REGION
    # =====================================================

    

    # =====================================================
    # 4. WORLD CATEGORY
    # =====================================================

    if has_world_category(
        article
    ):

        return {
            "scope":
                "world",

            "states": [],

            "evidence":
                "world_category",
        }

      # =====================================================
    # 5. FOREIGN COUNTRY DETECTION
    # =====================================================

    detected_countries = (
        detect_foreign_countries(
            article
        )
    )

    if detected_countries:

        return {
            "scope":
                "world",

            "states": [],

            "evidence":
                "foreign_country_text",
        }
    if region in INDIA_REGIONS:
    
            return {
                "scope":
                    "national",
    
                "states": [],
    
                "evidence":
                    "explicit_story_region",
            }

    # =====================================================
    # 6. TEXT-BASED STATE DETECTION
    # =====================================================

    detected_states = (
        detect_indian_states(
            article
        )
    )

    # -----------------------------------------------------
    # Exactly one state detected
    # -----------------------------------------------------

    if len(detected_states) == 1:

        detected_state = (
            detected_states[0]
        )

        if (
            preferred_state
            and detected_state
            == preferred_state
        ):

            return {
                "scope":
                    "preferred_state",

                "states":
                    detected_states,

                "evidence":
                    "single_state_text",
            }

        return {
            "scope":
                "other_state",

            "states":
                detected_states,

            "evidence":
                "single_state_text",
        }

    # -----------------------------------------------------
    # Multiple states detected
    #
    # Do not classify a multi-state story as the user's
    # preferred state merely because that state is one
    # of several locations mentioned.
    # -----------------------------------------------------

    if len(detected_states) > 1:

        return {
            "scope":
                "national",

            "states":
                detected_states,

            "evidence":
                "multi_state_text",
        }

    # =====================================================
    # 6. NATIONAL CATEGORY
    # =====================================================

    if has_national_category(
        article
    ):

        return {
            "scope":
                "national",

            "states": [],

            "evidence":
                "national_category",
        }

    # =====================================================
    # 7. INDIA TEXT
    # =====================================================

    if has_india_keyword(
        article
    ):

        return {
            "scope":
                "national",

            "states": [],

            "evidence":
                "india_text",
        }

    # =====================================================
    # 8. FEED-REGION FALLBACK
    # =====================================================

    if should_use_feed_state(
        article
    ):

        feed_state = get_feed_state(
            article
        )

        if (
            preferred_state
            and feed_state
            == preferred_state
        ):

            return {
                "scope":
                    "preferred_state",

                "states": [
                    feed_state
                ],

                "evidence":
                    "feed_region_fallback",
            }

        return {
            "scope":
                "other_state",

            "states": [
                feed_state
            ],

            "evidence":
                "feed_region_fallback",
        }

    # =====================================================
    # 9. DEFAULT WORLD
    # =====================================================

    return {
        "scope":
            "world",

        "states": [],

        "evidence":
            "default_world",
    }