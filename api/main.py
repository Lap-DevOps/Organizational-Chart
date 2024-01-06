# api/main.py
"""
Main module for the API application.

This module initializes the Flask application using the create_app function from the app module
and runs the application if executed directly.

Usage:
python main.py
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
