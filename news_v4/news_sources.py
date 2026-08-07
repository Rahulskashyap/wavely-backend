# news_v4/sources.py


SOURCES = [

    # =========================================================
    # WORLD — BBC
    # =========================================================

    {
        "id": "bbc_world",
        "publisher_id": "bbc",
        "name": "BBC News",
        "type": "publisher",
        "region": "world",
        "categories": ["world", "national"],
        "method": "rss",
        "url": "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/world/rss.xml",
    },

    {
        "id": "bbc_business",
        "publisher_id": "bbc",
        "name": "BBC News",
        "type": "publisher",
        "region": "world",
        "categories": ["business"],
        "method": "rss",
        "url": "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/business/rss.xml",
    },

    {
        "id": "bbc_technology",
        "publisher_id": "bbc",
        "name": "BBC News",
        "type": "publisher",
        "region": "world",
        "categories": ["technology"],
        "method": "rss",
        "url": "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/technology/rss.xml",
    },

    {
        "id": "bbc_health",
        "publisher_id": "bbc",
        "name": "BBC News",
        "type": "publisher",
        "region": "world",
        "categories": ["health"],
        "method": "rss",
        "url": "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/health/rss.xml",
    },

    {
        "id": "bbc_entertainment",
        "publisher_id": "bbc",
        "name": "BBC News",
        "type": "publisher",
        "region": "world",
        "categories": ["entertainment"],
        "method": "rss",
        "url": "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/entertainment/rss.xml",
    },

    {
        "id": "bbc_cricket",
        "publisher_id": "bbc",
        "name": "BBC Sport",
        "type": "publisher",
        "region": "world",
        "categories": ["sports", "cricket"],
        "method": "rss",
        "url": "http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/cricket/rss.xml",
    },


    # =========================================================
    # INDIA — INDIAN EXPRESS
    # =========================================================

    {
        "id": "indian_express_india",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "india",
        "categories": ["national"],
        "method": "rss",
        "url": "https://indianexpress.com/section/india/feed/",
    },

    {
        "id": "indian_express_world",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "world",
        "categories": ["world"],
        "method": "rss",
        "url": "https://indianexpress.com/section/world/feed/",
    },

    {
        "id": "indian_express_business",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "india",
        "categories": ["business"],
        "method": "rss",
        "url": "https://indianexpress.com/section/business/feed/",
    },

    {
        "id": "indian_express_cricket",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "india",
        "categories": ["sports", "cricket"],
        "method": "rss",
        "url": "https://indianexpress.com/section/sports/cricket/feed/",
    },

    {
        "id": "indian_express_mangaluru",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://indianexpress.com/section/cities/mangaluru/feed/",
    },

    {
        "id": "indian_express_chennai",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "tamil_nadu",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://indianexpress.com/section/cities/chennai/feed/",
    },

    {
        "id": "indian_express_kerala",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "kerala",
        "categories": ["state"],
        "method": "rss",
        "url": "https://indianexpress.com/section/india/kerala/feed/",
    },

    {
        "id": "indian_express_mumbai",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "maharashtra",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://indianexpress.com/section/cities/mumbai/feed/",
    },

    {
        "id": "indian_express_kolkata",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "west_bengal",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://indianexpress.com/section/cities/kolkata/feed/",
    },

    {
        "id": "indian_express_lucknow",
        "publisher_id": "indian_express",
        "name": "The Indian Express",
        "type": "publisher",
        "region": "uttar_pradesh",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://indianexpress.com/section/cities/lucknow/feed/",
    },


    # =========================================================
    # KARNATAKA — PUBLIC TV
    # =========================================================

    {
        "id": "publictv_main",
        "publisher_id": "public_tv",
        "name": "Public TV",
        "type": "publisher",
        "region": "karnataka",
        "categories": [
            "state",
            "local",
            "national",
            "world",
            "technology",
            "sports",
            "entertainment",
        ],
        "method": "rss",
        "url": "https://publictv.in/feed",
    },


    # =========================================================
    # KARNATAKA — KANNADA ONEINDIA
    # =========================================================

    {
        "id": "oneindia_kannada_news",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "national"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-news-fb.xml",
    },

    {
        "id": "oneindia_bengaluru",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-bengaluru-fb.xml",
    },

    {
        "id": "oneindia_mysuru",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-mysuru-fb.xml",
    },

    {
        "id": "oneindia_mangaluru",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-mangaluru-fb.xml",
    },

    {
        "id": "oneindia_belagavi",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-belagavi-fb.xml",
    },

    {
        "id": "oneindia_dharwad",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-dharwad-fb.xml",
    },

    {
        "id": "oneindia_shivamogga",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-shivamogga-fb.xml",
    },

    {
        "id": "oneindia_tumakuru",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-tumakuru-fb.xml",
    },

    {
        "id": "oneindia_entertainment",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["entertainment"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/kannada-entertainment-fb.xml",
    },

    {
        "id": "oneindia_ai",
        "publisher_id": "oneindia_kannada",
        "name": "Kannada Oneindia",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["technology", "ai"],
        "method": "rss",
        "url": "https://kannada.oneindia.com/rss/feeds/artificial-intelligence-fb.xml",
    },


    # =========================================================
    # INDIA — HINDUSTAN TIMES
    # =========================================================

    {
        "id": "ht_india",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "india",
        "categories": ["national"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
    },

    {
        "id": "ht_world",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "world",
        "categories": ["world"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/world-news/rssfeed.xml",
    },

    {
        "id": "ht_bengaluru",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "karnataka",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/cities/bengaluru-news/rssfeed.xml",
    },

    {
        "id": "ht_mumbai",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "maharashtra",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/cities/mumbai-news/rssfeed.xml",
    },

    {
        "id": "ht_kolkata",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "west_bengal",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/cities/kolkata-news/rssfeed.xml",
    },

    {
        "id": "ht_lucknow",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "uttar_pradesh",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/cities/lucknow-news/rssfeed.xml",
    },

    {
        "id": "ht_pune",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "maharashtra",
        "categories": ["state", "local"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/cities/pune-news/rssfeed.xml",
    },

    {
        "id": "ht_technology",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "india",
        "categories": ["technology"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/technology/rssfeed.xml",
    },

    {
        "id": "ht_sports",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "india",
        "categories": ["sports"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/sports/rssfeed.xml",
    },

    {
        "id": "ht_cricket",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "india",
        "categories": ["sports", "cricket"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/cricket/rssfeed.xml",
    },

    {
        "id": "ht_entertainment",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "india",
        "categories": ["entertainment"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/entertainment/rssfeed.xml",
    },

    {
        "id": "ht_health",
        "publisher_id": "hindustan_times",
        "name": "Hindustan Times",
        "type": "publisher",
        "region": "india",
        "categories": ["health"],
        "method": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/lifestyle/health/rssfeed.xml",
    },


    # =========================================================
    # INDIA — NDTV
    #
    # Start with the established FeedBurner feeds below.
    # We'll test each endpoint through the collector.
    # =========================================================

    {
        "id": "ndtv_india",
        "publisher_id": "ndtv",
        "name": "NDTV",
        "type": "publisher",
        "region": "india",
        "categories": ["national"],
        "method": "rss",
        "url": "https://feeds.feedburner.com/ndtvnews-india-news",
    },

    {
        "id": "ndtv_world",
        "publisher_id": "ndtv",
        "name": "NDTV",
        "type": "publisher",
        "region": "world",
        "categories": ["world"],
        "method": "rss",
        "url": "https://feeds.feedburner.com/ndtvnews-world-news",
    },

    {
        "id": "ndtv_business",
        "publisher_id": "ndtv",
        "name": "NDTV",
        "type": "publisher",
        "region": "india",
        "categories": ["business"],
        "method": "rss",
        "url": "https://feeds.feedburner.com/ndtvprofit-latest",
    },

    {
        "id": "ndtv_technology",
        "publisher_id": "ndtv",
        "name": "NDTV",
        "type": "publisher",
        "region": "india",
        "categories": ["technology"],
        "method": "rss",
        "url": "https://feeds.feedburner.com/gadgets360-latest",
    },

 {
    "id": "tv9_kannada_karnataka",
    "publisher_id": "tv9_kannada",
    "name": "TV9 Kannada",
    "type": "publisher",
    "region": "karnataka",
    "categories": ["state", "local"],

    "method": "website_links",

    "url": "https://tv9kannada.com/karnataka",

    "allowed_path_prefixes": [
        "/karnataka/",
    ],

    "excluded_path_prefixes": [
        "/videos/",
        "/photo-gallery/",
        "/web-stories/",
    ],

    "article_url_pattern": r"-\d+\.html$",
},


    # =========================================================
    # PRIMARY / OFFICIAL SOURCES
    # =========================================================

    {
        "id": "nasa",
        "publisher_id": "nasa",
        "name": "NASA",
        "type": "primary",
        "region": "world",
        "categories": ["technology", "science", "world"],
        "method": "rss",
        "url": "https://www.nasa.gov/news-release/feed/",
    },
]


def get_sources():
    return SOURCES


def get_source(source_id):
    for source in SOURCES:
        if source["id"] == source_id:
            return source

    return None