from flask import render_template

from cashly.blueprints.profile import profile_bp


@profile_bp.get("/")
def index():
    return "Profile — coming in Phase 2"
