from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config

from database import (
    initialize_database,
    email_exists,
    create_user,
    get_user_by_email,
    create_task,
    get_tasks,
    get_today_tasks,
    toggle_task,
    delete_task,
    get_task_counts,
    create_goal,
    get_goals,
    get_active_goals,
    update_goal_progress,
    delete_goal,
    get_goal_counts,
    create_note,
    get_notes,
    get_recent_notes,
    update_note,
    delete_note
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

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if (
            not full_name
            or not email
            or not password
            or not confirm_password
        ):

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

        hashed_password = generate_password_hash(
            password
        )

        create_user(
            full_name,
            email,
            hashed_password
        )

        flash(
            "Account created successfully. Please log in.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "auth/signup.html"
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not email or not password:

            return render_template(
                "auth/login.html",
                error="Please fill in all fields."
            )

        user = get_user_by_email(email)

        if user is None:

            flash(
                "No account exists with that email.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        if not check_password_hash(
            user["password"],
            password
        ):

            flash(
                "Incorrect password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        session["user_id"] = user["id"]

        session["user_name"] = user["full_name"]

        flash(
            f"Welcome back, {user['full_name']}!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "auth/login.html"
    )

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        flash(
            f"A verification code would be sent to {email}.",
            "success"
        )

        return redirect(
            url_for("forgot_password")
        )

    return render_template(
        "auth/forgot_password.html"
    )

@app.route("/dashboard")
def dashboard():

    current_hour = datetime.now().hour

    if current_hour < 12:

        greeting = "Good morning"

    elif current_hour < 18:

        greeting = "Good afternoon"

    else:

        greeting = "Good evening"


    user_id = session.get(
        "user_id"
    )


    user_name = session.get(
        "user_name",
        "there"
    )


    if not user_id:

        counts = {
            "total_tasks": 0,
            "completed_tasks": 0
        }

        today_tasks = []

        goal_counts = {
            "active_goals": 0
        }

        active_goals = []
        recent_notes = []

    else:

        counts = get_task_counts(
            user_id
        )

        all_tasks = get_tasks(
            user_id
        )

        goal_counts = get_goal_counts(
            user_id
        )

        active_goals = get_active_goals(
            user_id
        )

        recent_notes = get_recent_notes(
            user_id,
            5
        )


        today_tasks = []

        for task in all_tasks:

            if task["completed"]:

                continue

            today_tasks.append(
                task
            )

    return render_template(

        "dashboard.html",

        greeting=greeting,

        user_name=user_name,

        logged_in=(
            "user_id" in session
        ),

        total_tasks=counts[
            "total_tasks"
        ],

        completed_tasks=counts[
            "completed_tasks"
        ],

        today_tasks=today_tasks,

        recent_notes=recent_notes,

        active_goals=active_goals,
        

        active_goals_count=goal_counts[
            "active_goals"
        ]

    )

@app.route("/focus")
def focus():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    return render_template(
        "focus.html"
    )

@app.route("/notes")
def notes():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    user_notes = get_notes(
        user_id
    )

    return render_template(
        "notes.html",
        notes=user_notes
    )

@app.route("/notes/<int:note_id>/edit", methods=["POST"])
def edit_note_route(note_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get(
        "title",
        ""
    ).strip()

    content = request.form.get(
        "content",
        ""
    ).strip()

    if not title:

        flash(
            "Please enter a note title.",
            "error"
        )

        return redirect(
            url_for("notes")
        )

    update_note(
        note_id,
        session["user_id"],
        title,
        content
    )

    flash(
        "Note updated successfully.",
        "success"
    )

    return redirect(
        url_for("notes")
    )

@app.route(
    "/notes/create",
    methods=["POST"]
)
def create_note_route():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    title = request.form.get(
        "title",
        ""
    ).strip()

    content = request.form.get(
        "content",
        ""
    ).strip()

    if not title:

        flash(
            "Please enter a note title.",
            "error"
        )

        return redirect(
            url_for("notes")
        )

    create_note(
        session["user_id"],
        title,
        content
    )

    flash(
        "Note created successfully.",
        "success"
    )

    return redirect(
        url_for("notes")
    )

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note_route(note_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_note(
        note_id,
        session["user_id"]
    )

    flash(
        "Note deleted.",
        "success"
    )

    return redirect(
        url_for("notes")
    )

@app.route("/tasks")
def tasks():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session[
        "user_id"
    ]


    user_tasks = get_tasks(
        user_id
    )


    return render_template(

        "tasks.html",

        tasks=user_tasks

    )

@app.route("/goals")
def goals():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user_id = session[
        "user_id"
    ]

    user_goals = get_goals(
        user_id
    )

    return render_template(

        "goals.html",

        goals=user_goals

    )

@app.route(
    "/goals/create",
    methods=["POST"]
)
def create_goal_route():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    title = request.form.get(
        "title",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    target_date = request.form.get(
        "target_date"
    ) or None

    if not title:

        flash(
            "Please enter a goal title.",
            "error"
        )

        return redirect(
            url_for("goals")
        )

    create_goal(

        session["user_id"],

        title,

        description,

        target_date

    )

    flash(
        "Goal added successfully.",
        "success"
    )

    return redirect(
        url_for("goals")
    )

@app.route(
    "/goals/<int:goal_id>/delete",
    methods=["POST"]
)
def delete_goal_route(goal_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    delete_goal(

        goal_id,

        session["user_id"]

    )

    flash(
        "Goal deleted.",
        "success"
    )

    return redirect(
        url_for("goals")
    )

@app.route(
    "/goals/<int:goal_id>/progress",
    methods=["POST"]
)
def update_goal_progress_route(goal_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    progress = request.form.get(
        "progress",
        0
    )

    try:

        progress = int(progress)

    except (ValueError, TypeError):

        flash(
            "Invalid progress value.",
            "error"
        )

        return redirect(
            url_for("goals")
        )

    update_goal_progress(

        goal_id,

        session["user_id"],

        progress

    )

    return redirect(
        url_for("goals")
    )

@app.route(
    "/tasks/create",
    methods=["POST"]
)
def create_task_route():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    title = request.form.get(
        "title",
        ""
    ).strip()


    description = request.form.get(
        "description",
        ""
    ).strip()


    due_date = request.form.get(
        "due_date"
    ) or None


    priority = request.form.get(
        "priority",
        "medium"
    )


    if not title:

        flash(
            "Please enter a task title.",
            "error"
        )

        if request.referrer and "/dashboard" in request.referrer:

            return redirect(
                url_for("dashboard")
            )


        return redirect(
            url_for("tasks")
        )


    create_task(

        session["user_id"],

        title,

        description,

        due_date,

        priority

    )


    flash(
        "Task added successfully.",
        "success"
    )

    if request.referrer and "/dashboard" in request.referrer:

        return redirect(
            url_for("dashboard")
        )


    return redirect(
        url_for("tasks")
    )

@app.route(
    "/tasks/<int:task_id>/toggle",
    methods=["POST"]
)
def toggle_task_route(task_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    toggle_task(

        task_id,

        session["user_id"]

    )

    if request.referrer and "/dashboard" in request.referrer:

        return redirect(
            url_for("dashboard")
        )


    return redirect(
        url_for("tasks")
    )

@app.route(
    "/tasks/<int:task_id>/delete",
    methods=["POST"]
)
def delete_task_route(task_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    delete_task(

        task_id,

        session["user_id"]

    )


    flash(
        "Task deleted.",
        "success"
    )


    if request.referrer and "/dashboard" in request.referrer:

        return redirect(
            url_for("dashboard")
        )


    return redirect(
        url_for("tasks")
    )

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("login")
    )

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )