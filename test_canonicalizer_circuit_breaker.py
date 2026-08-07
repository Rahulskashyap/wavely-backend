import news_v4.canonicalizer as canonicalizer


# =========================================================
# CONFIG
# =========================================================

ARTICLE_COUNT = 31


# =========================================================
# FAKE GEMINI
# =========================================================

gemini_call_count = 0


def fake_canonicalize_news_batch(articles):
    """
    Simulate Gemini returning a 429 on the first request.

    If the circuit breaker works, this function must
    NEVER be called a second time.
    """

    global gemini_call_count

    gemini_call_count += 1

    raise RuntimeError(
        "429 RESOURCE_EXHAUSTED: "
        "Quota exceeded for Gemini API"
    )


# =========================================================
# TEST ARTICLES
# =========================================================

def make_kannada_article(number):
    """
    Every article is deliberately unique so none are
    treated as same-run duplicates.
    """

    return {
        "title": (
            f"ಕರ್ನಾಟಕ ಸುದ್ದಿ ಪರೀಕ್ಷೆ {number}"
        ),
        "summary": (
            f"ಇದು ಪರೀಕ್ಷಾ ಸುದ್ದಿ ಸಂಖ್ಯೆ {number}"
        ),
        "url": (
            f"https://example.com/"
            f"kannada/{number}"
        ),
    }


articles = [
    make_kannada_article(number)
    for number in range(
        1,
        ARTICLE_COUNT + 1,
    )
]


# =========================================================
# ISOLATE TEST FROM REAL CACHE
# =========================================================

original_load_cache = (
    canonicalizer.load_cache
)

original_save_cache = (
    canonicalizer.save_cache
)

original_gemini_function = (
    canonicalizer.canonicalize_news_batch
)


def fake_load_cache():
    return {}


def fake_save_cache(cache):
    # Nothing should be written to the real cache.
    pass


# =========================================================
# RUN TEST
# =========================================================

try:

    canonicalizer.load_cache = (
        fake_load_cache
    )

    canonicalizer.save_cache = (
        fake_save_cache
    )

    canonicalizer.canonicalize_news_batch = (
        fake_canonicalize_news_batch
    )

    canonicalizer.reset_gemini_circuit_breaker()

    print(
        "\n=============================="
    )
    print(
        "CANONICALIZER CIRCUIT "
        "BREAKER TEST"
    )
    print(
        "=============================="
    )

    result = (
        canonicalizer.canonicalize_articles(
            articles
        )
    )

finally:

    # Always restore module functions, even if the
    # test itself throws an unexpected exception.

    canonicalizer.load_cache = (
        original_load_cache
    )

    canonicalizer.save_cache = (
        original_save_cache
    )

    canonicalizer.canonicalize_news_batch = (
        original_gemini_function
    )


# =========================================================
# RESULTS
# =========================================================

canonicalized_count = sum(
    1
    for article in result
    if article.get(
        "canonicalized",
        False,
    )
)

fallback_count = (
    ARTICLE_COUNT
    - canonicalized_count
)


print(
    "\n=============================="
)
print(
    "RESULT"
)
print(
    "=============================="
)

print(
    "ARTICLES:",
    ARTICLE_COUNT,
)

print(
    "BATCH SIZE:",
    canonicalizer.BATCH_SIZE,
)

print(
    "GEMINI CALLS:",
    gemini_call_count,
)

print(
    "CANONICALIZED:",
    canonicalized_count,
)

print(
    "FALLBACK:",
    fallback_count,
)

print(
    "GEMINI AVAILABLE:",
    canonicalizer.GEMINI_AVAILABLE,
)


# =========================================================
# ASSERTIONS
# =========================================================

failures = []


if gemini_call_count != 1:

    failures.append(
        "Gemini should have been called "
        "exactly once."
    )


if canonicalizer.GEMINI_AVAILABLE:

    failures.append(
        "Circuit breaker should be active "
        "after simulated 429."
    )


if canonicalized_count != 0:

    failures.append(
        "No articles should be canonicalized "
        "after simulated Gemini failure."
    )


if fallback_count != ARTICLE_COUNT:

    failures.append(
        "All articles should safely fall back "
        "to original text."
    )


for article in result:

    if (
        article.get("canonical_title")
        != article.get("title")
    ):

        failures.append(
            "Fallback canonical title does not "
            "match original title."
        )

        break


# =========================================================
# FINAL
# =========================================================

print(
    "\n=============================="
)
print(
    "FINAL"
)
print(
    "=============================="
)


if failures:

    for failure in failures:
        print(
            "FAIL:",
            failure,
        )

    raise SystemExit(1)


print(
    "PASS: FIRST BATCH ATTEMPTED"
)

print(
    "PASS: SIMULATED 429 DETECTED"
)

print(
    "PASS: CIRCUIT BREAKER ACTIVATED"
)

print(
    "PASS: REMAINING BATCHES SKIPPED"
)

print(
    "PASS: ORIGINAL TEXT USED AS FALLBACK"
)

print(
    "\nALL CIRCUIT BREAKER TESTS PASSED"
)