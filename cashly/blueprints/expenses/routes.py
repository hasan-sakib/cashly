from flask import render_template

from cashly.blueprints.expenses import expenses_bp


@expenses_bp.get("/add")
def add():
    return "Add expense — coming in Phase 2"


@expenses_bp.route("/<int:expense_id>/edit", methods=["GET", "POST"])
def edit(expense_id: int):
    return f"Edit expense {expense_id} — coming in Phase 2"


@expenses_bp.post("/<int:expense_id>/delete")
def delete(expense_id: int):
    return f"Delete expense {expense_id} — coming in Phase 2"
