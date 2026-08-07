# news_v4/canonicalizer.py

import hashlib
import json
import re
from pathlib import Path

from gemini_service import canonicalize_news_batch


# =========================================================
# CONFIG
# =========================================================

BATCH_SIZE = 15
CACHE_VERSION = 1

CACHE_DIR = (
    Path(__file__).resolve().parent
    / "cache"
)

CACHE_FILE = (
    CACHE_DIR
    / "canonicalization_cache.json"
)


# =========================================================
# GEMINI RUN STATE
# =========================================================

# Circuit breaker is intentionally in-memory.
# A new Python process gets another chance to use Gemini.
GEMINI_AVAILABLE = True
GEMINI_DISABLED_REASON = None


def reset_gemini_circuit_breaker():
    """
    Mainly useful for tests.
    """

    global GEMINI_AVAILABLE
    global GEMINI_DISABLED_REASON

    GEMINI_AVAILABLE = True
    GEMINI_DISABLED_REASON = None


def disable_gemini(reason):
    global GEMINI_AVAILABLE
    global GEMINI_DISABLED_REASON

    GEMINI_AVAILABLE = False
    GEMINI_DISABLED_REASON = str(
        reason
        or "Gemini unavailable"
    )


# =========================================================
# GEMINI ERROR DETECTION
# =========================================================

def is_quota_or_rate_limit_error(error):
    """
    Detect errors where retrying every remaining batch
    during this run would be wasteful.
    """

    text = str(
        error
        or ""
    ).lower()

    signals = (
        "429",
        "resource_exhausted",
        "resource exhausted",
        "quota exceeded",
        "rate limit",
        "rate_limit",
        "too many requests",
    )

    return any(
        signal in text
        for signal in signals
    )


# =========================================================
# LANGUAGE CHECK
# =========================================================

def contains_kannada(text):
    if not text:
        return False

    return bool(
        re.search(
            r"[\u0C80-\u0CFF]",
            str(text),
        )
    )


def needs_canonicalization(article):
    title = article.get(
        "title",
        "",
    )

    summary = article.get(
        "summary",
        "",
    )

    return contains_kannada(
        f"{title} {summary}"
    )


# =========================================================
# DEFAULT CANONICAL VALUES
# =========================================================

def set_original_as_canonical(article):
    article[
        "canonical_title"
    ] = str(
        article.get(
            "title",
            "",
        )
        or ""
    )

    article[
        "canonical_summary"
    ] = str(
        article.get(
            "summary",
            "",
        )
        or ""
    )

    article[
        "canonicalized"
    ] = False

    article[
        "canonicalization_source"
    ] = "original"

    return article


# =========================================================
# CACHE KEY
# =========================================================

def normalize_cache_text(value):
    value = str(
        value
        or ""
    ).strip()

    return re.sub(
        r"\s+",
        " ",
        value,
    )


def build_cache_key(article):
    title = normalize_cache_text(
        article.get(
            "title",
            "",
        )
    )

    summary = normalize_cache_text(
        article.get(
            "summary",
            "",
        )
    )

    raw = (
        f"v{CACHE_VERSION}\n"
        f"{title}\n"
        f"{summary}"
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


# =========================================================
# CACHE
# =========================================================

def load_cache():
    if not CACHE_FILE.exists():
        return {}

    try:
        with CACHE_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(
                file
            )

        if isinstance(
            data,
            dict,
        ):
            return data

    except Exception as error:
        print(
            "Canonicalization cache "
            "load warning:",
            error,
        )

    return {}


def save_cache(cache):
    try:
        CACHE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_file = (
            CACHE_FILE.with_suffix(
                ".tmp"
            )
        )

        with temporary_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                cache,
                file,
                ensure_ascii=False,
                indent=2,
            )

        temporary_file.replace(
            CACHE_FILE
        )

    except Exception as error:
        print(
            "Canonicalization cache "
            "save warning:",
            error,
        )


# =========================================================
# APPLY RESULT
# =========================================================

def apply_canonical_result(
    article,
    canonical_title,
    canonical_summary,
    source,
):
    canonical_title = str(
        canonical_title
        or ""
    ).strip()

    canonical_summary = str(
        canonical_summary
        or ""
    ).strip()

    if not canonical_title:
        return False

    article[
        "canonical_title"
    ] = canonical_title

    article[
        "canonical_summary"
    ] = canonical_summary

    article[
        "canonicalized"
    ] = True

    article[
        "canonicalization_source"
    ] = source

    return True


def apply_cached_result(
    article,
    cached,
):
    if not isinstance(
        cached,
        dict,
    ):
        return False

    return apply_canonical_result(
        article,
        cached.get(
            "canonical_title",
            "",
        ),
        cached.get(
            "canonical_summary",
            "",
        ),
        "cache",
    )


# =========================================================
# GEMINI BATCH
# =========================================================

