MindDesk: https://mind-desk-ao9w.vercel.app/ is a student productivity and study workspace built with Python, Flask, PostgreSQL, HTML, CSS, and JavaScript. It brings tasks, goals, notes, and focus sessions into one simple workspace. You can create, complete, and delete tasks, create goals and track their progress, create, edit and delete notes, use dark mode, and start customizable focus sessions. The dashboard gives you a quick overview of your tasks, goals, recent notes, and focus time. This started as a small project and slowly turned into an actual app lol, and I'm pretty happy with how it turned out!:3

Requirements

Python 3.10 or newer
PostgreSQL
pip
A virtual environment

Installation

1. Clone or download the repository.

2. Open the project folder in VS Code or your terminal.

3. Create a virtual environment.

python -m venv venv

4. Activate the virtual environment on Windows.

venv\Scripts\activate

5. Install the required packages.

pip install -r requirements.txt

6. Create a .env file in the main project folder.

7. Add your PostgreSQL connection information.

DATABASE_URL=your_postgresql_connection_string

8. Make sure PostgreSQL is running and that the database in your connection string exists.

9. Start the application.

python app.py

10. Open your browser and go to:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

The application will initialize the required database tables when it starts.

Project Structure

app.py contains the Flask application and routes
database.py contains the PostgreSQL database functions
templates contains the HTML and Jinja templates
static/css contains the application's stylesheets
static/js contains the JavaScript
static/media contains images and icons
requirements.txt contains the Python dependencies
.env contains private environment variables and should not be uploaded to gitHub

Main Features

User signup and login
Task management
Goal tracking
Notes with editing and deleting
Focus timer
Dashboard
Dark mode
Responsive UI

To run MindDesk again after installation, activate the virtual environment and run python app.py,
Please keep your .env file private because it contains your database connection information.
Built with Python, Flask, PostgreSQL, HTML, CSS and JavaScript 
