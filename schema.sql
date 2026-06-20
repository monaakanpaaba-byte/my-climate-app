-- schema.sql
-- This file defines the structure of our SQLite database.
-- Run this once to create the table before starting the Flask app.

-- CREATE TABLE IF NOT EXISTS means: only create the table if it doesn't already exist.
-- This is safe to run multiple times without errors.
CREATE TABLE IF NOT EXISTS readings (
    -- id: auto-incrementing primary key — SQLite assigns this automatically
    id        INTEGER PRIMARY KEY AUTOINCREMENT,

    -- city: the name of the city for this temperature reading
    city      TEXT    NOT NULL,

    -- temperature: stored as a real (decimal) number, e.g. 28.5
    temperature REAL  NOT NULL,

    -- date: stored as text in YYYY-MM-DD format (SQLite has no native DATE type)
    date      TEXT    NOT NULL
);
 def init_db():
    try:
        with get_db() as conn:
            with open("schema.sql", "r") as f:
                conn.executescript(f.read())
                print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")