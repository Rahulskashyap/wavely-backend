from firebase_service import db
from google.cloud.firestore_v1 import Query


def get_podcast_history(uid):

    podcast_ref = (
        db.collection("users")
        .document(uid)
        .collection("podcasts")
    )

    docs = (
        podcast_ref
        .order_by(
    "date",
    direction=Query.DESCENDING,
)
        .stream()
    )

    podcasts = []

    for doc in docs:

        data = doc.to_dict()

        # Only show successfully generated podcasts
        if data.get("status") != "completed":
            continue

        podcasts.append({
            "podcast_id": data.get(
                "podcast_id",
                doc.id,
            ),
            "title": data.get(
                "title",
                "Morning Brief",
            ),
            "date": data.get(
                "date",
                "",
            ),
            "duration": data.get(
                "duration",
                20,
            ),
            "audio_url": data.get(
                "audio_url",
                "",
            ),
            "categories": data.get(
                "categories",
                [],
            ),
            "language": data.get(
                "language",
                "English",
            ),
            "voice": data.get(
                "voice",
                "Male",
            ),
        })

    return podcasts


def get_latest_podcast(uid):

    podcasts = get_podcast_history(uid)

    if not podcasts:
        return None

    return podcasts[0]


def get_podcast_details(uid, date):

    doc = (
        db.collection("users")
        .document(uid)
        .collection("podcasts")
        .document(date)
        .get()
    )

    if not doc.exists:
        return None

    return doc.to_dict()