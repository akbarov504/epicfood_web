from app import app
from flask import render_template, redirect, url_for, request
from models.language import Language
from models import dict_converter, db
from flask_login import current_user, login_required
from models.product import Product
from forms.product_form import ProductForm
from werkzeug.utils import secure_filename
import os

@app.route('/admin-products', methods = ['GET', 'POST'])
@login_required
def admin_products():
    if request.method == 'GET':
        admin = Language.query.filter_by(file_name = 'admin').all()
        product_translation = Language.query.filter_by(file_name = 'product').all()
        translations = dict_converter(admin+product_translation, current_user.language)
        products = Product.query.filter_by(is_deleted = False).all()
        return render_template('product/list.html', translation = translations, products = products, current_language = current_user.language)
    elif request.method == 'POST' and 'delete' in request.form:
        product = Product.query.filter_by(id = request.form.get('delete')).first()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin_products'))
    
@app.route('/product-create', methods = ["GET", "POST"])
@login_required
def product_create():
    p_form = ProductForm()
    if request.method == 'GET':
        product_translation = Language.query.filter_by(file_name = 'product').all()
        translation = dict_converter(product_translation, current_user.language)
        return render_template('product/create.html', form = p_form, translation = translation)
    elif p_form.validate_on_submit():
        title_eng = p_form.title_eng.data
        title_uzb = p_form.title_uzb.data
        title_rus = p_form.title_rus.data
        description_eng = p_form.description_eng.data
        description_uzb = p_form.description_uzb.data
        description_rus = p_form.description_rus.data
        typee = p_form.typee.data
        price = p_form.price.data
        gramm = p_form.gramm.data
        
        image = p_form.image_path.data
        filename = secure_filename(image.filename)
        file_path = os.path.join(app.config["UPLOADS_FOLDER"], filename)
        image.save(file_path)

        product = Product(title_eng,  title_uzb, title_rus, description_eng, description_uzb, description_rus, typee, price, gramm, filename)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('admin_products'))

@app.route('/product-update/<product_id>', methods = ['GET', "POST"])
@login_required
def product_update(product_id: int):
    p_form = ProductForm()
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'GET':
        p_form.title_eng.data = product.title_eng
        p_form.title_uzb.data = product.title_uzb
        p_form.title_rus.data = product.title_rus
        p_form.description_eng.data = product.description_eng
        p_form.description_uzb.data = product.description_uzb
        p_form.description_rus.data = product.description_rus
        p_form.typee.data = product.typee
        p_form.price.data = product.price
        p_form.gramm.data = product.gramm

        product_translation = Language.query.filter_by(file_name = 'product').all()
        translation = dict_converter(product_translation, current_user.language)
        p_form.submit.label.text = translation.get(69)
        return render_template('product/update.html', translation = translation, form = p_form)
    elif p_form.validate_on_submit():
        product.title_eng = p_form.title_eng.data
        product.title_uzb = p_form.title_uzb.data
        product.title_rus = p_form.title_rus.data
        product.description_eng = p_form.description_eng.data
        product.description_uzb = p_form.description_uzb.data
        product.description_rus = p_form.description_rus.data
        product.typee = p_form.typee.data
        product.price = p_form.price.data
        product.gramm = p_form.gramm.data
        
        image = p_form.image_path.data
        filename = secure_filename(image.filename)
        file_path = os.path.join(app.config["UPLOADS_FOLDER"], filename)
        image.save(file_path)
        
        product.image_path = filename

        db.session.commit()
        return redirect(url_for('admin_products'))