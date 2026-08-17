from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database import (
    initialize_database,
    email_exists,
    create_user,
    get_user_by_email
)

from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

initialize_database()


@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not full_name or not email or not password or not confirm_password:
            return render_template(
                "auth/signup.html",
                error="Please fill in all fields."
            )

        if password != confirm_password:
            return render_template(
                "auth/signup.html",
                error="Passwords do not match."
            )

        if email_exists(email):
            return render_template(
                "auth/signup.html",
                error="An account with this email already exists."
            )

        hashed_password = generate_password_hash(password)

        create_user(
            full_name,
            email,
            hashed_password
        )

        return redirect(url_for("login"))

    return render_template("auth/signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template(
                "auth/login.html",
                error="Please fill in all fields."
            )

        user = get_user_by_email(email)

        if user is None:
            flash("No account exists with that email.", "error")
            return redirect(url_for("login"))

        if not check_password_hash(user["password"], password):
           flash("Incorrect password.", "error")
           return redirect(url_for("login"))

        session["user_id"] = user["id"]
        session["user_name"] = user["full_name"]

        flash(f"Welcome back, {user['full_name']}!", "success")

        return redirect(url_for("dashboard"))

        return redirect(url_for("dashboard"))

    return render_template("auth/login.html")
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email")

        flash(
            f"A verification code would be sent to {email}.",
            "success"
        )

        return redirect(url_for("forgot_password"))

    return render_template("auth/forgot_password.html")


@app.route("/dashboard")
def dashboard():

    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    user_name = session.get("user_name", "there")

    return render_template(
        "dashboard.html",
        user_name=user_name,
        greeting=greeting,
        logged_in="user_id" in session
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )