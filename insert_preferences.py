import sqlite3

conn = sqlite3.connect("news_podcast.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO preferences (
    user_id,
    state,
    language,
    news_mode,
    voice,
    podcast_length
)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    1,
    "Karnataka",
    "Kannada",
    "Hybrid",
    "Female",
    40
))

conn.commit()

print("Preferences Added!")

conn.close()