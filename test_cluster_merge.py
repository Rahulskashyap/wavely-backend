from news_v4.clusterer import cluster_articles


articles = [
    {
        "publisher": "BBC",
        "title": "Salman Rushdie attacker convicted of terror offences",
        "summary": (
            "Hadi Matar, 28, was convicted of attempting to help "
            "Hezbollah by attacking the British-Indian author."
        ),
        "categories": ["world", "national"],
        "region": "world",
    },
    {
        "publisher": "Indian Express",
        "title": (
            "Man who stabbed author Salman Rushdie convicted "
            "of terror offences"
        ),
        "summary": "",
        "categories": ["world"],
        "region": "world",
    },
    {
        "publisher": "Hindustan Times",
        "title": (
            "Salman Rushdie's stabbing suspect Hadi Matar convicted "
            "in New York terrorism trial"
        ),
        "summary": (
            "Hadi Matar was convicted on federal terrorism charges "
            "for the 2022 stabbing of Salman Rushdie, adding a "
            "potential life sentence to his existing 25-year term."
        ),
        "categories": ["world"],
        "region": "world",
    },
    {
        "publisher": "NDTV",
        "title": (
            "Author Salman Rushdie's Attacker Hadi Matar "
            "Convicted On Terrorism Charges"
        ),
        "summary": (
            "Rushdie, 79, had faced threats on his life since the "
            "1988 publication of his novel The Satanic Verses."
        ),
        "categories": ["world"],
        "region": "world",
    },
]


clusters = cluster_articles(articles)


print("\n==============================")
print("CLUSTER MERGE TEST")
print("==============================")

print("ARTICLES:", len(articles))
print("CLUSTERS:", len(clusters))


for index, cluster in enumerate(clusters, start=1):

    print("\n------------------------------")
    print("CLUSTER:", index)
    print("SIZE:", len(cluster["articles"]))

    for article in cluster["articles"]:

        print(
            "-",
            article["publisher"],
            "|",
            article["title"],
        )


print("\n==============================")

if len(clusters) == 1:
    print("PASS: ALL ARTICLES MERGED")
else:
    print(
        "FAIL:",
        len(clusters),
        "CLUSTERS CREATED",
    )