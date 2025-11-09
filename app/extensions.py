from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# SQLAlchemy instance
db = SQLAlchemy()


class UserSession(UserMixin):
    def __init__(self, id: int, email: str, name: str | None = None, is_admin: bool = False):
        self.id = id
        self.email = email
        self.name = name
        self.is_admin = is_admin

    def get_id(self) -> str:
        return str(self.id)
