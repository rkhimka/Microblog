from datetime import datetime

from flask import render_template, flash, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from application import db
from application.auth.forms import EditProfileForm, EmptyForm, PostForm
from application.main import main
from application.models import Users, Posts


@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('.index', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title="Home page", form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@main.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('.news', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('.news', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title="Home page", posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@main.route('/user/<username>')
@login_required
def profile(username):
    user = Users.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Posts.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('.profile', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('.profile', username=user.username, page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('profile.html', user=user, posts=posts.items, form=form, next_url=next_url,
                           prev_url=prev_url)


@main.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash("Your changes have been saved!")
        return redirect(url_for('.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@main.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash("User {} not found".format(username))
            return redirect(url_for('.index'))
        if user == current_user:
            flash("You can not follow yourself!")
            return redirect(url_for('.index', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('.profile', username=username))
    else:
        return redirect(url_for('.index'))


@main.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash("User {} not found".format(username))
            return redirect(url_for('.index'))
        if user == current_user:
            flash("You can not follow yourself!")
            return redirect(url_for('.index', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {} anymore!'.format(username))
        return redirect(url_for('.profile', username=username))
    else:
        return redirect(url_for('.index'))
