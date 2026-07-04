import json


def load_preferences():

    with open("user_preferences.json", "r", encoding="utf-8") as file:
        return json.load(file)


def display_preferences():

    prefs = load_preferences()

    print("\n==============================")
    print("USER PREFERENCES")
    print("==============================")

    print("Name:", prefs["name"])
    print("State:", prefs["state"])
    print("Language:", prefs["language"])
    print("News Mode:", prefs["news_mode"])
    print("Voice:", prefs["voice"])
    print("Podcast Length:", prefs["podcast_length"], "minutes")

    print("\nSupported Languages:")

    for language in prefs["supported_languages"]:
        print("-", language)

    print("\nSupported News Modes:")

    for mode in prefs["supported_modes"]:
        print("-", mode)

    print("\nSupported Voices:")

    for voice in prefs["supported_voices"]:
        print("-", voice)


if __name__ == "__main__":
    display_preferences()