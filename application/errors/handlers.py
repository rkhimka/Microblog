from flask import render_template

from application import db
from application.errors import errors


@errors.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
