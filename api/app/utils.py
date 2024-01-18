"""

Utility functions and helper methods for the Flask application.

This module contains various utility functions and helper methods used across the Flask application.

"""

from flask import Flask

from app.extensions import bcrypt, db


def register_extensions(app: Flask) -> None:
    """Call the method 'init_app' to register the extensions in the flask.Flask object passed as parameter.

    :param app: The Flask app object.
    :type app: flask.Flask
    :return: None
    """
    from app.users.models import User  # noqa I001 isort:skip

    db.init_app(app)
    bcrypt.init_app(app)
