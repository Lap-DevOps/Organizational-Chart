import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api.app import create_app


@pytest.fixture
def app(monkeypatch) -> Flask:
    """
    Fixture providing an instance of our Flask app with a specific configuration.

    Args:
        monkeypatch: Pytest fixture to modify environment variables.

    Returns:
        Flask: An instance of the Flask app.
    """
    monkeypatch.setenv("ENVIRONMENT", "testing")
    app = create_app()
    assert os.environ.get("ENVIRONMENT") == "testing"
    return app


@pytest.fixture
def db(app) -> SQLAlchemy:
    """
    Fixture providing a SQLAlchemy database instance.

    Args:
        app (Flask): The Flask app instance.

    Yields:
        SQLAlchemy: The SQLAlchemy database instance.
    """
    from api.app import db

    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Fixture providing a test client for the Flask app.

    Args:
        app (Flask): The Flask app instance.

    Returns:
        FlaskClient: A test client for making requests to the app.
    """
    return app.test_client()
