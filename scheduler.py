import schedule
import time
from datetime import datetime

from firebase_service import db
from generate_daily_podcast import generate_podcast_for_user


def generate_for_all_users():

    print()
    print("=" * 60)
    print("STARTING AUTOMATIC DAILY GENERATION")
    print("=" * 60)

    users = db.collection("users").stream()

    user_count = 0
    success_count = 0
    failed_count = 0

    for user in users:

        uid = user.id
        user_count += 1

        print()
        print("Generating podcast for user:", uid)

        try:

            generate_podcast_for_user(uid)

            success_count += 1

        except Exception as e:

            failed_count += 1

            print(
                "Generation failed for user:",
                uid,
                "Error:",
                e,
            )

    print()
    print("=" * 60)
    print("DAILY GENERATION FINISHED")
    print("Users:", user_count)
    print("Successful:", success_count)
    print("Failed:", failed_count)
    print("=" * 60)


# Generate every day at 5:30 AM
schedule.every().day.at("05:30").do(
    generate_for_all_users
)


print("Wavely Scheduler Started")
print("Waiting for automatic generation...")


while True:

    schedule.run_pending()

    time.sleep(30)