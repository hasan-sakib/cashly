from cashly.database.db import get_db


def get_by_id(user_id: int):
    return get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def get_by_email(email: str):
    return get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


def get_by_username(username: str):
    return get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def create(username: str, email: str, password_hash: str) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    db.commit()
    return cur.lastrowid


def update_username(user_id: int, username: str) -> None:
    db = get_db()
    db.execute(
        "UPDATE users SET username = ?, updated_at = datetime('now') WHERE id = ?",
        (username, user_id),
    )
    db.commit()
