import sqlite3
import json

conn = sqlite3.connect("news_podcast.db")
cursor = conn.cursor()

# Create default user
cursor.execute("""
INSERT OR IGNORE INTO users(id, name, email)
VALUES(1, 'Rahul', 'rahul@example.com')
""")

# Remove old preferences if any
cursor.execute("""
DELETE FROM preferences
WHERE user_id = 1
""")

# Insert default preferences
cursor.execute("""
INSERT INTO preferences(
    user_id,
    country,
    state,
    language,
    voice,
    categories,
    duration
)
VALUES(
    ?, ?, ?, ?, ?, ?, ?
)
""", (
    1,
    "India",
    "Karnataka",
    "English",
    "Female",
    json.dumps([
        "Technology",
        "Business",
        "Sports"
    ]),
    15
))

conn.commit()
conn.close()

print("Default preferences inserted successfully!")