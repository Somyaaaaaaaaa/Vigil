FOLDER STRUCTURE
VIGIL/
├── app.py           # main Flask app
├── models.py        # database models
├── templates/       # HTML pages
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   └── home.html
├── static/          # CSS / JS / images
│   └── style.css
└── database.db      # SQLite database

STEP 2 — SET UP ENVIRONMENT

Open VS Code and navigate to VIGIL.

Create a Python virtual environment:

python -m venv venv


Activate it:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Install Flask + SQLAlchemy:

pip install flask flask_sqlalchemy flask_bcrypt flask_login
