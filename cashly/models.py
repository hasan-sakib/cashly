from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, row) -> None:
        self.id       = row["id"]
        self.email    = row["email"]
        self.username = row["username"]
        self._active  = bool(row["is_active"])

    @property
    def is_active(self) -> bool:
        return self._active
