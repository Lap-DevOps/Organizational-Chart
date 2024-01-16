from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


def test_app_exists(app: Flask) -> None:
    """Check if the Flask app instance exists.

    Args:
        app: The Flask application instance.

    Raises:
        AssertionError: If the `app` parameter is not an instance of the Flask class.
    """
    assert isinstance(app, Flask)


def test_config_testing(app: Flask) -> None:
    """
    Test if the app configuration is set to 'testing'.

    Args:
        app (Flask): The Flask application instance.
    """
    # Ensure that the app configuration is set to 'testing'
    assert app.config["ENV"] == "testing"


def test_app_settings(app: Flask) -> None:
    """
    Test specific settings of the Flask app.

    Args:
        app: The Flask application instance.
    """
    # Assert that the DEBUG and TESTING configurations of the app are set to True
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True

    # Assert that the DEBUG and TESTING configurations of the current app are set to True
    assert current_app.config["DEBUG"] is True
    assert current_app.config["TESTING"] is True


def test_db_version(app: Flask, db: SQLAlchemy) -> None:
    """
    Test the database version retrieval.

    Args:
        app: The Flask application instance.
        db: The SQLAlchemy database instance.

    Raises:
        AssertionError: If the retrieved database version is None or does not start with "PostgreSQL 16".
    """
    with app.app_context():
        query = text("SELECT VERSION()")
        version = db.session.execute(query).first()[0]

        assert version is not None, "Database version should not be None"
        assert version.startswith("PostgreSQL 16"), "Unexpected database version"
