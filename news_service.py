import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def get_global_news():

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "language": "en",
        "pageSize": 100,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    return response.json()