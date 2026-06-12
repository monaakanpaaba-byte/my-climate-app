# app.py
from flask import Flask, request, render_template, redirect, url_for
import sqlite3

import os

def init_db():
    try:
        # Get the directory where app.py is located
        app_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(app_dir, "schema.sql")
        
        with get_db() as conn:
            with open(schema_path, "r") as f:
                conn.executescript(f.read())
                conn.commit()
                print("✓ Database initialized successfully!")
    except FileNotFoundError:
        print(f"✗ Error: schema.sql not found at {schema_path}")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
app = Flask(__name__)
DATABASE = "climate.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    with get_db() as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())

@app.route("/", methods=["GET"])
def index():
    with get_db() as conn:
        # fetchall() returns sqlite3.Row objects
        rows = conn.execute("").fetchall()

    # Convert each Row to a plain dict so Jinja2's tojson can serialize it cleanly.
    # sqlite3.Row objects cannot be JSON-serialized directly — dicts can.
    readings_list = [dict(row) for row in rows]

    return render_template(
        "index.html",
        readings=readings_list,       # used by the Jinja2 {% for %} table loop
        readings_json=readings_list   # used by Chart.js via | tojson
    )

@app.route("/submit", methods=["POST"])
def submit():
    city        = request.form.get("city", "").strip()
    temperature = request.form.get("temperature", "").strip()
    date        = request.form.get("date", "").strip()

    if not city or not temperature or not date:
        return redirect(url_for("index"))

    with get_db() as conn:
        # Use ? placeholders — never string formatting — to prevent SQL injection
        conn.execute(
            "INSERT INTO readings (city, temperature, date) VALUES (?, ?, ?)",
            (city, float(temperature), date)
        )
        conn.commit()  # ← This saves the data to the database

    # Post/Redirect/Get pattern: redirect after POST to prevent duplicate submissions
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
