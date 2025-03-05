from app import app
from flask import render_template, redirect, url_for, request
from models.language import Language
from models import dict_converter
from models.gift import Gift
from models.product import Product

current_language = ""

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home_page() -> render_template:
    global current_language
    if request.method == 'POST':
        if request.form.get('english_language'):
            current_language = "en"
        elif request.form.get("russian_language"):
            current_language = 'ru'
        elif request.form.get('uzbek_language'):
            current_language = 'uz'
    else:
        if current_language == "":
            current_language = "en"

    puff = Product.query.filter_by(typee = 'puff').all()
    puff = [puff[i:i+2] for i in range(0, len(puff), 2)]

    popcorn = Product.query.filter_by(typee = 'popcorn').all()
    popcorn = [popcorn[i:i+2] for i in range(0, len(popcorn), 2)]

    gifts1 = Gift.query.all()
    gifts2 = [gifts1[i:i+2] for i in range(0, len(gifts1), 2)]
    gifts3 = [gifts1[i:i+3] for i in range(0, len(gifts1), 3)]

    translations = dict_converter(Language.query.filter_by(file_name = 'home').all(), current_language)


    return render_template("index.html", current_language = current_language, translations = translations, range = range, puffs = puff, popcorns = popcorn, gifts1 = gifts1, gifts2 = gifts2, gifts3 = gifts3)