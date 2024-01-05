from flask import current_app
from sqlalchemy import select
from sqlalchemy.sql import text

from api.app import db


def test_app_exists(app):
    """Test if the Flask app instance exists."""
    assert current_app is not None


def test_config_testing(app):
    """Test if the app configuration is set to 'testing'."""
    assert app.config["ENV"] == "testing"


def test_app_settings(app):
    """Test specific settings of the Flask app."""
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True
    assert current_app.config["DEBUG"] is True
    assert current_app.config["TESTING"] is True


def test_db_version(app):
    with app.app_context():
        query = text("SELECT VERSION()")
        version = db.session.execute(query).first()[0]
        assert version is not None, "Database version should not be None"
        assert version.startswith("PostgreSQL 16")

