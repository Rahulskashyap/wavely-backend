import sqlite3

DB_NAME = "news_podcast.db"


def get_user_preferences(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT country,
           state,
           language,
           voice,
           categories,
           duration
    FROM preferences
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    print("Database Result:", result)

    conn.close()

    return result


def update_user_preferences(
        user_id,
        country,
        state,
        language,
        voice,
        categories,
        duration
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
UPDATE preferences
SET country = ?,
    state = ?,
    language = ?,
    voice = ?,
    categories = ?,
    duration = ?
WHERE user_id = ?
""", (
    country,
    state,
    language,
    voice,
    categories,
    duration,
    user_id
))

    conn.commit()
    conn.close()

    print("Preferences Updated!")