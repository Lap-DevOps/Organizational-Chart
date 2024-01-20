"""
Module containing Flask extensions.

This module initializes and provides instances of Flask extensions like SQLAlchemy and Bcrypt.
"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from app.database import Base

db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()
