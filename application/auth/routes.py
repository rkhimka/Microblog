from flask import render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from application import db
from application.auth import a
from application.auth.email import send_reset_password_email
from application.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, SetNewPasswordForm
from application.models import Users


@a.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print(next_page)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


@a.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully! {}, now you can login'.format(form.username.data))
        return redirect(url_for('.login'))
    return render_template('register.html', title='Registration', form=form)


@a.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@a.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password_email(user)
            flash("Letter with temporary password has been sent to your email!")
            return redirect(url_for('.login'))
        else: flash("Sorry, but requested email does not exist into the system!")
    return render_template("reset_password_request.html", title='Reset Password', form=form)


@a.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset!')
        return redirect(url_for('.login'))
    return render_template('reset_password.html', form=form)
