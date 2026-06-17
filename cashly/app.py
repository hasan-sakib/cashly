import os

from flask import Flask

from cashly.config import config_map


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    from cashly.extensions import login_manager, csrf, limiter
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    from cashly.database.db import init_app as db_init_app
    db_init_app(app)

    from cashly.services import auth_service

    @login_manager.user_loader
    def load_user(user_id: str):
        return auth_service.get_user_by_id(int(user_id))

    from cashly.blueprints.auth import auth_bp
    from cashly.blueprints.expenses import expenses_bp
    from cashly.blueprints.dashboard import dashboard_bp
    from cashly.blueprints.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp, url_prefix="/expenses")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp, url_prefix="/profile")

    from cashly.errors import register_error_handlers
    register_error_handlers(app)

    return app
