from flask import current_app


def test_app_exists(app):
    """Test if the Flask app instance exists."""
    assert current_app is not None


