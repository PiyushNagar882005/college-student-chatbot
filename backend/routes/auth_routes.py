from flask import Blueprint, request, jsonify

from database.db import get_db_connection


auth_bp = Blueprint(
    "auth",
    __name__
)


# Register

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")

    password = data.get("password")

    conn = get_db_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password)

            VALUES (?, ?)
            """,
            (username, password)
        )

        conn.commit()

        return jsonify({
            "message": "Registration successful"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400

    finally:

        conn.close()


# Login

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")

    password = data.get("password")

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ?
        AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return jsonify({
            "message": "Login successful"
        })

    return jsonify({
        "error": "Invalid credentials"
    }), 401