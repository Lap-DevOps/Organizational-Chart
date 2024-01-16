import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from flask import Flask
from flask.testing import FlaskClient
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
    # Set the environment variable to "testing"
    monkeypatch.setenv("ENVIRONMENT", "testing")

    # Create an instance of the Flask app
    app = create_app()

    # Assert that the environment variable is set to "testing"
    assert os.environ.get("ENVIRONMENT") == "testing"

    # Enter the app context
    with app.app_context():
        yield app


def create_alembic_config(app) -> AlembicConfig:
    """
    Create and configure an AlembicConfig object.

    Args:
        alembic_config_file (str): The path to the Alembic config file.

    Returns:
        AlembicConfig: The configured AlembicConfig object.
    """
    alembic_config_file = Path(__file__).resolve().parents[3] / "api" / "alembic.ini"
    alembic_config = AlembicConfig(alembic_config_file)
    db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    alembic_config.set_main_option("sqlalchemy.url", db_url)
    alembic_location = alembic_config.get_main_option("script_location")
    base_path = os.path.dirname(alembic_config_file)
    if not os.path.isabs(alembic_location):
        alembic_config.set_main_option("script_location", os.path.join(base_path, alembic_location))
    return alembic_config


@pytest.fixture
def db(app) -> SQLAlchemy:
    """
    Fixture providing a SQLAlchemy database instance.

    Args:
        app (Flask): The Flask app instance.

    Yields:
        SQLAlchemy: The SQLAlchemy database instance.
    """
    db = app.extensions["sqlalchemy"]
    # Create an AlembicConfig object
    alembic_config = create_alembic_config(app)

    # Run the migrations
    with app.app_context():
        command.upgrade(alembic_config, "head")

    alembic_config = create_alembic_config(app)

    with app.app_context():
        command.upgrade(alembic_config, "head")
    yield db

    with app.app_context():
        command.downgrade(alembic_config, "base")


def client(app: Flask) -> FlaskClient:
    """
    Fixture providing a test client for the Flask app.

    Args:
        app: The Flask app instance.

    Returns:
        A test client for making requests to the app.
    """
    return app.test_client()


def app_ctx(app: Flask) -> None:
    """
    Fixture for creating an application context.

    This fixture enters the application context using a `with` statement,
    allowing the test function to execute within the application context.
    It yields control back to the test function after entering the context.

    Args:
        app (Flask): The Flask application object.

    Returns:
        None
    """

    with app.app_context():
        yield
