from http import HTTPStatus

from flask import Blueprint

from aio_fitness_app.dto.dish_request import CreateDishRequest
from aio_fitness_app.error import DishValidationError
from aio_fitness_app.services.dish_service import DishService
from aio_fitness_app.web.validators.dish_request_validators import DishRequestValidator

dish_blueprint = Blueprint("dish", __name__, url_prefix="/dish")


@dish_blueprint.post("")
@DishRequestValidator.validate_create_dish_request
def create_dish(
    create_dish_request: CreateDishRequest,
) -> tuple[dict[str, str | int | None], HTTPStatus]:
    """Create a dish from a validated HTTP request."""
    dish_service = DishService(verbose=True)

    try:
        dish = dish_service.create_dish(create_dish_request)
        return {"status": "created", "name": dish.name}, HTTPStatus.CREATED
    except DishValidationError as err:
        return {"status": "invalid dish", "message": str(err)}, HTTPStatus.BAD_REQUEST
