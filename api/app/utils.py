"""

Utility functions and helper methods for the Flask application.

This module contains various utility functions and helper methods used across the Flask application.

"""

from flask import Flask

from app.extensions import bcrypt, db, api


def register_flask_extensions(app: Flask) -> None:
    """Call the method 'init_app' to register the extensions in the Flask object passed as parameter.

    Args:
        app (Flask): The Flask app object.

    Returns:
     None
    """
    db.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app, validate=True)


def register_api_namespace(app: Flask) -> None:
    """Register the API namespace in the Flask app.

    Args:
        app (Flask): The Flask app object.

    Returns:
        None
    """
    from app.users.resources import user_namespace

    api.add_namespace(user_namespace, path="/api/user")


def register_flask_blueprints(app: Flask) -> None:
    """Register the Flask blueprints in the Flask app.

    Args:
        app (Flask): The Flask app object.

    Returns:
        None
    """
    from app.healthcheck import healthcheck_bp

    app.register_blueprint(healthcheck_bp)
