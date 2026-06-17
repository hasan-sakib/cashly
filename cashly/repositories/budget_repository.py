from typing import Optional

from cashly.database.db import get_db


def get_active(user_id: int, category_id: Optional[int]) -> Optional[dict]:
    db = get_db()
    row = db.execute(
        """SELECT * FROM budgets
           WHERE user_id=? AND category_id IS ?
             AND start_date <= date('now')
             AND (end_date IS NULL OR end_date >= date('now'))""",
        (user_id, category_id),
    ).fetchone()
    return dict(row) if row else None
