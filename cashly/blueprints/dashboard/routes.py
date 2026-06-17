from datetime import date

from flask import render_template, request
from flask_login import current_user, login_required

from cashly.blueprints.dashboard import dashboard_bp
from cashly.services import dashboard_service


@dashboard_bp.get("/dashboard")
@login_required
def index():
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    data  = dashboard_service.get_dashboard_data(current_user.id, month)
    return render_template("dashboard/index.html", month=month, **data)
