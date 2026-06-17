from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from cashly.blueprints.profile import profile_bp
from cashly.blueprints.profile.forms import ProfileForm
from cashly.database.db import get_db
from cashly.repositories import user_repository


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    db       = get_db()
    settings = db.execute(
        "SELECT * FROM user_settings WHERE user_id = ?", (current_user.id,)
    ).fetchone()

    form = ProfileForm()
    if form.validate_on_submit():
        existing = user_repository.get_by_username(form.username.data)
        if existing and existing["id"] != current_user.id:
            flash("Username is already taken.", "error")
        else:
            user_repository.update_username(current_user.id, form.username.data)
            db.execute(
                "UPDATE user_settings SET currency=?, theme=?, updated_at=datetime('now') WHERE user_id=?",
                (form.currency.data, form.theme.data, current_user.id),
            )
            db.commit()
            flash("Profile updated.", "success")
            return redirect(url_for("profile.index"))

    if request.method == "GET":
        form.username.data = current_user.username
        if settings:
            form.currency.data = settings["currency"]
            form.theme.data    = settings["theme"]

    return render_template("profile/index.html", form=form, settings=settings)
