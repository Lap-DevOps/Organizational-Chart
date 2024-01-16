from app.extensions import bcrypt, db


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :param app: The Flask app object.
    :type app: flask.Flask
    :return: None
    """
    from app.users.models import User  # noqa

    db.init_app(app)
    bcrypt.init_app(app)
