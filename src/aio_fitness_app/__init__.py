from collections.abc import Mapping

from flask import Flask

from .database import db
from .settings import DatabaseSettings


def create_app(config_overrides: Mapping[str, object] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if config_overrides is None:
        database_settings = DatabaseSettings.from_env()
        app.config["SQLALCHEMY_DATABASE_URI"] = database_settings.url
    else:
        app.config.update(config_overrides)

    db.init_app(app)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    return app
