from news_v4.clusterer import (
    calculate_semantic_similarity,
    same_event,
)


# =========================================================
# SAME EVENT — ORIGINAL KANNADA
# =========================================================

kannada = {
    "title": (
        "ತಮಿಳುನಾಡಿಗೆ ಕಾವೇರಿ ನೀರು ಬಿಡಲು "
        "CWRC ಆದೇಶ"
    ),
    "summary": "",
    "published_at": None,
    "categories": ["state"],
}


# =========================================================
# SAME EVENT — ENGLISH PUBLISHER
# =========================================================

english = {
    "title": (
        "CWRC directs Karnataka to release "
        "Cauvery water to Tamil Nadu"
    ),
    "summary": "",
    "published_at": None,
    "categories": ["state"],
}


# =========================================================
# SAME KANNADA STORY — CANONICAL ENGLISH VERSION
# =========================================================

kannada_canonical = {
    "title": (
        "CWRC orders Karnataka to release "
        "Cauvery water to Tamil Nadu"
    ),
    "summary": "",
    "published_at": None,
    "categories": ["state"],
}


# =========================================================
# UNRELATED STORY
# =========================================================

unrelated = {
    "title": (
        "India announces new technology policy"
    ),
    "summary": "",
    "published_at": None,
    "categories": ["national"],
}


# =========================================================
# TEST 1 — RAW KANNADA VS ENGLISH
# =========================================================

print("\n==============================")
print("KANNADA VS ENGLISH")
print("==============================")

print(
    "SEMANTIC:",
    calculate_semantic_similarity(
        kannada,
        english,
    ),
)

print(
    "SAME EVENT:",
    same_event(
        kannada,
        english,
    ),
)


# =========================================================
# TEST 2 — CANONICAL ENGLISH VS ENGLISH
# =========================================================

print("\n==============================")
print("CANONICAL VS ENGLISH")
print("==============================")

print(
    "SEMANTIC:",
    calculate_semantic_similarity(
        kannada_canonical,
        english,
    ),
)

print(
    "SAME EVENT:",
    same_event(
        kannada_canonical,
        english,
    ),
)


# =========================================================
# TEST 3 — KANNADA VS UNRELATED
# =========================================================

print("\n==============================")
print("KANNADA VS UNRELATED")
print("==============================")

print(
    "SEMANTIC:",
    calculate_semantic_similarity(
        kannada,
        unrelated,
    ),
)

print(
    "SAME EVENT:",
    same_event(
        kannada,
        unrelated,
    ),
)


# =========================================================
# TEST 4 — CANONICAL VS UNRELATED
# =========================================================

print("\n==============================")
print("CANONICAL VS UNRELATED")
print("==============================")

print(
    "SEMANTIC:",
    calculate_semantic_similarity(
        kannada_canonical,
        unrelated,
    ),
)

print(
    "SAME EVENT:",
    same_event(
        kannada_canonical,
        unrelated,
    ),
)