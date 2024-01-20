"""

Utility functions and helper methods for the Flask application.

This module contains various utility functions and helper methods used across the Flask application.

"""

from flask import Flask

from app.extensions import bcrypt, db


def register_flask_extensions(app: Flask) -> None:
    """Call the method 'init_app' to register the extensions in the Flask object passed as parameter.

    Args:
        app (Flask): The Flask app object.

    Returns:
     None
    """
    db.init_app(app)
    bcrypt.init_app(app)
