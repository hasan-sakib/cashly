from werkzeug.security import check_password_hash, generate_password_hash

from cashly.database.db import get_db
from cashly.models import User
from cashly.repositories import user_repository


def register_user(username: str, email: str, password: str) -> int:
    password_hash = generate_password_hash(password)
    user_id = user_repository.create(username, email, password_hash)
    db = get_db()
    db.execute("INSERT INTO user_settings (user_id) VALUES (?)", (user_id,))
    db.commit()
    return user_id


def authenticate(email: str, password: str):
    row = user_repository.get_by_email(email)
    if row and check_password_hash(row["password_hash"], password):
        return User(row)
    return None


def get_user_by_id(user_id: int):
    row = user_repository.get_by_id(user_id)
    return User(row) if row else None
