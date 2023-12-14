import os

import pytest
from flask import Flask

from api.app import create_app


@pytest.fixture
def app(monkeypatch) -> Flask:
    """Provides an instance of our Flask app with a specific configuration."""
    monkeypatch.setenv("ENVIRONMENT", "testing")
    app = create_app()
    with app.app_context():
        assert os.environ.get("ENVIRONMENT") == "testing"
        yield app


@pytest.fixture
def client(app):
    return app.test_client()
