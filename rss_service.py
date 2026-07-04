import feedparser

def get_google_news(topic):

    url = f"https://news.google.com/rss/search?q={topic}&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:20]:

        articles.append({
            "title": entry.title,
            "link": entry.link
        })

    return articles