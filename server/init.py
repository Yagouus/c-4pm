from flask import Flask
from typing import Any


def init_app() -> Any:
    """Initialize Flask application and dashboard."""
    app = Flask(__name__)

    with app.app_context():
        # Lazy import within the context
        from server.main import init_dashboard

        # Initialize dashboard (assuming init_dashboard modifies app in-place)
        app = init_dashboard(app)

    return app
