
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(query):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()


def format_articles(news_data):

    articles = news_data.get("articles", [])

    formatted_text = ""

    for article in articles[:15]:

        title = article.get("title", "")
        description = article.get("description", "")

        formatted_text += f"""
Title: {title}

Description: {description}

"""

    return formatted_text


def format_state_articles(news_data):

    articles = news_data.get("articles", [])

    formatted_text = ""

    for article in articles[:15]:

        title = article.get("title", "")
        description = article.get("description", "")

        combined = (title + " " + description).lower()

        if (
            "karnataka" not in combined
            and "bengaluru" not in combined
            and "mysuru" not in combined
            and "mangaluru" not in combined
            and "hubballi" not in combined
            and "belagavi" not in combined
        ):
            continue

        formatted_text += f"""
Title: {title}

Description: {description}

"""

    return formatted_text


def get_all_news(country, state):

    return {

        "state": format_state_articles(
            fetch_news(state)
        ),

        "india": format_articles(
            fetch_news(country)
        ),

        "world": format_articles(
            fetch_news("World News")
        ),

        "economy": format_articles(
            fetch_news("Indian economy")
        ),

        "technology": format_articles(
            fetch_news("Artificial Intelligence India")
        ),

        "sports": format_articles(
            fetch_news("Cricket India")
        ),

        "entertainment": format_articles(
            fetch_news("Bollywood")
        )
    }
