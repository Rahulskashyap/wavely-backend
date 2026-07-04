import sqlite3

conn = sqlite3.connect("news_podcast.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM preferences")

rows = cursor.fetchall()

print(rows)

conn.close()