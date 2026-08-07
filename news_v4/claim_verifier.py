from itertools import combinations

from .claim_extractor import extract_claims


# =========================================================
# BASIC OVERLAP
# =========================================================

def overlap(values_a, values_b):

    return set(values_a).intersection(
        set(values_b)
    )


# =========================================================
# ENTITY MATCHING
# =========================================================

def entity_overlap(
    entities_a,
    entities_b,
):
    """
    Compare normalized entity strings.

    Exact matches count immediately.

    Also allow containment for cases like:

    "johnson johnson"
    "johnson johnson company"
    """

    matches = set()

    for entity_a in entities_a:

        for entity_b in entities_b:

            if entity_a == entity_b:

                matches.add(entity_a)

                continue

            if (
                len(entity_a) >= 5
                and len(entity_b) >= 5
            ):

                if (
                    entity_a in entity_b
                    or entity_b in entity_a
                ):

                    matches.add(
                        min(
                            entity_a,
                            entity_b,
                            key=len,
                        )
                    )

    return matches


# =========================================================
# DIRECTION CONFLICT
# =========================================================

def find_direction_conflicts(
    directions_a,
    directions_b,
):

    conflicts = []

    shared_groups = (
        set(directions_a.keys())
        &
        set(directions_b.keys())
    )

    for group in shared_groups:

        value_a = directions_a[group]
        value_b = directions_b[group]

        if (
            value_a != value_b
            and value_a != "mixed"
            and value_b != "mixed"
        ):

            conflicts.append(
                {
                    "type": "direction",

                    "group": group,

                    "source_a":
                        value_a,

                    "source_b":
                        value_b,
                }
            )

    return conflicts


# =========================================================
# ADD AGREEMENT HELPER
# =========================================================

def add_agreement(
    result,
    agreement_type,
    values,
    weight,
):

    if not values:
        return

    result["agreements"].append(
        {
            "type": agreement_type,

            "values": sorted(values),

            "weight": weight,
        }
    )

    result["agreement_score"] += weight


# =========================================================
# COMPARE CLAIMS
# =========================================================

def compare_claims(
    claim_a,
    claim_b,
):

    result = {

        "source_a":
            claim_a.get(
                "source_name"
            ),

        "source_b":
            claim_b.get(
                "source_name"
            ),

        "agreements": [],

        "conflicts": [],

        "agreement_score": 0,

        "status": "insufficient",
    }


    # =====================================================
    # CONTRADICTIONS FIRST
    # =====================================================

    direction_conflicts = (
        find_direction_conflicts(

            claim_a.get(
                "directions",
                {},
            ),

            claim_b.get(
                "directions",
                {},
            ),
        )
    )

    result["conflicts"].extend(
        direction_conflicts
    )


    # =====================================================
    # ENTITIES
    # =====================================================

    shared_entities = entity_overlap(

        claim_a.get(
            "entities",
            [],
        ),

        claim_b.get(
            "entities",
            [],
        ),
    )

    add_agreement(
        result,
        "entities",
        shared_entities,
        2,
    )


    # =====================================================
    # MONEY
    # =====================================================

    shared_money = overlap(

        claim_a.get(
            "money",
            [],
        ),

        claim_b.get(
            "money",
            [],
        ),
    )

    add_agreement(
        result,
        "money",
        shared_money,
        3,
    )


    # =====================================================
    # PERCENTAGES
    # =====================================================

    shared_percentages = overlap(

        claim_a.get(
            "percentages",
            [],
        ),

        claim_b.get(
            "percentages",
            [],
        ),
    )

    add_agreement(
        result,
        "percentage",
        shared_percentages,
        2,
    )


    # =====================================================
    # ACTION / EVENT CONCEPTS
    # =====================================================

    shared_actions = overlap(

        claim_a.get(
            "actions",
            [],
        ),

        claim_b.get(
            "actions",
            [],
        ),
    )

    add_agreement(
        result,
        "actions",
        shared_actions,
        2,
    )


    # =====================================================
    # NUMBERS
    #
    # Numbers are intentionally weaker.
    #
    # Two unrelated articles can both contain "5".
    # =====================================================

    shared_numbers = overlap(

        claim_a.get(
            "numbers",
            [],
        ),

        claim_b.get(
            "numbers",
            [],
        ),
    )

    add_agreement(
        result,
        "numbers",
        shared_numbers,
        1,
    )


    # =====================================================
    # TIME
    # =====================================================

    shared_time = overlap(

        claim_a.get(
            "time_expressions",
            [],
        ),

        claim_b.get(
            "time_expressions",
            [],
        ),
    )

    add_agreement(
        result,
        "time",
        shared_time,
        1,
    )


    # =====================================================
    # FINAL STATUS
    # =====================================================

    if result["conflicts"]:

        result["status"] = "conflict"

    elif result["agreement_score"] >= 4:

        result["status"] = "agreement"

    elif result["agreement_score"] >= 2:

        result["status"] = "partial"

    else:

        result["status"] = "insufficient"

    return result


# =========================================================
# ARTICLE COMPARISON
# =========================================================

def compare_articles(
    article_a,
    article_b,
):

    claim_a = extract_claims(
        article_a
    )

    claim_b = extract_claims(
        article_b
    )

    return compare_claims(
        claim_a,
        claim_b,
    )


# =========================================================
# VERIFY CLUSTER
# =========================================================

def verify_cluster_claims(cluster):

    articles = cluster.get(
        "articles",
        []
    )

    comparisons = []

    for (
        article_a,
        article_b,
    ) in combinations(
        articles,
        2,
    ):

        publisher_a = (
            article_a.get(
                "publisher_id"
            )
        )

        publisher_b = (
            article_b.get(
                "publisher_id"
            )
        )

        # Same publisher cannot independently
        # corroborate itself.
        if (
            publisher_a
            and publisher_b
            and publisher_a == publisher_b
        ):
            continue

        comparison = (
            compare_articles(
                article_a,
                article_b,
            )
        )

        comparisons.append(
            comparison
        )


    agreement_count = sum(
        comparison["status"]
        == "agreement"
        for comparison
        in comparisons
    )

    partial_count = sum(
        comparison["status"]
        == "partial"
        for comparison
        in comparisons
    )

    conflict_count = sum(
        comparison["status"]
        == "conflict"
        for comparison
        in comparisons
    )

    insufficient_count = sum(
        comparison["status"]
        == "insufficient"
        for comparison
        in comparisons
    )

    # =====================================================
    # CLUSTER STATUS
    # =====================================================

    total_comparisons = len(comparisons)

    if total_comparisons == 0:

        status = "insufficient"

    else:

        agreement_ratio = (
            agreement_count / total_comparisons
        )

        conflict_ratio = (
            conflict_count / total_comparisons
        )

        partial_ratio = (
            partial_count / total_comparisons
        )

        if conflict_ratio >= 0.50:

            status = "conflict"

        elif agreement_ratio >= 0.50:

            status = "agreement"

        elif (
            partial_ratio > 0
            or agreement_count > 0
        ):

            status = "partial"

        else:

            status = "insufficient"

    return {

        "status": status,

        "agreement_count":
            agreement_count,

        "partial_count":
            partial_count,

        "conflict_count":
            conflict_count,

        "insufficient_count":
            insufficient_count,

        "comparisons":
            comparisons,
    }