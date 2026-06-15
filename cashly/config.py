import os
from datetime import timedelta

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig:
    SECRET_KEY                 = os.environ.get("SECRET_KEY", "dev-only-insecure-key")
    SESSION_COOKIE_HTTPONLY    = True
    SESSION_COOKIE_SAMESITE    = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    DATABASE_PATH              = os.path.join(_project_root, "instance", "cashly.db")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING       = True
    DATABASE_PATH = ":memory:"


class ProductionConfig(BaseConfig):
    DEBUG                 = False
    SESSION_COOKIE_SECURE = True


config_map = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
}
