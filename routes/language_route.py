from flask import render_template, redirect, url_for, request
from app import app
from flask_login import login_required, current_user
from models.language import Language
from forms.language_form import LanguageCreate
from models import db, dict_converter

@app.route('/admin-language', methods = ['GET', 'POST'])
@login_required
def admin_language():
    if request.method == 'GET':
        admin = Language.query.filter_by(file_name = 'admin').all()
        language_translation = Language.query.filter_by(file_name = 'language').all()
        translation = dict_converter(admin+language_translation, current_user.language)
        languages = Language.query.order_by(Language.code).all()
        return render_template('language/list.html', translation = translation, languages = languages)
    elif request.method == 'POST' and 'delete' in request.form:
        language = Language.query.filter_by(code = request.form.get('delete')).first()
        db.session.delete(language)
        db.session.commit()
        return redirect(url_for('admin_language'))
    
@app.route('/language-create', methods = ['GET', 'POST'])
@login_required
def language_create():
    form = LanguageCreate()
    if request.method == 'GET':
        admin = Language.query.filter_by(file_name = 'admin').all()
        language_translation = Language.query.filter_by(file_name = 'language').all()
        translation = dict_converter(admin+language_translation, current_user.language)
        form.submit.label.text = translation.get(26)
        return render_template("language/create.html", form=form, translation = translation)
    elif form.validate_on_submit():
        eng = form.eng.data
        uzb = form.uzb.data
        rus = form.rus.data
        file_name = form.file_name.data
        row = Language(eng, uzb, rus, file_name)
        db.session.add(row)    
        db.session.commit()
        return redirect(url_for('admin_language'))

@app.route('/language-update/<language_id>', methods = ['GET', 'POST'])
@login_required
def language_update(language_id: int):
    form = LanguageCreate() #i know why Create instead of update
    language = Language.query.filter_by(code = language_id).first()
    if request.method == 'GET':
        form.eng.data = language.eng
        form.uzb.data = language.uzb
        form.rus.data = language.rus
        form.file_name.data = language.file_name

        admin = Language.query.filter_by(file_name = 'admin').all()
        language_translation = Language.query.filter_by(file_name = 'language').all()
        translation = dict_converter(admin+language_translation, current_user.language)
        form.submit.label.text = translation.get(26)
        
        return render_template('language/update.html', form = form, translation = translation)
    elif form.validate_on_submit():
        language.eng = form.eng.data
        language.uzb = form.uzb.data
        language.rus = form.rus.data
        language.file_name = form.file_name.data
        db.session.commit()
        return redirect(url_for('admin_language'))