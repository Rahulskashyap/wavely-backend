import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def fetch_category(category):

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "country": "in",
        "category": category,
        "pageSize": 50,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    print("\n--------------------")
    print("Category:", category)
    print("Status Code:", response.status_code)
    print("URL:", response.url)
    print("Response:", response.text[:500])

    return response.json()


def get_all_india_news():

    return {
        "general": fetch_category("general"),
        "business": fetch_category("business"),
        "technology": fetch_category("technology"),
        "sports": fetch_category("sports"),
        "entertainment": fetch_category("entertainment")
    }