
from flask import Flask


def init_app():
    app = Flask(__name__)

    with app.app_context():
        from main_server import init_dashboard
        app = init_dashboard(app)

        return app
