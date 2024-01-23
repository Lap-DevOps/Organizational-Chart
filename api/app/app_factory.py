"""Factory function to create the API application instance."""
import os

from flask import Flask

from app.config import config
from app.utils import register_flask_extensions, register_api_namespace, register_flask_blueprints


def create_app() -> Flask:
    """
    Create and configure an instance of the Flask application.

    Returns:
        Flask: A Flask object representing the API application.
    """
    app = Flask(__name__)

    # Set the configuration based on the environment variable
    config_name = os.environ.get("ENVIRONMENT", "development")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    print("API configuration:", app.config["ENV"])

    register_flask_extensions(app)
    register_api_namespace(app)
    register_flask_blueprints(app)

    return app
