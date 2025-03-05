from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def dict_converter(languages: list, current_language: str) -> dict:
    translation = {}
    for i in languages:
        if current_language == 'en':
            translation.update({i.code : i.eng})
        elif current_language == 'ru':
            translation.update({i.code : i.rus})
        elif current_language == 'uz':
            translation.update({i.code : i.uzb})
    return translation