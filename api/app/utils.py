from .extensions import db, migrate, bcrypt


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :app: flask.Flask object
    :returns: None
    """

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
