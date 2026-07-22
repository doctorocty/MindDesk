from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from config import Config
from database import initialize_database, email_exists, create_user



app = Flask(__name__)
print(">>> THIS IS THE APP.PY THAT FLASK IS RUNNING <<<")
app.config.from_object(Config)

initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    app.logger.info(f"Request Method: {request.method}")

    if request.method == "POST":

        app.logger.info(f"Form Data: {request.form}")

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

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

        print("----- New Sign Up -----")
        print("Full Name:", full_name)
        print("Email:", email)
        print("Hashed Password:", hashed_password)

    return render_template("auth/signup.html")

@app.route("/login")
def login():
    return render_template("auth/login.html")


if __name__ == "__main__":
    app.run(debug=True)