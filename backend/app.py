from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

import os
import json

from dotenv import load_dotenv

from routes.pdf_routes import pdf_bp
from rag.retriever import retrieve_relevant_chunks


# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

CORS(app)

app.register_blueprint(pdf_bp)


# ==========================================
# FILE PATHS
# ==========================================

USERS_FILE = "users.json"

HISTORY_FILE = "chat_history.json"


# ==========================================
# CREATE FILES IF NOT EXISTS
# ==========================================

if not os.path.exists(USERS_FILE):

    with open(USERS_FILE, "w") as f:

        json.dump([], f)


if not os.path.exists(HISTORY_FILE):

    with open(HISTORY_FILE, "w") as f:

        json.dump([], f)


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message":
        "College Student Chatbot Backend Running"
    })


# ==========================================
# REGISTER ROUTE
# ==========================================

@app.route("/register", methods=["POST"])
def register():

    try:

        data = request.json

        username = data.get("username")

        password = data.get("password")


        if not username or not password:

            return jsonify({
                "message":
                "All fields are required"
            }), 400


        with open(USERS_FILE, "r") as f:

            users = json.load(f)


        for user in users:

            if user["username"] == username:

                return jsonify({
                    "message":
                    "User already exists"
                }), 400


        users.append({

            "username": username,

            "password": password
        })


        with open(USERS_FILE, "w") as f:

            json.dump(users, f, indent=4)


        return jsonify({
            "message":
            "Registration successful"
        })


    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# LOGIN ROUTE
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.json

        username = data.get("username")

        password = data.get("password")


        with open(USERS_FILE, "r") as f:

            users = json.load(f)


        for user in users:

            if (
                user["username"] == username
                and
                user["password"] == password
            ):

                return jsonify({
                    "message":
                    "Login successful"
                })


        return jsonify({
            "message":
            "Invalid credentials"
        }), 401


    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# CHAT ROUTE
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.json

        username = data.get("username")

        user_message = data.get("message")

        print("\n===================================")

        print(f"User Question: {user_message}")

        print("===================================\n")


        # ==========================================
        # RETRIEVE RELEVANT CHUNKS
        # ==========================================

        chunks = retrieve_relevant_chunks(
            user_message
        )


        context = "\n".join(chunks)


        print("\nRetrieved Context:\n")

        print(context)


        # ==========================================
        # PROMPT
        # ==========================================

        prompt = f"""
        You are a helpful college student assistant.

        Answer ONLY using the provided context.

        If answer is not found in context,
        reply exactly:

        "I could not find this in uploaded notes."

        Context:
        {context}

        Question:
        {user_message}
        """


        # ==========================================
        # GROQ API
        # ==========================================

        response = client.chat.completions.create(

           model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",

                    "content":
                    "You are a helpful college assistant."
                },

                {
                    "role": "user",

                    "content": prompt
                }
            ],

            temperature=0.3,

            max_tokens=500
        )


        bot_reply = (
            response
            .choices[0]
            .message.content
        )


        print("\nBot Reply:\n")

        print(bot_reply)


        # ==========================================
        # SAVE CHAT HISTORY
        # ==========================================

        with open(HISTORY_FILE, "r") as f:

            chats = json.load(f)


        chats.append({

            "id": len(chats) + 1,

            "username": username,

            "user_message": user_message,

            "bot_response": bot_reply
        })


        with open(HISTORY_FILE, "w") as f:

            json.dump(chats, f, indent=4)


        # ==========================================
        # RETURN RESPONSE
        # ==========================================

        return jsonify({
            "response": bot_reply
        })


    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# GET CHAT HISTORY
# ==========================================

@app.route("/history/<username>", methods=["GET"])
def history(username):

    try:

        with open(HISTORY_FILE, "r") as f:

            chats = json.load(f)


        user_chats = [

            chat for chat in chats

            if chat["username"] == username
        ]


        return jsonify(user_chats)


    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# DELETE CHAT ROUTE
# ==========================================

@app.route("/delete-chat/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):

    try:

        with open(HISTORY_FILE, "r") as f:

            chats = json.load(f)


        chats = [
            chat for chat in chats
            if chat.get("id") != chat_id
        ]


        with open(HISTORY_FILE, "w") as f:

            json.dump(chats, f, indent=4)


        return jsonify({
            "message": "Chat deleted successfully"
        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# LOGOUT ROUTE
# ==========================================

@app.route("/logout")
def logout():

    return jsonify({
        "message":
        "Logout successful"
    })


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )