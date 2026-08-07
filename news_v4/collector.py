# news_v4/collector.py

import json
import random
import re
import time

from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin, urlsplit, urlunsplit

import feedparser
import requests
from bs4 import BeautifulSoup

from .news_sources import get_sources
from .normalizer import normalize_article


# =========================================================
# NETWORK CONFIG
# =========================================================

REQUEST_TIMEOUT = 20
MAX_REQUEST_ATTEMPTS = 3

RETRYABLE_STATUS_CODES = {
    408,
    425,
    429,
    500,
    502,
    503,
    504,
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,"
        "application/rss+xml;q=0.9,"
        "application/atom+xml;q=0.9,"
        "*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


# =========================================================
# NETWORK FETCHING
# =========================================================

def fetch_url(
    url,
    source_name="source",
    timeout=REQUEST_TIMEOUT,
):
    """
    Fetch a URL with retry + exponential backoff.

    Retries:
        - timeout
        - connection errors
        - HTTP 408 / 425 / 429
        - HTTP 5xx

    Permanent HTTP errors such as 401, 403 and 404
    are not repeatedly retried.
    """

    last_error = None

    for attempt in range(
        1,
        MAX_REQUEST_ATTEMPTS + 1,
    ):
        try:
            response = SESSION.get(
                url,
                timeout=timeout,
            )

            if (
                response.status_code
                in RETRYABLE_STATUS_CODES
            ):
                raise requests.HTTPError(
                    (
                        f"Retryable HTTP "
                        f"{response.status_code}"
                    ),
                    response=response,
                )

            response.raise_for_status()

            return response

        except (
            requests.Timeout,
            requests.ConnectionError,
        ) as error:
            last_error = error

        except requests.HTTPError as error:
            last_error = error

            status = None

            if error.response is not None:
                status = (
                    error.response.status_code
                )

            if (
                status is not None
                and 400 <= status < 500
                and status
                not in RETRYABLE_STATUS_CODES
            ):
                break

        except requests.RequestException as error:
            last_error = error

        if attempt < MAX_REQUEST_ATTEMPTS:
            delay = (
                2 ** attempt
                + random.uniform(0, 0.5)
            )

            print(
                f"{source_name}: request failed "
                f"(attempt {attempt}/"
                f"{MAX_REQUEST_ATTEMPTS}). "
                f"Retrying in {delay:.1f}s..."
            )

            time.sleep(delay)

    raise requests.RequestException(
        (
            f"{source_name} unavailable after "
            f"{MAX_REQUEST_ATTEMPTS} attempts: "
            f"{last_error}"
        )
    )


# =========================================================
# URL NORMALIZATION
# =========================================================

def canonicalize_url(url):
    """
    Remove query parameters/fragments and normalize URLs.

    Example:
        https://example.com/news?a=1#section
            ->
        https://example.com/news
    """

    if not url:
        return ""

    try:
        parts = urlsplit(url)

        clean_url = urlunsplit(
            (
                parts.scheme.lower(),
                parts.netloc.lower(),
                parts.path.rstrip("/"),
                "",
                "",
            )
        )

        return clean_url

    except Exception:
        return url


# =========================================================
# FRESHNESS
# =========================================================

def is_recent(article, hours=30):
    """
    Check whether an article was published within
    the requested freshness window.
    """

    published_at = article.get(
        "published_at"
    )

    if published_at is None:
        return False

    if published_at.tzinfo is None:
        published_at = (
            published_at.replace(
                tzinfo=timezone.utc
            )
        )

    cutoff = (
        datetime.now(timezone.utc)
        - timedelta(hours=hours)
    )

    return published_at >= cutoff


# =========================================================
# DATE PARSING
# =========================================================

def parse_iso_datetime(value):
    """
    Parse ISO date/time into timezone-aware UTC datetime.
    """

    if not value:
        return None

    try:
        value = value.strip()

        if value.endswith("Z"):
            value = (
                value[:-1]
                + "+00:00"
            )

        parsed = datetime.fromisoformat(
            value
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(
                tzinfo=timezone.utc
            )

        return parsed.astimezone(
            timezone.utc
        )

    except (
        ValueError,
        TypeError,
    ):
        return None


def extract_published_at(container):
    """
    Extract publication time from an HTML container.
    """

    time_tag = container.find(
        "time"
    )

    if time_tag:
        value = (
            time_tag.get("datetime")
            or time_tag.get("content")
        )

        parsed = parse_iso_datetime(
            value
        )

        if parsed:
            return parsed

    return None


# =========================================================
# RSS COLLECTION
# =========================================================

def collect_from_rss(source):
    """
    Collect recent articles from an RSS feed.

    The RSS document is downloaded using fetch_url()
    so RSS sources get controlled timeout/retry behavior.
    """

    print(
        f"Collecting: {source['name']}"
    )

    try:
        response = fetch_url(
            source["url"],
            source_name=source["name"],
        )

        feed = feedparser.parse(
            response.content
        )

        if feed.bozo:
            print(
                f"Feed parse warning for "
                f"{source['name']}:",
                feed.bozo_exception,
            )

        articles = []

        for entry in feed.entries[:50]:
            article = normalize_article(
                entry,
                source,
            )

            if not article.get("title"):
                continue

            if not article.get("url"):
                continue

            if is_recent(article):
                articles.append(
                    article
                )

        print(
            f"{source['name']}: "
            f"{len(articles)} articles"
        )

        return articles

    except requests.RequestException as error:
        print(
            f"Failed collecting "
            f"{source['name']}:",
            error,
        )

        return []

    except Exception as error:
        print(
            f"Failed parsing "
            f"{source['name']}:",
            error,
        )

        return []


# =========================================================
# GENERIC WEBSITE COLLECTION
# =========================================================

def collect_from_website(source):
    """
    Generic CSS-selector based website collector.
    """

    print(
        f"Collecting: {source['name']}"
    )

    selectors = source.get(
        "selectors",
        {},
    )

    article_selector = selectors.get(
        "article"
    )

    title_selector = selectors.get(
        "title"
    )

    link_selector = selectors.get(
        "link",
        "a",
    )

    summary_selector = selectors.get(
        "summary"
    )

    if not article_selector:
        print(
            f"Website config missing article "
            f"selector for {source['name']}"
        )

        return []

    if not title_selector:
        print(
            f"Website config missing title "
            f"selector for {source['name']}"
        )

        return []

    try:
        response = fetch_url(
            source["url"],
            source_name=source["name"],
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        containers = soup.select(
            article_selector
        )

        articles = []

        for container in containers[:100]:
            title_element = (
                container.select_one(
                    title_selector
                )
            )

            if not title_element:
                continue

            title = (
                title_element.get_text(
                    " ",
                    strip=True,
                )
            )

            if not title:
                continue

            if title_element.name == "a":
                link_element = (
                    title_element
                )
            else:
                link_element = (
                    container.select_one(
                        link_selector
                    )
                )

            if not link_element:
                continue

            href = link_element.get(
                "href"
            )

            if not href:
                continue

            article_url = urljoin(
                source["url"],
                href,
            )

            summary = ""

            if summary_selector:
                summary_element = (
                    container.select_one(
                        summary_selector
                    )
                )

                if summary_element:
                    summary = (
                        summary_element.get_text(
                            " ",
                            strip=True,
                        )
                    )

            published_at = (
                extract_published_at(
                    container
                )
            )

            article = {
                "title": title,
                "summary": summary,

                "url": canonicalize_url(
                    article_url
                ),

                "published_at":
                    published_at,

                "publisher_id":
                    source.get(
                        "publisher_id"
                    ),

                "source_name":
                    source.get(
                        "name"
                    ),

                "source_type":
                    source.get(
                        "type",
                        "publisher",
                    ),

                "language":
                    source.get(
                        "language"
                    ),

                "feed_region":
                    source.get(
                        "region"
                    ),

                # Actual story geography is
                # determined later.
                "region": None,

                "categories":
                    source.get(
                        "categories",
                        [],
                    ),
            }

            articles.append(
                article
            )

        print(
            f"{source['name']}: "
            f"{len(articles)} website articles"
        )

        return articles

    except requests.RequestException as error:
        print(
            f"Failed collecting "
            f"{source['name']}:",
            error,
        )

        return []

    except Exception as error:
        print(
            f"Failed parsing "
            f"{source['name']}:",
            error,
        )

        return []


# =========================================================
# TV9 KANNADA ARTICLE METADATA
# =========================================================

def extract_tv9_article_metadata(url):
    """
    Fetch a TV9 Kannada article and extract NewsArticle
    JSON-LD metadata.

    Meta tags are used as fallbacks when JSON-LD does
    not provide the required fields.
    """

    result = {
        "published_at": None,
        "modified_at": None,
        "summary": "",
        "article_body": "",
        "headline": "",
        "language": None,
        "article_section": None,
    }

    try:
        response = fetch_url(
            url,
            source_name=(
                "TV9 Kannada article"
            ),
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # =================================================
        # JSON-LD
        # =================================================

        scripts = soup.find_all(
            "script",
            attrs={
                "type":
                    "application/ld+json"
            },
        )

        for script in scripts:
            raw = (
                script.string
                or script.get_text()
            )

            if not raw:
                continue

            raw = raw.strip()

            if not raw:
                continue

            try:
                data = json.loads(
                    raw
                )

            except (
                json.JSONDecodeError,
                TypeError,
            ):
                continue

            objects = []

            if isinstance(
                data,
                list,
            ):
                objects.extend(
                    data
                )

            elif isinstance(
                data,
                dict,
            ):
                objects.append(
                    data
                )

                graph = data.get(
                    "@graph"
                )

                if isinstance(
                    graph,
                    list,
                ):
                    objects.extend(
                        graph
                    )

            for item in objects:
                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                article_type = (
                    item.get("@type")
                )

                if isinstance(
                    article_type,
                    list,
                ):
                    is_news_article = (
                        "NewsArticle"
                        in article_type
                    )

                else:
                    is_news_article = (
                        article_type
                        == "NewsArticle"
                    )

                if not is_news_article:
                    continue

                result["headline"] = (
                    item.get(
                        "headline"
                    )
                    or ""
                ).strip()

                result["summary"] = (
                    item.get(
                        "description"
                    )
                    or ""
                ).strip()

                result["article_body"] = (
                    item.get(
                        "articleBody"
                    )
                    or ""
                ).strip()

                result["published_at"] = (
                    parse_iso_datetime(
                        item.get(
                            "datePublished"
                        )
                    )
                )

                result["modified_at"] = (
                    parse_iso_datetime(
                        item.get(
                            "dateModified"
                        )
                    )
                )

                result["language"] = (
                    item.get(
                        "inLanguage"
                    )
                )

                result[
                    "article_section"
                ] = item.get(
                    "articleSection"
                )

                return result

        # =================================================
        # FALLBACK META TAGS
        # =================================================

        published_tag = soup.find(
            "meta",
            attrs={
                "property":
                    "article:published_time"
            },
        )

        if published_tag:
            result["published_at"] = (
                parse_iso_datetime(
                    published_tag.get(
                        "content"
                    )
                )
            )

        title_tag = soup.find(
            "meta",
            attrs={
                "property": "og:title"
            },
        )

        if title_tag:
            result["headline"] = (
                title_tag.get(
                    "content",
                    "",
                )
            ).strip()

        description_tag = soup.find(
            "meta",
            attrs={
                "property":
                    "og:description"
            },
        )

        if not description_tag:
            description_tag = soup.find(
                "meta",
                attrs={
                    "name":
                        "description"
                },
            )

        if description_tag:
            result["summary"] = (
                description_tag.get(
                    "content",
                    "",
                )
            ).strip()

        return result

    except requests.RequestException as error:
        print(
            "Failed fetching TV9 article "
            f"{url}: {error}"
        )

        return result

    except Exception as error:
        print(
            "Failed parsing TV9 article "
            f"{url}: {error}"
        )

        return result


# =========================================================
# LINK-BASED WEBSITE COLLECTION
# =========================================================

def collect_from_website_links(source):
    """
    Collect article links from a listing page.

    For TV9 Kannada:
        1. Read the Karnataka listing page.
        2. Find valid article URLs.
        3. Fetch article metadata.
        4. Keep fresh articles.
    """

    print(
        f"Collecting: {source['name']}"
    )

    try:
        # IMPORTANT:
        # Use retry-enabled network fetch here too.
        response = fetch_url(
            source["url"],
            source_name=source["name"],
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        allowed_prefixes = source.get(
            "allowed_path_prefixes",
            [],
        )

        excluded_prefixes = source.get(
            "excluded_path_prefixes",
            [],
        )

        source_parts = urlsplit(
            source["url"]
        )

        source_domain = (
            source_parts.netloc
            .lower()
            .removeprefix("www.")
        )

        articles = []
        seen_urls = set()

        for link in soup.find_all("a"):
            href = link.get(
                "href"
            )

            title = link.get_text(
                " ",
                strip=True,
            )

            if not href:
                continue

            if not title:
                continue

            if len(title) < 20:
                continue

            full_url = urljoin(
                source["url"],
                href,
            )

            parsed = urlsplit(
                full_url
            )

            article_domain = (
                parsed.netloc
                .lower()
                .removeprefix("www.")
            )

            path = parsed.path

            # ---------------------------------------------
            # DOMAIN CHECK
            # ---------------------------------------------

            if (
                article_domain
                != source_domain
            ):
                continue

            # ---------------------------------------------
            # ALLOWED PATH CHECK
            # ---------------------------------------------

            if allowed_prefixes:
                allowed = any(
                    path.startswith(
                        prefix
                    )
                    for prefix
                    in allowed_prefixes
                )

                if not allowed:
                    continue

            # ---------------------------------------------
            # EXCLUDED PATH CHECK
            # ---------------------------------------------

            excluded = any(
                path.startswith(
                    prefix
                )
                for prefix
                in excluded_prefixes
            )

            if excluded:
                continue

            # ---------------------------------------------
            # ARTICLE URL PATTERN
            # ---------------------------------------------

            article_url_pattern = (
                source.get(
                    "article_url_pattern"
                )
            )

            if article_url_pattern:
                if not re.search(
                    article_url_pattern,
                    path,
                    flags=re.IGNORECASE,
                ):
                    continue

            # ---------------------------------------------
            # NORMALIZE URL
            # ---------------------------------------------

            clean_url = (
                canonicalize_url(
                    full_url
                )
            )

            if not clean_url:
                continue

            if clean_url in seen_urls:
                continue

            seen_urls.add(
                clean_url
            )

            # =================================================
            # ARTICLE METADATA
            # =================================================

            metadata = {
                "published_at": None,
                "modified_at": None,
                "summary": "",
                "article_body": "",
                "headline": "",
                "language": None,
                "article_section": None,
            }

            # =================================================
            # TV9 KANNADA
            # =================================================

            if (
                source.get(
                    "publisher_id"
                )
                == "tv9_kannada"
            ):
                metadata = (
                    extract_tv9_article_metadata(
                        clean_url
                    )
                )

                # Require a real timestamp so the
                # freshness rule remains reliable.
                if (
                    metadata.get(
                        "published_at"
                    )
                    is None
                ):
                    continue

            # =================================================
            # BUILD ARTICLE
            # =================================================

            article = {
                "title": (
                    metadata.get(
                        "headline"
                    )
                    or title
                ),

                "summary": (
                    metadata.get(
                        "summary",
                        "",
                    )
                ),

                "article_body": (
                    metadata.get(
                        "article_body",
                        "",
                    )
                ),

                "url": clean_url,

                "published_at":
                    metadata.get(
                        "published_at"
                    ),

                "modified_at":
                    metadata.get(
                        "modified_at"
                    ),

                "language":
                    metadata.get(
                        "language"
                    ),

                "article_section":
                    metadata.get(
                        "article_section"
                    ),

                "publisher_id":
                    source.get(
                        "publisher_id"
                    ),

                "source_name":
                    source.get(
                        "name"
                    ),

                "source_type":
                    source.get(
                        "type",
                        "publisher",
                    ),

                "feed_region":
                    source.get(
                        "region"
                    ),

                # Do not assume every article
                # from a regional feed is local.
                "region": None,

                "categories":
                    source.get(
                        "categories",
                        [],
                    ),
            }

            if not is_recent(
                article
            ):
                continue

            articles.append(
                article
            )

        print(
            f"{source['name']}: "
            f"{len(articles)} website articles"
        )

        return articles

    except requests.RequestException as error:
        print(
            f"Failed collecting "
            f"{source['name']}:",
            error,
        )

        return []

    except Exception as error:
        print(
            f"Failed parsing "
            f"{source['name']}:",
            error,
        )

        return []


# =========================================================
# SOURCE ROUTER
# =========================================================

def collect_source(source):
    """
    Route each configured source to its collector.
    """

    method = source.get(
        "method",
        "rss",
    ).lower()

    if method == "rss":
        return collect_from_rss(
            source
        )

    if method == "website":
        return collect_from_website(
            source
        )

    if method == "website_links":
        return (
            collect_from_website_links(
                source
            )
        )

    print(
        f"Unknown collection method "
        f"'{method}' for {source['name']}"
    )

    return []


# =========================================================
# COLLECT EVERYTHING
# =========================================================

def collect_all_news():
    """
    Collect news from every configured source and perform
    exact URL deduplication.
    """

    all_articles = []

    for source in get_sources():
        articles = collect_source(
            source
        )

        all_articles.extend(
            articles
        )

    print(
        "\nTotal collected before "
        f"deduplication: {len(all_articles)}"
    )

    # =====================================================
    # EXACT URL DEDUPLICATION
    # =====================================================

    unique_articles = []
    seen_urls = set()

    for article in all_articles:
        url = article.get(
            "url"
        )

        if not url:
            continue

        clean_url = canonicalize_url(
            url
        )

        if not clean_url:
            continue

        if clean_url in seen_urls:
            continue

        seen_urls.add(
            clean_url
        )

        article["url"] = (
            clean_url
        )

        unique_articles.append(
            article
        )

    print(
        "Total after exact "
        f"deduplication: "
        f"{len(unique_articles)}"
    )

    return unique_articles