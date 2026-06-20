-- schema.sql
-- Defines the structure of the SQLite database.
-- Run once to create the table before starting the Flask app.

CREATE TABLE IF NOT EXISTS readings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-incrementing ID
    city        TEXT    NOT NULL,                   -- name of the city
    temperature REAL    NOT NULL,                    -- decimal temperature, e.g. 28.5
    date        TEXT    NOT NULL                     -- stored as YYYY-MM-DD text
);
