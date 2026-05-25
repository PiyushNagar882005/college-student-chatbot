import sqlite3


def get_db_connection():

    conn = sqlite3.connect(
        "college_chatbot.db"
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db_connection()

    cursor = conn.cursor()

    # Users table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT
    )
    """)

    # Chat history table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        user_message TEXT,

        bot_response TEXT
    )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":

    init_db()

    print("Database Created")