from http import HTTPStatus

from flask import Blueprint, request

from aio_fitness_app.enum import UsdaFoodType
from aio_fitness_app.error import UsdaFoodApiError, UsdaFoodApiRateLimitError
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.settings import UsdaFoodApiSettings

usda_food_blueprint = Blueprint("usda_food", __name__, url_prefix="/usda_foods")


@usda_food_blueprint.post("/import")
def trigger_usda_food_import() -> tuple[dict[str, str], HTTPStatus]:
    """Trigger USDA Foods import process"""
    food_type_value = request.args.get("food_type")
    if food_type_value is None:
        return (
            {
                "status": "invalid_request",
                "message": "food_type query parameter must be 'foundation' or 'fndds'.",
            },
            HTTPStatus.BAD_REQUEST,
        )

    try:
        food_type = UsdaFoodType(food_type_value)
    except ValueError:
        return (
            {
                "status": "invalid_request",
                "message": "food_type query parameter must be 'foundation' or 'fndds'.",
            },
            HTTPStatus.BAD_REQUEST,
        )

    try:
        client = UsdaFoodClient(
            settings=UsdaFoodApiSettings.from_env(), verbose=True, food_type=food_type
        )
        importer = UsdaFoodImporter(client=client, verbose=True, food_type=food_type)
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
