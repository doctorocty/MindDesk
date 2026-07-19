from flask import Flask, render_template
from config import Config
from database import initialize_database

app = Flask(__name__)
app.config.from_object(Config)

initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)