from flask import Flask, render_template, session, redirect, request, jsonify
from database.db import close_db, query_db, execute_db
from auth.google_auth import verify_google_token
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"


@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db()

@app.route("/")
def home():
    return render_template(
        "index.html",
        user=session.get("user_email")
    )

@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect("/")
    return f"Logged in as {session['user_email']}"

@app.route("/login")
def login_page():
    return render_template(
        "login.html",
        client_id=os.getenv("GOOGLE_CLIENT_ID")
    )

@app.route("/login", methods=["POST"])
def login_data():

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)