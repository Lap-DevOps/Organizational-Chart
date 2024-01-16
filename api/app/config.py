"""
Module containing configuration settings for the API application.

Attributes:
    config = (): Configuration settings for the API application.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

current_file_directory = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(current_file_directory)
PARENT_DIR = os.path.abspath(os.path.join(current_file_directory, os.pardir))
DOTENV_PATH = os.path.join(PARENT_DIR, ".env")


if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)


class Config(object):
    """
    Main configuration class.

    Attributes:
        SECRET_KEY (str): Secret key for the application.
        SECURITY_PASSWORD_SALT (str): Salt for password hashing.
        SECURITY_PASSWORD_HASH (str): Hashing algorithm for passwords.
        DEBUG (bool): Debug mode, set to False.
        JWT_SECRET_KEY (str): Secret key for JWT.
        JWT_ACCESS_TOKEN_EXPIRES (timedelta): Expiry duration for access tokens.
        JWT_REFRESH_TOKEN_EXPIRES (timedelta): Expiry duration for refresh tokens.
        CORS_ORIGINS (List[str]): List of allowed CORS origins.

    Methods:
        init_app(app: Flask) -> None: Initialize the Flask application.

    Note:
        This class can be extended for specific environment configurations.
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "hard to guess string"
    SECURITY_PASSWORD_HASH = os.environ.get("SECURITY_PASSWORD_HASH") or "hard to guess string"
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "hard to guess string"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=31)
    CORS_ORIGINS = ["http://localhost:5000", "http:127.0.0.1:5000", "http:0.0.0.0"]

    @staticmethod
    def init_app(app):
        """
        Initialize the Flask application.

        Args:
            app (Flask): The Flask application instance.
        """
        pass


class DevelopmentConfig(Config):
    """
    Configuration settings for the development environment.

    Attributes:
        ENV (str): The environment mode set to 'development'.
        DEBUG (bool): Debug mode set to True.
        dev_database_user (str): The username for the development database.
        dev_database_password (str): The password for the development database.
        dev_database_host (str): The host address for the development database.
        dev_database_port (str): The port number for the development database.
        dev_database_name (str): The name of the development database.
        SQLALCHEMY_DATABASE_URI (str): The SQLAlchemy database URI for the development database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy track modifications set to False.
        SQLALCHEMY_ECHO (bool): SQLAlchemy echo mode set to False.
        SQLALCHEMY_ENGINE_OPTIONS (dict): Additional options for configuring SQLAlchemy Engine.
    """

    ENV = "development"
    DEBUG = True

    dev_database_user = os.environ.get("DEV_DATABASE_USER")
    dev_database_password = os.environ.get("DEV_DATABASE_PASSWORD")
    dev_database_host = os.environ.get("DEV_DATABASE_HOST")
    dev_database_port = os.environ.get("DEV_DATABASE_PORT")
    dev_database_name = os.environ.get("DEV_DATABASE_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{dev_database_user}:"
        f"{dev_database_password}@{dev_database_host}:"
        f"{dev_database_port}/{dev_database_name}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "echo": True,
        "max_overflow": 10,
    }


class TestingConfig(Config):
    """
    Testing configuration settings for the API application.

    Attributes:
        ENV (str): The environment mode set to 'testing'.
        DEBUG (bool): Debug mode set to True.
        TESTING (bool): Testing mode set to True.
        RESTX_MASK_SWAGGER (bool): RESTX Swagger mask set to True.

        test_database_user (str): The username for the testing database.
        test_database_password (str): The password for the testing database.
        test_database_host (str): The host address for the testing database.
        test_database_port (str): The port number for the testing database.
        test_database_name (str): The name of the testing database.

        SQLALCHEMY_DATABASE_URI (str): The SQLAlchemy database URI for the testing database.
        PRESERVE_CONTEXT_ON_EXCEPTION (bool): Set to False.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Set to False.
    """

    ENV = "testing"
    DEBUG = True
    TESTING = True
    RESTX_MASK_SWAGGER = True

    test_database_user = os.environ.get("TEST_DATABASE_USER")
    test_database_password = os.environ.get("TEST_DATABASE_PASSWORD")
    test_database_host = os.environ.get("TEST_DATABASE_HOST")
    test_database_port = os.environ.get("TEST_DATABASE_PORT")
    test_database_name = os.environ.get("TEST_DATABASE_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{test_database_user}:"
        f"{test_database_password}@{test_database_host}:"
        f"{test_database_port}/{test_database_name}"
    )

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configuration settings for the API application.

    Attributes:
        ENV (str): The environment mode set to 'production'.
        DEBUG (bool): Debug mode set to False.

        database_user (str): The username for the production database.
        database_password (str): The password for the production database.
        database_host (str): The host address for the production database.
        database_port (str): The port number for the production database.
        database_name (str): The name of the production database.

        SQLALCHEMY_DATABASE_URI (str): The SQLAlchemy database URI for the production database.
        SQLALCHEMY_ECHO (bool): SQLAlchemy echo mode set to False.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy track modifications set to False.
    """

    ENV = "production"
    DEBUG = False

    database_user = os.environ.get("PROD_DATABASE_USER")
    database_password = os.environ.get("PROD_DATABASE_PASSWORD")
    database_host = os.environ.get("PROD_DATABASE_HOST")
    database_port = os.environ.get("PROD_DATABASE_PORT")
    database_name = os.environ.get("PROD_DATABASE_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{database_user}:"
        f"{database_password}@{database_host}:"
        f"{database_port}/{database_name}"
    )

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
