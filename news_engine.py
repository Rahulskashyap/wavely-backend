import json
from news_service_v3 import get_all_news


def load_preferences():
    with open("user_preferences.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_news_by_mode():

    prefs = load_preferences()

    mode = prefs["news_mode"]

    all_news = get_all_news()

    if mode == "India":

        selected_news = {
            "state": all_news["state"],
            "india": all_news["india"],
            "economy": all_news["economy"],
            "sports": all_news["sports"],
            "entertainment": all_news["entertainment"]
        }

    elif mode == "Global":

        selected_news = {
            "india": all_news["india"],
            "technology": all_news["technology"]
        }

    else:  # Hybrid

        selected_news = all_news

    return selected_news