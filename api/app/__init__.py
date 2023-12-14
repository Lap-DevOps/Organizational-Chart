import os

from flask import Flask, jsonify


def create_app() -> Flask:
    """
    Creates an application instance to run API
    :return: A Flask object
    """

    app = Flask(__name__)
    config_name = os.environ.get("ENVIRONMENT", "development2")


    @app.route("/")
    def index():
        return {"API": "Test API v.0.1 "}

    @app.route('/health', methods=['GET'])
    def health_check():
        # Здесь вы можете добавить логику проверки здоровья вашего приложения
        # Например, проверка подключения к базе данных и других зависимостей
        health_status = {'status': 'ok'}
        return jsonify(health_status)


    return app
