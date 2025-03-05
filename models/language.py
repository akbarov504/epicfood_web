from models import db
from datetime import datetime

class Language(db.Model):
    __tablename__ = 'language'

    code = db.Column(db.Integer(), primary_key = True)
    eng = db.Column(db.String(), nullable = False)
    uzb = db.Column(db.String(), nullable = False)
    rus = db.Column(db.String(), nullable = False)
    file_name = db.Column(db.String(), nullable = False)

    def __init__(self, eng: str, uzb: str, rus: str, file_name: str):
        super().__init__()
        self.eng = eng
        self.uzb = uzb
        self.rus = rus
        self.file_name = file_name