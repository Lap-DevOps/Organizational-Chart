from flask import current_app
from sqlalchemy.sql import text

from api.app import db


def test_app_exists(app):
    """
    Test if the Flask app instance exists.

    Args:
        app (Flask): The Flask application instance.
    """
    assert current_app is not None


def test_config_testing(app):
    """
    Test if the app configuration is set to 'testing'.

    Args:
        app (Flask): The Flask application instance.
    """
    assert app.config["ENV"] == "testing"


def test_app_settings(app):
    """
    Test specific settings of the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True
    assert current_app.config["DEBUG"] is True
    assert current_app.config["TESTING"] is True


def test_db_version(app):
    """
    Test the database version retrieval.

    Args:
        app (Flask): The Flask application instance.

    Raises:
        AssertionError: If the retrieved database version is None or does not start with "PostgreSQL 16".
    """
    with app.app_context():
        query = text("SELECT VERSION()")
        version = db.session.execute(query).first()[0]

        assert version is not None, "Database version should not be None"
        assert version.startswith("PostgreSQL 16"), "Unexpected database version"
