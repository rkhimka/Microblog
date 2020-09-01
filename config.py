import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # for security purposes
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my dog barney'

    # DB setup created application.db file
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # email notifications setup
    # NOT WORKING debug needed
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_USERNAME = 'romakhima@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = 'Lotersfuro2020'
    ADMINS = ['romakhima@gmail.com']

    # pagination: count of posts on the page
    POSTS_PER_PAGE = 10
