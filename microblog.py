from application import db, mail, create_app
from application.models import Users, Posts

app = create_app()


@app.shell_context_processor
def shell_context():
    return {'db': db, 'Users': Users, 'Posts': Posts, 'mail': mail}
