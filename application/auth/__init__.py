from flask import Blueprint

a = Blueprint('auth', __name__, template_folder='templates')

from application.auth import email, forms, routes
