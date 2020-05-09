from secrets import token_hex
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from iseeya import db, bcrypt
from iseeya.models import User
from iseeya.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, TokenForm, ActiveEmailForm)
from iseeya.users.utils import save_picture, send_reset_email, delete_picture, send_activation_email

users = Blueprint('users', __name__)


@users.route("/me/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = token_hex(8)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=False)
        db.session.add(user)
        db.session.commit()
        send_activation_email(user, password)
        flash('An email has been sent with default password.', 'info')
        return redirect(url_for('main.home'))
    return render_template('signup.html', title='Register', form=form)


@users.route("/me/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pages.page', page_name='home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.email == form.email.data) | (User.username == form.email.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('pages.page', page_name='home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/me/logout")
def logout():
    logout_user()
    return redirect(url_for('pages.page', page_name='home'))


@users.route("/me/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            delete_picture(current_user.image_file)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)




@users.route("/me/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('main.home'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/me/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/me/activate_email/<token>", methods=['GET', 'POST'])
def activate_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.home'))
    form = ActiveEmailForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your email has been activated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Active email', form=form)


@users.route("/me/token", methods=['GET', 'POST'])
@login_required
def token():
    form = TokenForm()
    token=None
    if form.validate_on_submit():
        token = current_user.get_reset_token()

    return render_template('token.html', title='token',
                           form=form, token=token)

