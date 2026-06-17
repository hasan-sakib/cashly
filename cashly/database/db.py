import os
import sqlite3

from flask import g, current_app

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT    NOT NULL UNIQUE,
    username      TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    is_active     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    name       TEXT    NOT NULL,
    icon       TEXT    NOT NULL DEFAULT '📦',
    color      TEXT    NOT NULL DEFAULT '#1a472a',
    is_default INTEGER NOT NULL DEFAULT 0,
    created_at TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, name)
);
CREATE INDEX IF NOT EXISTS idx_categories_user ON categories(user_id);

CREATE TABLE IF NOT EXISTS expenses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    category_id  INTEGER NOT NULL,
    amount       REAL    NOT NULL CHECK(amount > 0),
    currency     TEXT    NOT NULL DEFAULT 'BDT',
    description  TEXT    NOT NULL,
    note         TEXT,
    expense_date TEXT    NOT NULL,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at   TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_expenses_user      ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date      ON expenses(expense_date);
CREATE INDEX IF NOT EXISTS idx_expenses_category  ON expenses(category_id);
CREATE INDEX IF NOT EXISTS idx_expenses_user_date ON expenses(user_id, expense_date);

CREATE TABLE IF NOT EXISTS budgets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    category_id INTEGER,
    amount      REAL    NOT NULL CHECK(amount > 0),
    period      TEXT    NOT NULL CHECK(period IN ('monthly', 'weekly', 'yearly')),
    start_date  TEXT    NOT NULL,
    end_date    TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    UNIQUE (user_id, category_id, period)
);

CREATE TABLE IF NOT EXISTS user_settings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL UNIQUE,
    currency      TEXT    NOT NULL DEFAULT 'BDT',
    theme         TEXT    NOT NULL DEFAULT 'light'
                          CHECK(theme IN ('light', 'dark', 'system')),
    date_format   TEXT    NOT NULL DEFAULT 'YYYY-MM-DD',
    notifications INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

_DEFAULT_CATEGORIES = [
    ("Food",          "🍽️",  "#e67e22"),
    ("Transport",     "🚗",  "#3498db"),
    ("Shopping",      "🛍️",  "#9b59b6"),
    ("Bills",         "📄",  "#e74c3c"),
    ("Entertainment", "🎬",  "#1abc9c"),
    ("Health",        "💊",  "#2ecc71"),
    ("Education",     "📚",  "#f39c12"),
    ("Other",         "📦",  "#1a472a"),
]


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        path = current_app.config["DATABASE_PATH"]
        use_uri = path.startswith("file:")
        g.db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES, uri=use_uri)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    path = current_app.config["DATABASE_PATH"]
    if not path.startswith("file:") and path != ":memory:":
        os.makedirs(os.path.dirname(path), exist_ok=True)
    db = get_db()
    db.executescript(SCHEMA_SQL)


def seed_db() -> None:
    db = get_db()
    if db.execute("SELECT COUNT(*) FROM categories WHERE user_id IS NULL").fetchone()[0] > 0:
        return
    db.executemany(
        "INSERT INTO categories (user_id, name, icon, color, is_default) VALUES (NULL, ?, ?, ?, 1)",
        _DEFAULT_CATEGORIES,
    )
    db.commit()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)

    path = app.config["DATABASE_PATH"]
    if path.startswith("file:") and "memory" in path:
        # Keep a persistent connection so the shared in-memory DB survives context teardowns
        app._keep_alive_conn = sqlite3.connect(path, uri=True)

    with app.app_context():
        init_db()
        seed_db()
