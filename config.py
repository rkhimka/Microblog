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
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['romkhimka@gmail.com']

    # pagination: count of posts on the page
    POSTS_PER_PAGE = 10
