"""
Module containing Flask extensions.

This module initializes and provides instances of Flask extensions like SQLAlchemy and Bcrypt.
"""

from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from app.database import Base

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "API key in the Authorization header. Example: Bearer <API_KEY>",
    }
}

db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()
api = Api(
    version="1.0",
    title="Organization Chart API",
    description="A simple RESTful API",
    authorizations=authorizations,
    doc="/swagger",
    prefix="/api",
    default_mediatype="application/json",
    catch_all_404s=False,
    serve_challenge_on_401=False,
)
