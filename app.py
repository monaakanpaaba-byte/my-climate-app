# app.py — Flask app using Supabase (Postgres) as the database
# This version works on Vercel, since Vercel's filesystem is read-only
# and can't store a local SQLite file.

from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client
import os

app = Flask(__name__)

# These must be set as Environment Variables in your Vercel project settings:
#   SUPABASE_URL      → e.g. https://xxxx.supabase.co
#   SUPABASE_ANON_KEY → your project's anon/public API key
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")


def get_db():
    """
    Returns a Supabase client.
    NOTE: unlike sqlite3, this is NOT a context manager —
    never use "with get_db() as conn:" with it.
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/", methods=["GET"])
def index():
    """
    GET /  — Home page.
    Fetches all readings from the Supabase 'readings' table,
    newest first, and passes them to the template.
    """
    db = get_db()

    response = (
        db.table("readings")
        .select("*")
        .order("date", desc=True)
        .execute()
    )

    readings_list = response.data

    return render_template(
        "index.html",
        readings=readings_list,
        readings_json=readings_list
    )


@app.route("/submit", methods=["POST"])
def submit():
    """
    POST /submit — Saves a new reading to Supabase, then redirects back to GET /.
    """
    city        = request.form.get("city", "").strip()
    temperature = request.form.get("temperature", "").strip()
    date        = request.form.get("date", "").strip()

    if not city or not temperature or not date:
        return redirect(url_for("index"))

    db = get_db()

    db.table("readings").insert({
        "city": city,
        "temperature": float(temperature),
        "date": date
    }).execute()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
