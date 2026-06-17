from datetime import date

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from cashly.blueprints.expenses import expenses_bp
from cashly.blueprints.expenses.forms import ExpenseForm
from cashly.repositories import category_repository
from cashly.services import expense_service


def _load_categories(form):
    cats = category_repository.list_for_user(current_user.id)
    form.category_id.choices = [(c["id"], f"{c['icon']} {c['name']}") for c in cats]


@expenses_bp.get("/")
@login_required
def index():
    page     = request.args.get("page", 1, type=int)
    search   = request.args.get("q", "")
    month    = request.args.get("month", "")
    category = request.args.get("category", None, type=int)

    expenses, total = expense_service.list_expenses(
        current_user.id,
        search=search or None,
        month=month or None,
        category_id=category,
        page=page,
    )
    categories = category_repository.list_for_user(current_user.id)
    return render_template(
        "expenses/index.html",
        expenses=expenses, total=total,
        page=page, per_page=20,
        search=search, month=month, category=category,
        categories=categories,
    )


@expenses_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = ExpenseForm()
    _load_categories(form)
    if form.validate_on_submit():
        expense_service.add_expense(current_user.id, {
            "category_id":  form.category_id.data,
            "amount":       float(form.amount.data),
            "currency":     form.currency.data,
            "description":  form.description.data,
            "note":         form.note.data,
            "expense_date": form.expense_date.data.isoformat(),
        })
        flash("Expense added.", "success")
        return redirect(url_for("expenses.index"))
    if request.method == "GET":
        form.expense_date.data = date.today()
    return render_template("expenses/form.html", form=form, action="Add")


@expenses_bp.route("/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit(expense_id: int):
    expense = expense_service.get_or_404(expense_id, current_user.id)
    form = ExpenseForm()
    _load_categories(form)
    if form.validate_on_submit():
        expense_service.update_expense(expense_id, current_user.id, {
            "category_id":  form.category_id.data,
            "amount":       float(form.amount.data),
            "currency":     form.currency.data,
            "description":  form.description.data,
            "note":         form.note.data,
            "expense_date": form.expense_date.data.isoformat(),
        })
        flash("Expense updated.", "success")
        return redirect(url_for("expenses.index"))
    if request.method == "GET":
        form.category_id.data  = expense["category_id"]
        form.amount.data       = expense["amount"]
        form.currency.data     = expense["currency"]
        form.description.data  = expense["description"]
        form.note.data         = expense["note"]
        form.expense_date.data = date.fromisoformat(expense["expense_date"])
    return render_template("expenses/form.html", form=form, action="Edit", expense=expense)


@expenses_bp.post("/<int:expense_id>/delete")
@login_required
def delete(expense_id: int):
    expense_service.get_or_404(expense_id, current_user.id)
    expense_service.delete_expense(expense_id, current_user.id)
    flash("Expense deleted.", "info")
    return redirect(url_for("expenses.index"))
