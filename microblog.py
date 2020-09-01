from application import app, db, mail
from application.models import Users, Posts


@app.shell_context_processor
def shell_context():
    return {'db': db, 'Users': Users, 'Posts': Posts, 'mail': mail}
