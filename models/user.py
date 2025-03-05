from datetime import datetime
from models import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id: int):
    return User.query.filter_by(id = user_id, is_deleted = False).first()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key = True)
    full_name = db.Column(db.String(), nullable = False)
    username = db.Column(db.String(), nullable = False)
    password = db.Column(db.String(), nullable = False)
    language = db.Column(db.String(), nullable = False)
    is_deleted = db.Column(db.Boolean(), default = False)
    created_at = db.Column(db.DateTime(), default = datetime.now)

    def __init__(self, full_name: str, username: str, password: str, language: str):
        super().__init__()
        self.full_name = full_name
        self.username = username
        self.password = password
        self.language = language
