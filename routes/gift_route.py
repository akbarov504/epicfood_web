from app import app
from flask import render_template, redirect, url_for, request
from models.gift import Gift
from models.language import Language
from models.gift import Gift
from models import db, dict_converter
from flask_login import current_user, login_required
from forms.gifts_form import GiftForm
from werkzeug.utils import secure_filename
import os

@app.route('/admin-gifts', methods = ['GET', 'POST'])
@login_required
def admin_gifts():
    if request.method == 'GET':
        admin = Language.query.filter_by(file_name = 'admin').all()
        product_translation = Language.query.filter_by(file_name = 'product').all()
        translations = dict_converter(admin+product_translation, current_user.language)
        gifts = Gift.query.filter_by(is_deleted = False).all()
        return render_template('gifts/list.html', translation = translations, gifts = gifts, current_language = current_user.language)
    elif request.method == 'POST' and 'delete' in request.form:
        gift = Gift.query.filter_by(id = request.form.get('delete')).first()
        db.session.delete(gift)
        db.session.commit()
        return redirect(url_for('admin_gifts'))

@app.route('/gift-create', methods = ['GET', 'POST'])
@login_required
def gift_create():
    g_form = GiftForm()
    if request.method == 'GET':
        gift_translation = Language.query.filter_by(file_name = 'product').all() #I know why file_name is product
        translation = dict_converter(gift_translation, current_user.language)
        return render_template('gifts/create.html', translation = translation, form = g_form)
    elif g_form.validate_on_submit():
        title_eng = g_form.title_eng.data
        title_uzb = g_form.title_uzb.data
        title_rus = g_form.title_rus.data
        description_eng = g_form.description_eng.data
        description_uzb = g_form.description_uzb.data
        description_rus = g_form.description_rus.data

        image = g_form.image_path.data
        filename = secure_filename(image.filename)
        file_path = os.path.join(app.config["UPLOADS_FOLDER"], filename)
        image.save(file_path)

        gift = Gift(title_eng, title_uzb, title_rus, description_eng, description_uzb, description_rus, filename)
        db.session.add(gift)
        db.session.commit()

        return redirect(url_for('admin_gifts'))
    
@app.route('/gift-update/<gift_id>', methods = ['GET', 'POST'])
@login_required
def gift_update(gift_id: int):
    g_form = GiftForm()
    gift = Gift.query.filter_by(id = gift_id).first()
    if request.method == 'GET':
        g_form.title_eng.data = gift.title_eng
        g_form.title_uzb.data = gift.title_uzb
        g_form.title_rus.data = gift.title_rus
        g_form.description_eng.data = gift.description_eng
        g_form.description_uzb.data = gift.description_uzb
        g_form.description_rus.data = gift.description_rus

        product_translation = Language.query.filter_by(file_name = 'product').all() # i know why file_name is product
        translation = dict_converter(product_translation, current_user.language)
        g_form.submit.label.text = translation.get(69)
        return render_template('gifts/update.html', translation = translation, form = g_form)
    elif g_form.validate_on_submit():
        gift.title_eng = g_form.title_eng.data
        gift.title_uzb = g_form.title_uzb.data
        gift.title_rus = g_form.title_rus.data
        gift.description_eng = g_form.description_eng.data
        gift.description_uzb = g_form.description_uzb.data
        gift.description_rus = g_form.description_rus.data

        image = g_form.image_path.data
        filename = secure_filename(image.filename)
        file_path = os.path.join(app.config["UPLOADS_FOLDER"], filename)
        image.save(file_path)

        gift.image_path = filename

        db.session.commit()
        return redirect(url_for("admin_gifts"))