from flask import Blueprint, request, session, redirect, jsonify
from auth.google_auth import verify_google_token
from database.db import query_db, execute_db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():

    token = request.json.get("credential")

    user_data = verify_google_token(token)

    if not user_data:
        return jsonify({"error": "Unauthorized domain"}), 403

    user = query_db(
        "SELECT * FROM users WHERE google_id=?",
        (user_data["google_id"],),
        one=True
    )

    if not user:
        execute_db("""
            INSERT INTO users (google_id, email, name)
            VALUES (?, ?, ?)
        """, (
            user_data["google_id"],
            user_data["email"],
            user_data["name"]
        ))

    session["user_email"] = user_data["email"]

    return jsonify({"success": True})


@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")