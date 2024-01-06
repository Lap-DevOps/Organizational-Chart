"""
API Application Package.

This package contains core functionality for the API application, including the Flask
application creation and database initialization.

Usage:
from api.app import create_app, db

app = create_app()
db.create_all(app=app)
"""
from .app_factory import create_app, db

__all__ = ["create_app", "db"]
