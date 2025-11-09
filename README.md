# Cocina - Flask Recipes App

A simple recipe app built with Flask, SQLAlchemy (SQLite), Flask-Login, bcrypt, and Tailwind CSS via CDN. Users can register, log in, and manage their own recipes. Only authenticated users can view recipes.

## Features

- Auth: Register, Login, Logout (Flask-Login + bcrypt)
- Recipes: Create, Read, Update, Delete (CRUD)
- Protected routes: Only logged-in users can access recipes
- Logging: Rotating file logger at `app.log` with an admin-only logs view
- Tailwind CSS via CDN for quick styling
- SQLite via Flask-SQLAlchemy

## Requirements

- Python 3.10+
- (Optional but recommended) A virtual environment

## Quick start (Windows PowerShell)

```powershell
# 1) Create & activate venv (optional but recommended)
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

# 2) Install Python dependencies
pip install -r requirements.txt

# 3) Initialize the database
python init_db.py

# 4) Run the app
python run.py
```

Open http://127.0.0.1:5000/ in your browser.

## Docker deployment

To run the application in a Docker container:

```powershell
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The app will be available at http://localhost:5000/

**Docker notes:**

- Database persists in the `instance/` directory (volume mounted)
- Logs persist in `app.log` (volume mounted)
- Uses Gunicorn WSGI server for production
- Set `SECRET_KEY` environment variable in `.env` file or docker-compose.yml

## Admin access for logs

- By default, new users are not admins. To view `/logs`, manually set a user's `is_admin` to `true` in the SQLite database using a DB browser or Python shell.

## Project structure

```
app/
  __init__.py           # App factory, logging, blueprint registration
  extensions.py         # LoginManager, SQLAlchemy db instance, User session
  models.py             # User and Recipe SQLAlchemy models
  blueprints/
    auth/               # Register/Login/Logout
    recipes/            # CRUD endpoints for recipes (protected)
    logs/               # Admin-only logs view
  templates/
    base.html           # Tailwind CDN, nav, flash messages
    auth/               # login/register views
    recipes/            # index/new/show/edit views
    logs/               # logs view
  static/               # (optional assets)
init_db.py              # Database initialization script
run.py                  # Dev entrypoint
requirements.txt
README.md
```

## Notes

- Replace the Flask `SECRET_KEY` with a secure value in production (e.g., via environment variable).
- Tailwind is used via CDN for simplicity. For production, consider a proper Tailwind build pipeline.
- The SQLite database file is created at `instance/app.db` by Flask-SQLAlchemy.
