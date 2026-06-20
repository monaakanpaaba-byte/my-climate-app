# app.py — Main Flask application
# Flask maps URLs to Python functions ("routes").

from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client
import os

app = Flask(__name__)

# Use an absolute path so the database is always found, no matter
# where the app is run from.
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "climate.db")



SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

 
def get_db():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# def get_db():
#     """
#     Opens a SQLite connection.
#     row_factory = sqlite3.Row lets us access columns by name (row["city"])
#     instead of by index (row[0]).
#     """
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn


def init_db():
    """Creates the readings table from schema.sql if it doesn't exist yet."""
    db = get_db()
    response = db.table("readings").select("*").order("date", desc=True).execute()
    readings_list = response.data


@app.route("/", methods=["GET"])
def index():
    """
    GET /  — Home page.
    Fetches all readings and passes them to the template:
      - readings       → used by Jinja2 {% for %} to build the HTML table
      - readings_json   → same data, but converted to plain dicts so it can
                          be safely turned into JSON for Chart.js
    """
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY date DESC"
        ).fetchall()

    # sqlite3.Row objects can't be JSON-serialized directly — convert to dicts
    readings_list = [dict(row) for row in rows]

    return render_template(
        "index.html",
        readings=readings_list,
        readings_json=readings_list
    )


@app.route("/submit", methods=["POST"])
def submit():
    """
    POST /submit — Saves a new reading, then redirects back to GET /.
    This Post/Redirect/Get pattern prevents duplicate submits on refresh.
    """
    city        = request.form.get("city", "").strip()
    temperature = request.form.get("temperature", "").strip()
    date        = request.form.get("date", "").strip()

    if not city or not temperature or not date:
        return redirect(url_for("index"))

    with get_db() as conn:
        # ? placeholders prevent SQL injection — never use string formatting here
        conn.execute(
            "INSERT INTO readings (city, temperature, date) VALUES (?, ?, ?)",
            (city, float(temperature), date)
        )

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()       # make sure the table exists before the first request
    app.run(debug=True)
