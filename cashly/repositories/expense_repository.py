from typing import Optional

from cashly.database.db import get_db


def get_by_id_and_user(expense_id: int, user_id: int):
    return get_db().execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id),
    ).fetchone()


def list_expenses(
    user_id: int,
    *,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    month: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple:
    where = ["e.user_id = ?"]
    params: list = [user_id]

    if category_id:
        where.append("e.category_id = ?")
        params.append(category_id)
    if search:
        where.append("e.description LIKE ?")
        params.append(f"%{search}%")
    if month:
        where.append("strftime('%Y-%m', e.expense_date) = ?")
        params.append(month)

    clause = " AND ".join(where)
    db = get_db()
    total = db.execute(
        f"SELECT COUNT(*) FROM expenses e WHERE {clause}", params
    ).fetchone()[0]
    rows = db.execute(
        f"""SELECT e.*, c.name AS category_name, c.icon AS category_icon, c.color AS category_color
            FROM expenses e
            JOIN categories c ON c.id = e.category_id
            WHERE {clause}
            ORDER BY e.expense_date DESC, e.id DESC
            LIMIT ? OFFSET ?""",
        [*params, per_page, (page - 1) * per_page],
    ).fetchall()
    return [dict(r) for r in rows], total


def create(user_id: int, data: dict) -> int:
    db = get_db()
    cur = db.execute(
        """INSERT INTO expenses (user_id, category_id, amount, currency, description, note, expense_date)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            data["category_id"],
            data["amount"],
            data.get("currency", "BDT"),
            data["description"],
            data.get("note") or None,
            data["expense_date"],
        ),
    )
    db.commit()
    return cur.lastrowid


def update(expense_id: int, user_id: int, data: dict) -> None:
    db = get_db()
    db.execute(
        """UPDATE expenses SET category_id=?, amount=?, currency=?, description=?,
           note=?, expense_date=?, updated_at=datetime('now')
           WHERE id=? AND user_id=?""",
        (
            data["category_id"],
            data["amount"],
            data.get("currency", "BDT"),
            data["description"],
            data.get("note") or None,
            data["expense_date"],
            expense_id,
            user_id,
        ),
    )
    db.commit()


def delete(expense_id: int, user_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    db.commit()


def sum_for_period(user_id: int, category_id: int, period: str) -> float:
    db = get_db()
    if period == "monthly":
        date_filter = "strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')"
    elif period == "weekly":
        date_filter = "strftime('%W-%Y', expense_date) = strftime('%W-%Y', 'now')"
    else:
        date_filter = "strftime('%Y', expense_date) = strftime('%Y', 'now')"

    result = db.execute(
        f"""SELECT COALESCE(SUM(amount), 0) FROM expenses
            WHERE user_id=? AND category_id=? AND {date_filter}""",
        (user_id, category_id),
    ).fetchone()[0]
    return float(result)
