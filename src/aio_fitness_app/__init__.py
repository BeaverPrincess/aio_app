from flask import Flask

from .database import db
from .settings import DatabaseSettings


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    database_settings = DatabaseSettings.from_env()
    app.config["SQLALCHEMY_DATABASE_URI"] = database_settings.url

    db.init_app(app)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    return app
