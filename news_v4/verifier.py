# news_v4/verifier.py

from .claim_verifier import verify_cluster_claims


def verify_cluster(cluster):
    articles = cluster["articles"]

    # ---------------------------------------------------------
    # INDEPENDENT PUBLISHERS
    # ---------------------------------------------------------

    publisher_ids = {
        article["publisher_id"]
        for article in articles
        if article["source_type"] == "publisher"
    }

    # ---------------------------------------------------------
    # PRIMARY / OFFICIAL SOURCES
    # ---------------------------------------------------------

    primary_sources = {
        article["publisher_id"]
        for article in articles
        if article["source_type"] == "primary"
    }

    independent_count = len(publisher_ids)
    has_primary_source = len(primary_sources) > 0

    # ---------------------------------------------------------
    # CLAIM VERIFICATION
    # ---------------------------------------------------------

    claim_verification = verify_cluster_claims(cluster)

    claim_status = claim_verification["status"]

    # ---------------------------------------------------------
    # EXISTING CONFIDENCE SYSTEM
    #
    # Keep this unchanged for now.
    # After testing real articles, claim agreement/conflict
    # will become part of the final confidence calculation.
    # ---------------------------------------------------------

        # ---------------------------------------------------------
    # CONFIDENCE CALCULATION
    # ---------------------------------------------------------

    if claim_status == "conflict":

        confidence = "low"

    elif (
        claim_status == "agreement"
        and (
            has_primary_source
            or independent_count >= 3
        )
    ):

        confidence = "high"

    elif (
        claim_status in {
            "agreement",
            "partial",
        }
        and independent_count >= 2
    ):

        confidence = "medium"

    elif has_primary_source:

        confidence = "medium"

    else:

        confidence = "low"

    # ---------------------------------------------------------
    # CONFIRMED SOURCE NAMES
    # ---------------------------------------------------------

    confirmed_by = sorted(
        {
            article["source_name"]
            for article in articles
        }
    )

    # ---------------------------------------------------------
    # SOURCE DETAILS
    # ---------------------------------------------------------

    sources = [
        {
            "name": article["source_name"],
            "type": article["source_type"],
            "url": article["url"],
            "published_at": (
                article["published_at"].isoformat()
                if article["published_at"]
                else None
            ),
        }
        for article in articles
    ]

    # ---------------------------------------------------------
    # RESULT
    # ---------------------------------------------------------

    return {
        "title": articles[0]["title"],

        # Existing verification fields
        "confidence": confidence,

        "independent_source_count":
            independent_count,

        "has_primary_source":
            has_primary_source,

        "confirmed_by":
            confirmed_by,

        "sources":
            sources,

        # NEW: Claim verification
        "claim_status":
            claim_status,

        "claim_verification":
            claim_verification,

        # Keep original articles for later stages
        "articles":
            articles,
    }


def verify_clusters(clusters):
    return [
        verify_cluster(cluster)
        for cluster in clusters
    ]