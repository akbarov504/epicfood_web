from app import app
from flask import render_template, redirect, url_for, request
from forms.auth_form import LoginForm, UserCreate, UserUpdate
from models.user import User
from flask_login import login_user, login_required, current_user, logout_user
from models.user import User
from models.language import Language
from models import db, dict_converter

@app.route("/admin", methods = ["GET", "POST"])
def admin_login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template("auth/login.html", login_form = login_form)
    elif login_form.submit.data and login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username = username, password = password, is_deleted = False).first()
        if user:
            login_user(user)
            return redirect(url_for("admin_home"))
        else:
            return redirect(url_for("admin_login"))
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/admin-home", methods = ['GET', 'POST'])
@login_required
def admin_home():
    if request.method == 'GET':
        admin = Language.query.filter_by(file_name = 'admin').all()
        translation = dict_converter(admin, current_user.language)
        return render_template("auth/admin.html", admin = admin, translation = translation)
    
@app.route('/admin-users', methods = ['GET', 'POST'])
@login_required
def admin_users():
    if request.method == 'GET':
        users = User.query.filter_by(is_deleted = False).all()
        admin = Language.query.filter_by(file_name = 'admin').all()
        users_translation = Language.query.filter_by(file_name = 'user').all()
        translation = dict_converter(admin+users_translation, current_user.language)
        return render_template("users/list.html", users = users, translation = translation)
    elif request.method == 'POST' and 'delete' in request.form:
        user_id = request.form.get('delete')
        user = User.query.filter_by(id = user_id).first()
        user.is_deleted = True
        db.session.commit()
        return redirect(url_for('admin_users'))
    
@app.route('/users-create', methods = ['GET', 'POST'])
@login_required
def users_create():
    form = UserCreate()
    if request.method == 'GET':
        users_translation = Language.query.filter_by(file_name = 'user').all()
        admin = Language.query.filter_by(file_name = 'admin').all()
        translation = dict_converter(users_translation+admin, current_user.language)
        form.submit.label.text = translation.get(26)
        return render_template("users/create.html", form=form, translation = translation)
    elif form.validate_on_submit():
        full_name = form.full_name.data
        username = form.username.data
        password = form.password.data
        language = form.language.data
        user = User(full_name, username, password, language)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin_users'))
    
@app.route('/users-update/<user_id>', methods = ['GET', 'POST'])
@login_required
def users_update(user_id: int):
    user = User.query.filter_by(id = user_id).first()
    form = UserUpdate()
        
    if form.validate_on_submit():
        full_name = form.full_name.data
        username = form.username.data
        password = form.password.data
        language = form.language.data
        user.full_name = full_name
        user.username = username
        user.password = password
        user.language = language
        db.session.commit()
        return redirect(url_for('admin_users'))
    else:
        form.full_name.data = user.full_name
        form.username.data = user.username
        form.password.data = user.password
        form.language.data = user.language

        users_translation = Language.query.filter_by(file_name = 'user').all()
        admin = Language.query.filter_by(file_name = 'admin').all()
        translation = dict_converter(users_translation+admin, current_user.language)
        form.submit.label.text = translation.get(26)

        return render_template('users/update.html',form=form,translation = translation)