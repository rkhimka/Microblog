from threading import Thread

from flask import render_template

from application import mail, app
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_message(subj, sender, recipients, body, html_part):
    msg = Message(subj, sender=sender, recipients=recipients)
    msg.body = body
    msg.html = html_part
    Thread(target=send_async_email, args=(app, msg)).start()


def send_reset_password_email(user):
    token = user.get_reset_password_token()
    send_message('[Microblog] Reset password request',
                 sender=app.config['ADMINS'][0],
                 recipients=[user.email],
                 body=render_template('email/reset_pass.txt', user=user, token=token),
                 html_part=render_template('email/reset_password.html', user=user, token=token))
