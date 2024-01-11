from .extensions import db, bcrypt


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :app: flask.Flask object
    :returns: None
    """
    from api.app.users.models import User

    db.init_app(app)
    # migrate.init_app(app, db)
    bcrypt.init_app(app)
