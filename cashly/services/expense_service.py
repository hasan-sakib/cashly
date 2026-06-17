from flask import abort, flash

from cashly.repositories import budget_repository, expense_repository


def list_expenses(user_id: int, **kwargs) -> tuple:
    return expense_repository.list_expenses(user_id, **kwargs)


def add_expense(user_id: int, data: dict) -> int:
    expense_id = expense_repository.create(user_id, data)
    _check_budget(user_id, data["category_id"])
    return expense_id


def get_or_404(expense_id: int, user_id: int) -> dict:
    row = expense_repository.get_by_id_and_user(expense_id, user_id)
    if not row:
        abort(404)
    return dict(row)


def update_expense(expense_id: int, user_id: int, data: dict) -> None:
    expense_repository.update(expense_id, user_id, data)
    _check_budget(user_id, data["category_id"])


def delete_expense(expense_id: int, user_id: int) -> None:
    expense_repository.delete(expense_id, user_id)


def _check_budget(user_id: int, category_id: int) -> None:
    budget = budget_repository.get_active(user_id, category_id)
    if not budget:
        return
    spent = expense_repository.sum_for_period(user_id, category_id, budget["period"])
    if spent >= budget["amount"] * 0.9:
        flash("You've used 90%+ of your budget for this category.", "warning")
