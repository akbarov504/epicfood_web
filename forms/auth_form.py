from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, validators, SelectField

class LoginForm(FlaskForm):
    username = StringField('Foydalanuvchi nomi', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Parol', [validators.DataRequired(), validators.Length(min=8, max=30)])
    submit = SubmitField('Login')

class UserCreate(FlaskForm):
    full_name = StringField('Full Name', [validators.DataRequired(), validators.Length(min=4, max=50)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=30)])
    language = SelectField("Language", choices = [("en", "English"), ("uz", "Uzbek"), ("ru", "Russian")])
    submit = SubmitField("Submit")

class UserUpdate(FlaskForm):
    full_name = StringField('Full Name', [validators.DataRequired(), validators.Length(min=4, max=50)])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=30)])
    language = SelectField("Language", choices = [("en", "English"), ("uz", "Uzbek"), ("ru", "Russian")])
    submit = SubmitField("Submit")
    