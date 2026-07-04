import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

url = "https://newsapi.org/v2/everything"

params = {
    "q": "India",
    "pageSize": 20,
    "sortBy": "publishedAt",
    "apiKey": API_KEY
}

response = requests.get(url, params=params)

print(response.json())