# app.py
from flask import Flask, request, render_template, redirect, url_for
from supabase import create_client
import os

app = Flask(__name__)

# Read credentials from environment variables set in Vercel dashboard
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

def get_db():
    # Returns a Supabase client — NOT a context manager, so no "with" statement
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/", methods=["GET"])
def index():
    db = get_db()

    # Fetch all readings, newest first
    response = db.table("readings").select("*").order("date", desc=True).execute()

    # response.data is a plain list of dicts — ready for Jinja2 and tojson
    readings_list = response.data

    return render_template(
        "index.html",
        readings=readings_list,
        readings_json=readings_list
    )


@app.route("/submit", methods=["POST"])
def submit():
    city        = request.form.get("city", "").strip()
    temperature = request.form.get("temperature", "").strip()
    date        = request.form.get("date", "").strip()

    if not city or not temperature or not date:
        return redirect(url_for("index"))

    db = get_db()

    # Insert a new row — pass a dict matching your Supabase table columns
    db.table("readings").insert({
        "city": city,
        "temperature": float(temperature),
        "date": date
    }).execute()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
    