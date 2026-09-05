from http import HTTPStatus

from flask import Blueprint

from aio_fitness_app.dto.dish_request import CreateDishRequest
from aio_fitness_app.web.validators.dish_request_validators import DishRequestValidator

dish_blueprint = Blueprint("dish", __name__, url_prefix="/dish")


@dish_blueprint.post("")
@DishRequestValidator.validate_create_dish_request
def create_dish(
    create_dish_request: CreateDishRequest,
) -> tuple[dict[str, str | int | None], HTTPStatus]:
    return {"status": "validated", "name": create_dish_request.name}, HTTPStatus.OK
