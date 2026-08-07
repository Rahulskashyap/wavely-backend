from generate_daily_podcast import generate_podcast_for_user


# Replace this with the UID of the Firebase user
# you normally use for testing.
TEST_UID = "R2V7CIxEKNVq3TSb94xgNvw91K32"


if __name__ == "__main__":
    print("=" * 60)
    print("WAVELY V4 PRODUCTION INTEGRATION TEST")
    print("=" * 60)

    result = generate_podcast_for_user(
        TEST_UID
    )

    print("\nTEST COMPLETED")

    if result:
        print("STATUS:", result.get("status"))
        print("STATE:", result.get("state"))
        print("LANGUAGE:", result.get("language"))
        print("DURATION:", result.get("duration"))
        print("AUDIO URL:", result.get("audio_url"))
        print(
            "NEWS ENGINE:",
            result.get("news_engine"),
        )