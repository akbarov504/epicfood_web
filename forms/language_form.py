from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators, SelectField

class LanguageCreate(FlaskForm):
    eng = StringField('English', [validators.DataRequired()])
    uzb = StringField('Uzbek', [validators.DataRequired()])
    rus = StringField('Russian', [validators.DataRequired()])
    file_name = StringField('File name', [validators.DataRequired()])
    submit = SubmitField("Submit")