from models import db
from datetime import datetime

class Gift(db.Model):
    __tablename__ = 'gift'

    id = db.Column(db.Integer(), primary_key = True)
    title_eng = db.Column(db.String(), nullable = False)
    title_uzb = db.Column(db.String(), nullable = False)
    title_rus = db.Column(db.String(), nullable = False)
    description_eng = db.Column(db.String(), nullable = False)
    description_uzb = db.Column(db.String(), nullable = False)
    description_rus = db.Column(db.String(), nullable = False)
    image_path = db.Column(db.String(), nullable = False)
    is_deleted = db.Column(db.Boolean(), default = False)
    created_at = db.Column(db.DateTime(), default = datetime.now)

    def __init__(self, title_eng: str, title_uzb: str, title_rus: str, description_eng: str, description_uzb: str, description_rus: str, image_path: str):
        super().__init__()
        self.title_eng = title_eng
        self.title_uzb = title_uzb
        self.title_rus = title_rus
        self.description_eng = description_eng
        self.description_uzb = description_uzb
        self.description_rus = description_rus
        self.image_path = image_path