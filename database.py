import sqlite3

conn = sqlite3.connect("news_podcast.db")

cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Preferences Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    country TEXT,
    state TEXT,
    language TEXT,
    voice TEXT,
    categories TEXT,
    duration INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Podcasts Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS podcasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    podcast_date TEXT,
    podcast_file TEXT,
    language TEXT,
    duration INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()

print("Database Created Successfully!")

conn.close()