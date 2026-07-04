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

    # If this is a new user, create default preferences
    if result is None:

        print(f"No preferences found for user {user_id}. Creating defaults.")

        cursor.execute("""
            INSERT INTO preferences (
                user_id,
                country,
                state,
                language,
                voice,
                categories,
                duration
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            "India",
            "Karnataka",
            "English",
            "Male",
            '["Technology"]',
            20
        ))

        conn.commit()

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

    # Check whether preferences already exist
    cursor.execute(
        "SELECT id FROM preferences WHERE user_id = ?",
        (user_id,)
    )

    existing = cursor.fetchone()

    if existing:

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

        print("Preferences Updated!")

    else:

        cursor.execute("""
            INSERT INTO preferences (
                user_id,
                country,
                state,
                language,
                voice,
                categories,
                duration
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            country,
            state,
            language,
            voice,
            categories,
            duration
        ))

        print("Preferences Created!")

    conn.commit()
    conn.close()