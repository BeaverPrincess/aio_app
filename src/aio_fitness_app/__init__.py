from collections.abc import Mapping

from flask import Flask

from aio_fitness_app.database import db
from aio_fitness_app.settings import DatabaseSettings
from aio_fitness_app.web.dish_routes import dish_blueprint
from aio_fitness_app.web.test_routes import test_blueprint
from aio_fitness_app.web.usda_food_routes import usda_food_blueprint


def create_app(config_overrides: Mapping[str, object] | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if config_overrides is None:
        database_settings = DatabaseSettings.from_env()
        app.config["SQLALCHEMY_DATABASE_URI"] = database_settings.url
    else:
        app.config.update(config_overrides)

    db.init_app(app)
    app.register_blueprint(test_blueprint)
    app.register_blueprint(usda_food_blueprint)
    app.register_blueprint(dish_blueprint)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    return app
