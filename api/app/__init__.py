import os

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from api.app.config import config

db = SQLAlchemy()
migrate = Migrate(db)


def create_app() -> Flask:
    """
    Creates an application instance to run API
    :return: A Flask object
    """

    app = Flask(__name__)
    config_name = os.environ.get("ENVIRONMENT", "development2")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    print("API configuration:", app.config["ENV"])

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return {"API": "Test API v.0.1 "}

    @app.route('/health', methods=['GET'])
    def health_check():
        health_status = {'status': 'ok'}
        return jsonify(health_status)

    return app
