# all the imports necessary


import os
import secrets
from PIL import Image
from flask import json, url_for, redirect, Markup, Response, render_template, flash, g, session, jsonify, request, send_from_directory, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app         import bcrypt, login_manager, db
from app.models    import User
from app.users.forms     import LoginForm, RegisterForm, UpdateAccountForm
import os, shutil, re, cgi, json, random, time
from datetime import datetime


random.seed()  # Initialize the random number generator
users = Blueprint('users', __name__)
# provide login manager with load_user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# authenticate user
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.about = form.about.data
        user = User(username=current_user.username, firstName=current_user.firstName, email=current_user.email, lastName=current_user.lastName, about=current_user.about, image_file=image_file)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.about.data = current_user.about
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    return render_template( 'pages/account.html', title='Account details', description='ipNX Dashboard', image_file=image_file, form=form)
# register user
@users.route('/register', methods=['GET', 'POST'])

def register():
    
    # define login form here
    form = RegisterForm()

    msg = None

   
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, firstName=form.firstName.data, email=form.email.data, lastName=form.lastName.data, about=form.about.data, image_file=form.picture.data)
        user.save()
        msg = 'User created, please <a href="' + url_for('users.login') + '">login</a>'     

    
    return render_template( 'pages/register.html', title='Register',form=form, msg=msg)


# App main route + generic routing
# authenticate user
@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template('pages/login.html', title='Login', form=form)

    