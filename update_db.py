import sqlite3

conn = sqlite3.connect("news_podcast.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE preferences
ADD COLUMN country TEXT DEFAULT 'India'
""")

cursor.execute("""
ALTER TABLE preferences
ADD COLUMN categories TEXT DEFAULT '["Technology"]'
""")

cursor.execute("""
ALTER TABLE preferences
ADD COLUMN duration INTEGER DEFAULT 20
""")

conn.commit()
conn.close()

print("Database Updated!")
