from flask import Flask, render_template, session, redirect
from database.db import close_db
from routes.auth_routes import auth

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"

app.register_blueprint(auth)

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

@app.route("/login_page")
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)