import json
from datetime import datetime, timezone

from firebase_service import db


DEFAULT_PREFERENCES = {
    "country": "India",
    "state": "Karnataka",
    "language": "English",
    "voice": "Male",
    "categories": ["Technology"],
    "duration": 20,
}


def ensure_user_document(uid):

    user_ref = (
        db.collection("users")
        .document(uid)
    )

    user_ref.set(
        {
            "uid": uid,
            "updated_at": datetime.now(timezone.utc),
        },
        merge=True,
    )


def get_user_preferences(uid):

    # Ensure scheduler can discover this user
    ensure_user_document(uid)

    doc_ref = (
        db.collection("users")
        .document(uid)
        .collection("settings")
        .document("preferences")
    )

    doc = doc_ref.get()

    if not doc.exists:

        print(
            f"No preferences found for {uid}. "
            "Creating defaults."
        )

        doc_ref.set(
            DEFAULT_PREFERENCES.copy()
        )

        return DEFAULT_PREFERENCES.copy()

    preferences = doc.to_dict()

    print(
        "Firestore Preferences:",
        preferences,
    )

    return preferences


def update_user_preferences(
    uid,
    country,
    state,
    language,
    voice,
    categories,
    duration,
):

    # Ensure scheduler can discover this user
    ensure_user_document(uid)

    doc_ref = (
        db.collection("users")
        .document(uid)
        .collection("settings")
        .document("preferences")
    )

    if isinstance(categories, str):

        try:
            categories = json.loads(categories)

        except Exception:
            categories = []

    data = {
        "country": country,
        "state": state,
        "language": language,
        "voice": voice,
        "categories": categories,
        "duration": duration,
        "updated_at": datetime.now(timezone.utc),
    }

    doc_ref.set(
        data,
        merge=True,
    )

    print(
        f"Preferences updated for user: {uid}"
    )

    return data