from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, validators, IntegerField, SelectField

class ProductForm(FlaskForm):
    title_eng = StringField("English title:", [validators.DataRequired(), validators.Length(min=4)])
    title_uzb = StringField("Uzbek title:", [validators.DataRequired(), validators.Length(min=4)])
    title_rus = StringField("Russian title:", [validators.DataRequired(), validators.Length(min=4)])
    description_eng = StringField("English description:", [validators.DataRequired(), validators.Length(min=4)])
    description_uzb = StringField("Uzbek description:", [validators.DataRequired(), validators.Length(min=4)])
    description_rus = StringField("Russian description:", [validators.DataRequired(), validators.Length(min=4)])
    typee = SelectField('Type:', choices=[('puff','puff'),('popcorn','popcorn')], validators=[validators.DataRequired()])
    price = IntegerField("Price: ", [validators.DataRequired()])
    gramm = IntegerField("Gramms:", [validators.DataRequired()])
    image_path = FileField("Product image:", [validators.DataRequired()])
    submit = SubmitField("Submit")