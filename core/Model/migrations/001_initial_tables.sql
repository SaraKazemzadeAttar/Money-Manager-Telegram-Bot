CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT,
    budget REAL DEFAULT 0,
    currency TEXT DEFAULT 'rial'
);

