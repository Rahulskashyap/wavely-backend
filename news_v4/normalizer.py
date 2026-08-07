# news_v4/normalizer.py

from datetime import timezone
from dateutil import parser as date_parser


# =========================================================
# DATE PARSING
# =========================================================

def parse_date(value):
    """
    Parse an RSS publication date and return a
    timezone-aware UTC datetime.
    """

    if not value:
        return None

    try:
        dt = date_parser.parse(value)

        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=timezone.utc
            )

        return dt.astimezone(
            timezone.utc
        )

    except (
        ValueError,
        TypeError,
        OverflowError,
    ):
        return None


# =========================================================
# LANGUAGE
# =========================================================

def get_entry_language(entry, source):
    """
    Get language metadata without treating language
    as geographic information.

    Example:
        Kannada language != Karnataka story
    """

    language = (
        entry.get("language")
        or source.get("language")
    )

    if not language:
        return None

    return str(language).strip()


# =========================================================
# ARTICLE NORMALIZATION
# =========================================================

def normalize_article(entry, source):
    """
    Convert an RSS entry into Wavely's common
    article structure.

    IMPORTANT:

    feed_region:
        Geographic context of the feed from which
        the article was collected.

    region:
        Actual story geography.

        This is intentionally None here because the
        RSS feed alone cannot reliably determine the
        geographic scope of every individual story.

    Example:

        Kannada feed publishes:
        "US LNG tanker attacked in Egypt"

        feed_region = "karnataka"
        region = None
        language = "kn"

    The geography classifier will later determine
    whether the story is Karnataka, another state,
    India, or world.
    """

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    title = (
        entry.get("title")
        or ""
    ).strip()

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    summary = (
        entry.get("summary")
        or entry.get("description")
        or ""
    ).strip()

    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    url = (
        entry.get("link")
        or entry.get("url")
        or ""
    ).strip()

    # -----------------------------------------------------
    # PUBLICATION DATE
    # -----------------------------------------------------

    published_raw = (
        entry.get("published")
        or entry.get("updated")
    )

    published_at = parse_date(
        published_raw
    )

    # -----------------------------------------------------
    # SOURCE METADATA
    # -----------------------------------------------------

    source_id = source.get(
        "id"
    )

    publisher_id = source.get(
        "publisher_id"
    )

    source_name = source.get(
        "name"
    )

    source_type = source.get(
        "type",
        "publisher",
    )

    # -----------------------------------------------------
    # FEED METADATA
    # -----------------------------------------------------

    feed_region = source.get(
        "region"
    )

    categories = list(
        source.get(
            "categories",
            [],
        )
        or []
    )

    language = get_entry_language(
        entry,
        source,
    )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {
        "title": title,
        "summary": summary,

        "source_id": source_id,
        "publisher_id": publisher_id,
        "source_name": source_name,
        "source_type": source_type,

        "url": url,
        "published_at": published_at,

        # Language and geography are separate.
        "language": language,

        # Feed/source geographic context.
        "feed_region": feed_region,

        # Actual story geography is determined later.
        "region": None,

        "categories": categories,
    }