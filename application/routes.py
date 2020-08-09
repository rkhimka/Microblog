from flask import render_template, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from application import app, db
from application.forms import LoginForm, RegistrationForm
from application.models import Users

posts = [{"author": {"username": "Vova"}, "body": "I want to be programmer"},
         {"author": {"username": "Tanya"}, "body": "I want to be cosmetolog"}]


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title="Home", posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print(next_page)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title="Sign in", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully! {}, now you can login'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
