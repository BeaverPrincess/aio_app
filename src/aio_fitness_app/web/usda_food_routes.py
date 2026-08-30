from http import HTTPStatus

from flask import Blueprint

from aio_fitness_app.error import UsdaFoodApiError, UsdaFoodApiRateLimitError
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.settings import UsdaFoodApiSettings

usda_food_blueprint = Blueprint("usda_food", __name__, url_prefix="/usda_foods")


@usda_food_blueprint.post("/import")
def trigger_usda_food_import() -> tuple[dict[str, str], HTTPStatus]:
    """Trigger USDA Foundation Foods import process"""
    try:
        client = UsdaFoodClient(settings=UsdaFoodApiSettings.from_env(), verbose=True)
        importer = UsdaFoodImporter(client=client, verbose=True)
        importer.continue_batch_food_import()
        return (
            {
                "status": "completed",
                "message": "USDA food import completed.",
            },
            HTTPStatus.OK,
        )

    except UsdaFoodApiRateLimitError:
        return (
            {
                "status": "rate_limited",
                "message": "USDA stopped the import because its rate limit was reached.",
            },
            HTTPStatus.TOO_MANY_REQUESTS,
        )

    except UsdaFoodApiError:
        return (
            {
                "status": "upstream_error",
                "message": "USDA could not complete the food import.",
            },
            HTTPStatus.BAD_GATEWAY,
        )
