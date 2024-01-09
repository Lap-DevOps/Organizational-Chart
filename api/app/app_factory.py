"""Factory function to create the API application instance."""
import os

from flask import Flask, jsonify


from .config import config
from .utils import register_extensions


def create_app() -> Flask:
    """
    Create an application instance to run the API.

    Returns:
        Flask: A Flask object representing the API application.
    """
    app = Flask(__name__)

    config_name = os.environ.get("ENVIRONMENT", "development")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    print("API configuration:", app.config["ENV"])

    register_extensions(app)

    @app.route("/")
    def index():
        return {"API": "Test API v.0.212 "}

    @app.route("/health", methods=["GET"])
    def health_check():
        health_status = {"status": "ok"}
        return jsonify(health_status)

    return app
