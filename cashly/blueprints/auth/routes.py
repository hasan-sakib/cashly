from flask import render_template

from cashly.blueprints.auth import auth_bp


@auth_bp.get("/")
def landing():
    return render_template("landing.html")


@auth_bp.get("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.get("/register")
def register():
    return render_template("auth/register.html")


@auth_bp.get("/logout")
def logout():
    return "Logout — coming in Phase 2"
