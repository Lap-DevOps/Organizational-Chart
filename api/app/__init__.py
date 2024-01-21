"""
API Application Package.

This package contains core functionality for the API application, including the Flask
application creation and database initialization.

Usage:
from app import create_app, db

app = create_app()
db.create_all(app=app)
"""
# module: app
# noqa
from .app_factory import create_app
from .database import Base
from .extensions import bcrypt, db

__all__ = ["Base", "db", "bcrypt", "create_app"]
