import re


# =========================================================
# NUMBER NORMALIZATION
# =========================================================

NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
}


def normalize_number_words(text):
    if not text:
        return ""

    pattern = (
        r"\b("
        + "|".join(NUMBER_WORDS.keys())
        + r")\b"
    )

    def replace(match):
        return NUMBER_WORDS[
            match.group(0).lower()
        ]

    return re.sub(
        pattern,
        replace,
        text,
        flags=re.IGNORECASE,
    )


# =========================================================
# NUMBERS
# =========================================================

def extract_numbers(text):
    if not text:
        return []

    text = normalize_number_words(text)

    numbers = re.findall(
        r"\b\d+(?:,\d{3})*(?:\.\d+)?\b",
        text,
    )

    return list(
        dict.fromkeys(
            number.replace(",", "")
            for number in numbers
        )
    )


# =========================================================
# PERCENTAGES
# =========================================================

def extract_percentages(text):
    if not text:
        return []

    values = re.findall(
        r"\b\d+(?:\.\d+)?\s*%",
        text,
    )

    return [
        value.replace(" ", "")
        for value in values
    ]


# =========================================================
# MONEY NORMALIZATION
# =========================================================

MONEY_MULTIPLIERS = {
    "k": 1_000,
    "thousand": 1_000,

    "m": 1_000_000,
    "million": 1_000_000,

    "bn": 1_000_000_000,
    "billion": 1_000_000_000,

    "trillion": 1_000_000_000_000,

    "lakh": 100_000,
    "crore": 10_000_000,
}


CURRENCY_NAMES = {
    "$": "USD",
    "us$": "USD",
    "usd": "USD",

    "₹": "INR",
    "rs": "INR",
    "rs.": "INR",
    "inr": "INR",

    "£": "GBP",
    "gbp": "GBP",

    "€": "EUR",
    "eur": "EUR",
}


def extract_money(text):
    """
    Returns normalized monetary claims.

    $5.5bn
    $5.5 billion

    both become:

    USD:5500000000
    """

    if not text:
        return []

    pattern = re.compile(
        r"""
        (?P<currency>
            US\$|
            \$|
            ₹|
            Rs\.?|
            INR|
            £|
            GBP|
            €|
            EUR
        )
        \s*
        (?P<number>
            \d+(?:,\d{3})*(?:\.\d+)?
        )
        \s*
        (?P<unit>
            trillion|
            billion|
            million|
            thousand|
            crore|
            lakh|
            bn|
            m|
            k
        )?
        """,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    results = []

    for match in pattern.finditer(text):

        currency_raw = (
            match.group("currency")
            .lower()
        )

        number_raw = (
            match.group("number")
            .replace(",", "")
        )

        unit_raw = match.group("unit")

        currency = CURRENCY_NAMES.get(
            currency_raw,
            currency_raw.upper(),
        )

        try:
            value = float(number_raw)
        except ValueError:
            continue

        if unit_raw:
            multiplier = MONEY_MULTIPLIERS.get(
                unit_raw.lower(),
                1,
            )

            value *= multiplier

        if value.is_integer():
            value = int(value)

        results.append(
            f"{currency}:{value}"
        )

    return list(dict.fromkeys(results))


# =========================================================
# TIME EXPRESSIONS
# =========================================================

def extract_time_expressions(text):
    if not text:
        return []

    patterns = [
        r"\btoday\b",
        r"\byesterday\b",
        r"\btomorrow\b",

        r"\bmonday\b",
        r"\btuesday\b",
        r"\bwednesday\b",
        r"\bthursday\b",
        r"\bfriday\b",
        r"\bsaturday\b",
        r"\bsunday\b",

        r"\b\d{1,2}:\d{2}\s*(?:am|pm)?\b",
    ]

    results = []

    for pattern in patterns:
        results.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE,
            )
        )

    return list(
        dict.fromkeys(
            result.lower()
            for result in results
        )
    )


# =========================================================
# ACTIONS
# =========================================================

ACTION_GROUPS = {

    "death": [
        "killed",
        "dies",
        "died",
        "dead",
        "death",
        "deaths",
    ],

    "injury": [
        "injured",
        "wounded",
    ],

    "arrest": [
        "arrested",
        "detained",
        "held",
    ],

    "resignation": [
        "resigned",
        "resigns",
        "quit",
        "steps down",
        "stepped down",
    ],

    "approval": [
        "approved",
        "approves",
        "accepted",
        "cleared",
        "green signal",
        "green light",
    ],

    "rejection": [
        "rejected",
        "rejects",
        "denied",
        "blocked",
    ],

    "announcement": [
        "announced",
        "announces",
        "unveiled",
        "revealed",
    ],

    "launch": [
        "launched",
        "launches",
        "introduced",
    ],

    "attack": [
        "attacked",
        "attack",
        "struck",
        "strike",
        "bombed",
    ],

    "increase": [
        "increased",
        "increase",
        "rose",
        "rises",
        "surged",
        "surges",
        "jumped",
        "gained",
    ],

    "decrease": [
        "decreased",
        "decrease",
        "fell",
        "falls",
        "dropped",
        "declined",
        "slumped",
    ],

    "victory": [
        "won",
        "wins",
        "victory",
        "defeated",
        "beats",
        "beat",
    ],

    "loss": [
        "lost",
        "loses",
        "defeat",
    ],

    "settlement": [
        "settlement",
        "settle",
        "settles",
        "settled",
    ],

    "lawsuit": [
        "lawsuit",
        "lawsuits",
        "case",
        "cases",
    ],

    "warning": [
        "warning",
        "warned",
        "warns",
        "advisory",
        "alert",
    ],

    "earthquake": [
        "earthquake",
        "quake",
        "tremor",
    ],

    "election": [
        "election",
        "elections",
        "poll",
        "polls",
        "voting",
    ],
}


