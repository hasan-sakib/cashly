from flask import render_template

from cashly.blueprints.dashboard import dashboard_bp


@dashboard_bp.get("/dashboard")
def index():
    return "Dashboard — coming in Phase 2"
