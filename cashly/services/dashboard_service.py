from cashly.database.db import get_db


def get_dashboard_data(user_id: int, month: str) -> dict:
    db = get_db()
    return {
        "monthly_total":      _monthly_total(db, user_id, month),
        "category_breakdown": _category_breakdown(db, user_id, month),
        "recent_expenses":    _recent_expenses(db, user_id),
        "daily_trend":        _daily_trend(db, user_id, month),
        "month_vs_last":      _month_vs_last(db, user_id, month),
    }


def _monthly_total(db, user_id: int, month: str) -> float:
    result = db.execute(
        """SELECT COALESCE(SUM(amount), 0) FROM expenses
           WHERE user_id=? AND strftime('%Y-%m', expense_date)=?""",
        (user_id, month),
    ).fetchone()[0]
    return float(result)


def _category_breakdown(db, user_id: int, month: str) -> list:
    rows = db.execute(
        """SELECT c.name, c.icon, c.color, SUM(e.amount) AS total, COUNT(*) AS count
           FROM expenses e
           JOIN categories c ON c.id = e.category_id
           WHERE e.user_id=? AND strftime('%Y-%m', e.expense_date)=?
           GROUP BY e.category_id ORDER BY total DESC""",
        (user_id, month),
    ).fetchall()
    return [dict(r) for r in rows]


def _recent_expenses(db, user_id: int, limit: int = 5) -> list:
    rows = db.execute(
        """SELECT e.*, c.name AS category_name, c.icon AS category_icon, c.color AS category_color
           FROM expenses e
           JOIN categories c ON c.id = e.category_id
           WHERE e.user_id=?
           ORDER BY e.expense_date DESC, e.id DESC LIMIT ?""",
        (user_id, limit),
    ).fetchall()
    return [dict(r) for r in rows]


def _daily_trend(db, user_id: int, month: str) -> list:
    rows = db.execute(
        """SELECT strftime('%d', expense_date) AS day, SUM(amount) AS total
           FROM expenses WHERE user_id=? AND strftime('%Y-%m', expense_date)=?
           GROUP BY day ORDER BY day""",
        (user_id, month),
    ).fetchall()
    return [dict(r) for r in rows]


def _month_vs_last(db, user_id: int, month: str) -> dict:
    year, m = int(month[:4]), int(month[5:])
    prev = f"{year - 1}-12" if m == 1 else f"{year}-{m - 1:02d}"

    current = float(db.execute(
        """SELECT COALESCE(SUM(amount), 0) FROM expenses
           WHERE user_id=? AND strftime('%Y-%m', expense_date)=?""",
        (user_id, month),
    ).fetchone()[0])
    last = float(db.execute(
        """SELECT COALESCE(SUM(amount), 0) FROM expenses
           WHERE user_id=? AND strftime('%Y-%m', expense_date)=?""",
        (user_id, prev),
    ).fetchone()[0])

    diff = current - last
    pct = (diff / last * 100) if last else None
    return {"current": current, "last": last, "diff": diff, "pct": pct, "prev_month": prev}
