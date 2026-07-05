import sys
from datetime import datetime, timezone

from firebase_service import db
from generate_daily_podcast import generate_podcast_for_user


def generate_for_all_users():

    print()
    print("=" * 60)
    print("WAVELY AUTOMATIC DAILY GENERATION")
    print("Started at:", datetime.now(timezone.utc))
    print("=" * 60)

    users = db.collection("users").stream()

    user_count = 0
    success_count = 0
    failed_count = 0
    skipped_count = 0

    for user in users:

        uid = user.id
        user_count += 1

        print()
        print("-" * 60)
        print("CHECKING USER")
        print("USER:", uid)
        print("-" * 60)

        today = datetime.now(
            timezone.utc
        ).strftime("%Y-%m-%d")

        episode_ref = (
            db.collection("users")
            .document(uid)
            .collection("podcasts")
            .document(today)
        )

        existing_episode = episode_ref.get()

        if existing_episode.exists:

            episode_data = existing_episode.to_dict()

            if episode_data.get("status") == "completed":

                skipped_count += 1

                print(
                    "SKIPPING USER:",
                    uid,
                    "- today's podcast already exists.",
                )

                continue

        print()
        print("GENERATING PODCAST")
        print("USER:", uid)

        try:

            generate_podcast_for_user(uid)

            success_count += 1

            print(
                "SUCCESS:",
                uid,
            )

        except Exception as e:

            failed_count += 1

            print(
                "FAILED:",
                uid,
            )

            print(
                "ERROR:",
                str(e),
            )

    print()
    print("=" * 60)
    print("DAILY GENERATION FINISHED")
    print("Total users:", user_count)
    print("Successful:", success_count)
    print("Skipped:", skipped_count)
    print("Failed:", failed_count)
    print("Finished at:", datetime.now(timezone.utc))
    print("=" * 60)

    return {
        "total_users": user_count,
        "successful": success_count,
        "skipped": skipped_count,
        "failed": failed_count,
    }

if __name__ == "__main__":

    try:

        result = generate_for_all_users()

        if result["failed"] == 0:
            sys.exit(0)

        sys.exit(1)

    except Exception as e:

        print()
        print("SCHEDULER CRASHED")
        print("ERROR:", str(e))

        sys.exit(1)