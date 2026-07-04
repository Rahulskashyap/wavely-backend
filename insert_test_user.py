import sqlite3

conn = sqlite3.connect("news_podcast.db")

cursor = conn.cursor()

cursor.execute("""
INSERT INTO users (name, email)
VALUES (?, ?)
""", (
    "Rahul",
    "rahul@test.com"
))

conn.commit()

print("User Added!")

conn.close()