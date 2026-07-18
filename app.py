from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from database import initialize_database, get_connection

app = Flask(__name__)

app.secret_key = "minddesk-secret-key"

initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""

    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            message = "An account with this email already exists."

        else:
            hashed_password = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO users (full_name, email, password)
                VALUES (?, ?, ?)
                """,
                (full_name, email, hashed_password)
            )

            connection.commit()
            connection.close()

            return redirect(url_for("home"))

        connection.close()

    return render_template("signup.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)  