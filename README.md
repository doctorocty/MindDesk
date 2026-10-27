# MindDesk

<p align="center">
  <img src="https://img.shields.io/badge/MindDesk-Personal%20Productivity-DB7093?style=for-the-badge&labelColor=FCE4EC" alt="MindDesk Personal Productivity">
</p>

<p align="center">
  A modern study workspace for organizing tasks, tracking goals, and staying focused.
</p>

<p align="center">
  <a href="https://mind-desk-ao9w.vercel.app/">Live Demo</a>
  &nbsp; · &nbsp;
  <a href="https://github.com/doctorocty/MindDesk">Source Code</a>
  &nbsp; · &nbsp;
  <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-DB7093?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-CB668F?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-BB668F?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/HTML5-E8A0BF?style=flat-square&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-D98AB5?style=flat-square&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-C77D9A?style=flat-square&logo=javascript&logoColor=white" alt="JavaScript">
</p>

---

## About

MindDesk is a student productivity web application built to bring everyday planning into one organized workspace.

From managing daily tasks to tracking personal goals, writing notes, and running focus sessions, MindDesk helps you keep your responsibilities organized and your attention on what matters.

The project combines a lightweight frontend with a Python and Flask backend to deliver a practical, responsive productivity experience.

## Features

### Task Management

Organize daily responsibilities and keep track of what needs to be done.

- Create, complete, and delete tasks.
- Keep important work visible.
- Manage tasks alongside your other productivity tools.

### Goal Tracking

Turn long-term ambitions into goals you can monitor over time.

- Create personal goals.
- Track progress toward your objectives.
- Update goals as your priorities evolve.

### Notes

Keep important information and ideas accessible in your workspace.

- Create notes.
- Edit existing notes.
- Delete notes when they are no longer needed.

### Focus Sessions

Set aside dedicated time for concentrated work or study.

- Start customizable focus sessions.
- Structure your work into focused periods.
- Keep track of focus time from your dashboard.

### Productivity Dashboard

Get a convenient overview of your productivity.

- View tasks and goals.
- Access recent notes.
- Review your focus time.

### Dark Mode

Switch to a darker interface for a different viewing experience.

### Responsive Interface

Use a clean, organized interface designed to make the main productivity tools easy to access.

### User Authentication

Sign up and log in to access your productivity workspace.

## Tech Stack

MindDesk uses a lightweight full-stack web development stack.

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| Flask | Web framework and routing |
| PostgreSQL | Relational database |
| HTML5 | Page structure |
| CSS3 | Styling and layout |
| Vanilla JavaScript | Frontend interactivity |
| Jinja | Dynamic HTML templating |
| Vercel | Deployment and hosting |

The frontend uses standard web technologies rather than a large JavaScript framework, keeping the application focused on the fundamentals of web development.

## Getting Started

Follow these steps to run MindDesk locally.

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or newer
- PostgreSQL
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/doctorocty/MindDesk.git
```

### 2. Navigate to the project folder

```bash
cd MindDesk
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the database

Create a `.env` file in the project's root directory and configure your PostgreSQL connection:

```env
DATABASE_URL=your_postgresql_connection_string
```

Replace the placeholder with your actual connection string. Make sure PostgreSQL is running and the target database exists.

Keep your `.env` file private. Never commit your database credentials to the repository.

### 6. Start the application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

The application initializes the required database tables when it starts.

## Project Structure

```text
MindDesk/
├── api/                 # API and deployment-related files
├── static/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── media/           # Images and icons
├── templates/           # HTML and Jinja templates
├── .env.example         # Example environment configuration
├── .gitignore           # Git ignore rules
├── app.py               # Flask application and routes
├── config.py            # Application configuration
├── database.py          # Database operations
├── requirements.txt     # Python dependencies
└── vercel.json          # Vercel configuration
```

## Future Improvements

Potential areas for future development include:

- More detailed productivity analytics.
- Advanced task filtering and prioritization.
- Goal milestones and progress visualizations.
- Calendar integration and study scheduling.
- Additional accessibility and personalization options.

These are possible future enhancements, not a claim that they are already implemented.

## Contributing

Suggestions, feedback, and contributions are welcome.

1. Fork the repository.
2. Create a branch for your changes.
3. Implement and test your improvements.
4. Commit your changes with a descriptive message.
5. Open a pull request explaining the changes.

For larger improvements, opening an issue first can help establish the approach before development begins.

## License

MindDesk is licensed under the **MIT License**.

The MIT License permits use, copying, modification, distribution, sublicensing, and sale of the software, subject to its conditions, including retaining the required copyright notice and license text in redistributions.

See the [`LICENSE`](LICENSE) file for the complete terms.

## Author

**Sarah Fatima Lari**

- GitHub: [@doctorocty](https://github.com/doctorocty)
- Portfolio: [sarahs-portfolio-inky.vercel.app](https://sarahs-portfolio-inky.vercel.app/)

---

<p align="center">
  <sub>Built with curiosity, thoughtful design, and a passion for creating useful things.</sub>
</p>
