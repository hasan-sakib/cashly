from cashly.database.db import get_db


def list_for_user(user_id: int) -> list:
    return get_db().execute(
        """SELECT * FROM categories
           WHERE user_id IS NULL OR user_id = ?
           ORDER BY is_default DESC, name""",
        (user_id,),
    ).fetchall()


def create(user_id: int, name: str, icon: str = "📦", color: str = "#1a472a") -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO categories (user_id, name, icon, color) VALUES (?, ?, ?, ?)",
        (user_id, name, icon, color),
    )
    db.commit()
    return cur.lastrowid