def process_batch(
    batch,
    cache,
):
    """
    Returns:
        successful_count,
        cache_changed
    """

    if not batch:
        return 0, False

    # Circuit already open.
    if not GEMINI_AVAILABLE:
        print(
            "Gemini skipped for "
            f"{len(batch)} articles: "
            "circuit breaker active."
        )

        return 0, False

    print(
        f"Canonicalizing {len(batch)} "
        "uncached articles..."
    )

    try:
        results = canonicalize_news_batch(
            batch
        )

    except Exception as error:
        print(
            "Canonicalization Gemini error:",
            error,
        )

        if is_quota_or_rate_limit_error(
            error
        ):
            disable_gemini(
                error
            )

            print(
                "Gemini circuit breaker activated."
            )

            print(
                "Remaining uncached articles "
                "will use original text."
            )

        return 0, False

    if not isinstance(
        results,
        list,
    ):
        print(
            "Canonicalization warning: "
            "invalid Gemini result."
        )

        return 0, False

    result_map = {}

    for result in results:
        if not isinstance(
            result,
            dict,
        ):
            continue

        result_id = result.get(
            "id"
        )

        try:
            result_id = int(
                result_id
            )

        except (
            TypeError,
            ValueError,
        ):
            continue

        result_map[
            result_id
        ] = result

    successful = 0
    cache_changed = False

    for index, article in enumerate(
        batch
    ):
        result = result_map.get(
            index
        )

        if not result:
            continue

        canonical_title = str(
            result.get(
                "canonical_title",
                "",
            )
            or ""
        ).strip()

        canonical_summary = str(
            result.get(
                "canonical_summary",
                "",
            )
            or ""
        ).strip()

        if not canonical_title:
            continue

        if not apply_canonical_result(
            article,
            canonical_title,
            canonical_summary,
            "gemini",
        ):
            continue

        cache_key = build_cache_key(
            article
        )

        cache[
            cache_key
        ] = {
            "canonical_title":
                canonical_title,

            "canonical_summary":
                canonical_summary,
        }

        successful += 1
        cache_changed = True

    return (
        successful,
        cache_changed,
    )


# =========================================================
# SAME-RUN DUPLICATE REUSE
# =========================================================

def copy_canonicalization(
    source_article,
    target_article,
):
    if not source_article.get(
        "canonicalized",
        False,
    ):
        return False

    return apply_canonical_result(
        target_article,
        source_article.get(
            "canonical_title",
            "",
        ),
        source_article.get(
            "canonical_summary",
            "",
        ),
        "same_run_cache",
    )


# =========================================================
# MAIN
# =========================================================

def canonicalize_articles(articles):
    print(
        "\n=============================="
    )
    print("CANONICALIZATION")
    print(
        "=============================="
    )

    if not articles:
        print("Articles: 0")
        return articles

    cache = load_cache()

    pending_unique = []
    representatives = {}
    duplicates = {}

    need_count = 0
    cache_hits = 0
    same_run_duplicates = 0

    # =====================================================
    # PREPARE
    # =====================================================

    for article in articles:
        set_original_as_canonical(
            article
        )

        if not needs_canonicalization(
            article
        ):
            continue

        need_count += 1

        cache_key = build_cache_key(
            article
        )

        cached = cache.get(
            cache_key
        )

        # Cache remains usable even if Gemini circuit
        # breaker is active.
        if cached:
            if apply_cached_result(
                article,
                cached,
            ):
                cache_hits += 1
                continue

        # Avoid sending identical articles more than once
        # during this run.
        if cache_key in representatives:
            duplicates.setdefault(
                cache_key,
                [],
            ).append(
                article
            )

            same_run_duplicates += 1
            continue

        representatives[
            cache_key
        ] = article

        duplicates[
            cache_key
        ] = []

        pending_unique.append(
            article
        )

    print(
        "Articles:",
        len(articles),
    )

    print(
        "Need canonicalization:",
        need_count,
    )

    print(
        "Cache hits:",
        cache_hits,
    )

    print(
        "Same-run duplicates:",
        same_run_duplicates,
    )

    print(
        "Gemini needed:",
        len(pending_unique),
    )

    if need_count == 0:
        print(
            "No non-English articles found."
        )

        return articles

    # =====================================================
    # GEMINI
    # =====================================================

    gemini_successful = 0
    cache_changed = False

    for start in range(
        0,
        len(pending_unique),
        BATCH_SIZE,
    ):
        batch = pending_unique[
            start:
            start + BATCH_SIZE
        ]

        # Once quota/rate limit has opened the circuit,
        # don't even enter another Gemini request.
        if not GEMINI_AVAILABLE:
            remaining = (
                len(pending_unique)
                - start
            )

            print(
                "Skipping remaining "
                f"{remaining} uncached articles "
                "because Gemini is unavailable."
            )

            break

        (
            successful,
            changed,
        ) = process_batch(
            batch,
            cache,
        )

        gemini_successful += (
            successful
        )

        if changed:
            cache_changed = True

    # =====================================================
    # SAME-RUN DUPLICATES
    # =====================================================

    duplicate_successful = 0

    for (
        cache_key,
        representative,
    ) in representatives.items():

        for duplicate in duplicates.get(
            cache_key,
            [],
        ):
            if copy_canonicalization(
                representative,
                duplicate,
            ):
                duplicate_successful += 1

    # =====================================================
    # SAVE SUCCESSFUL RESULTS
    # =====================================================

    if cache_changed:
        save_cache(
            cache
        )

    # =====================================================
    # FINAL STATS
    # =====================================================

    successful = sum(
        1
        for article in articles
        if (
            needs_canonicalization(
                article
            )
            and article.get(
                "canonicalized",
                False,
            )
        )
    )

    failed = (
        need_count
        - successful
    )

    print(
        "Gemini canonicalized:",
        gemini_successful,
    )

    print(
        "Duplicate reuse:",
        duplicate_successful,
    )

    print(
        "Total canonicalized:",
        successful,
    )

    print(
        "Fallback to original:",
        failed,
    )

    if not GEMINI_AVAILABLE:
        print(
            "Gemini status: DISABLED "
            "FOR THIS PROCESS"
        )

    else:
        print(
            "Gemini status: AVAILABLE"
        )

    return articles