def extract_actions(text):
    """
    Return normalized concepts directly.

    killed -> death
    died   -> death

    settlement -> settlement
    settle     -> settlement
    """

    if not text:
        return []

    lowered = text.lower()

    found = []

    for concept, phrases in (
        ACTION_GROUPS.items()
    ):

        for phrase in phrases:

            pattern = (
                r"\b"
                + re.escape(phrase)
                + r"\b"
            )

            if re.search(
                pattern,
                lowered,
            ):

                found.append(concept)
                break

    return list(dict.fromkeys(found))


# =========================================================
# DIRECTION / CONTRADICTION SIGNALS
# =========================================================

CONFLICT_GROUPS = {

    "financial_result": {

        "positive": [
            "profit",
            "profits",
            "gain",
            "gains",
        ],

        "negative": [
            "loss",
            "losses",
            "deficit",
        ],
    },

    "movement": {

        "positive": [
            "rose",
            "rise",
            "rises",
            "increased",
            "increase",
            "surged",
            "surge",
            "gained",
            "jumped",
        ],

        "negative": [
            "fell",
            "fall",
            "falls",
            "decreased",
            "decrease",
            "dropped",
            "drop",
            "declined",
            "slumped",
        ],
    },

    "decision": {

        "positive": [
            "approved",
            "accepted",
            "cleared",
        ],

        "negative": [
            "rejected",
            "denied",
            "blocked",
        ],
    },

    "result": {

        "positive": [
            "won",
            "wins",
            "victory",
            "defeated",
            "beat",
            "beats",
        ],

        "negative": [
            "lost",
            "loses",
            "defeat",
        ],
    },
}


def extract_directions(text):
    if not text:
        return {}

    lowered = text.lower()

    directions = {}

    for group, sides in (
        CONFLICT_GROUPS.items()
    ):

        positive_found = any(
            re.search(
                rf"\b{re.escape(word)}\b",
                lowered,
            )
            for word in sides["positive"]
        )

        negative_found = any(
            re.search(
                rf"\b{re.escape(word)}\b",
                lowered,
            )
            for word in sides["negative"]
        )

        if (
            positive_found
            and not negative_found
        ):
            directions[group] = "positive"

        elif (
            negative_found
            and not positive_found
        ):
            directions[group] = "negative"

        elif (
            positive_found
            and negative_found
        ):
            directions[group] = "mixed"

    return directions


# =========================================================
# IMPORTANT PHRASES / ENTITY-LIKE SIGNALS
# =========================================================

ENTITY_STOPWORDS = {
    "the",
    "this",
    "that",
    "after",
    "before",
    "new",
    "news",
    "latest",
    "live",
    "today",
}


def extract_entities(text):
    """
    Lightweight V2 entity extraction.

    This is NOT full NLP NER yet.

    It extracts capitalized names such as:

    Johnson & Johnson
    Rahul Gandhi
    Pralhad Joshi
    Sri Lanka

    Useful as another corroboration signal.
    """

    if not text:
        return []

    pattern = re.compile(
        r"""
        \b
        (?:
            [A-Z][A-Za-z.'&-]*
            (?:\s+|&\s*)
        )*
        [A-Z][A-Za-z.'&-]*
        \b
        """,
        flags=re.VERBOSE,
    )

    results = []

    for match in pattern.finditer(text):

        entity = re.sub(
            r"\s+",
            " ",
            match.group(0),
        ).strip()

        if len(entity) < 3:
            continue

        if entity.lower() in ENTITY_STOPWORDS:
            continue

        results.append(
            entity.lower()
        )

    return list(dict.fromkeys(results))


# =========================================================
# MAIN CLAIM EXTRACTOR
# =========================================================

def extract_claims(article):

    title = article.get(
        "title",
        "",
    )

    summary = article.get(
        "summary",
        "",
    )

    text = f"{title} {summary}"

    return {

        "title": title,

        "publisher_id":
            article.get(
                "publisher_id"
            ),

        "source_name":
            article.get(
                "source_name"
            ),

        "numbers":
            extract_numbers(text),

        "percentages":
            extract_percentages(text),

        "money":
            extract_money(text),

        "time_expressions":
            extract_time_expressions(text),

        "actions":
            extract_actions(text),

        "directions":
            extract_directions(text),

        "entities":
            extract_entities(text),
    }
