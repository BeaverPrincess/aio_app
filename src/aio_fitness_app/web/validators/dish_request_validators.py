from collections.abc import Callable
from functools import wraps
from http import HTTPStatus

from flask import request

from aio_fitness_app.dto.dish_request import (
    CreateDishRequest,
    CreateDishRequestField,
    DishIngredientRequest,
    DishIngredientRequestField,
)
from aio_fitness_app.error import DishRequestValidationError
from aio_fitness_app.type import JsonValue, ViewResponse

type ValidationFailureResponse = tuple[dict[str, str], HTTPStatus]


class DishRequestValidator:
    """Validate the JSON structure of dish HTTP requests."""

    @classmethod
    def validate_create_dish_request(
        cls,
        view: Callable[[CreateDishRequest], ViewResponse],
    ) -> Callable[[], ViewResponse | ValidationFailureResponse]:
        """Validate a create-dish JSON body before its route runs."""

        @wraps(view)
        def wrapped() -> ViewResponse | ValidationFailureResponse:
            try:
                create_dish_request = cls._parse_create_dish_request(request.get_json(silent=True))
            except DishRequestValidationError as error:
                return (
                    {
                        "status": "invalid_request",
                        "message": str(error),
                    },
                    HTTPStatus.BAD_REQUEST,
                )

            return view(create_dish_request)

        return wrapped

    @classmethod
    def _parse_create_dish_request(cls, payload: JsonValue) -> CreateDishRequest:
        if not isinstance(payload, dict):
            raise DishRequestValidationError("Request body must be a JSON object.")

        name = payload.get(CreateDishRequestField.NAME)
        if not isinstance(name, str):
            raise DishRequestValidationError("Field 'name' is required and must be a string.")

        description = payload.get(CreateDishRequestField.DESCRIPTION)
        if description is not None and not isinstance(description, str):
            raise DishRequestValidationError("Field 'description' must be a string or null.")

        ingredient_values = payload.get(CreateDishRequestField.INGREDIENTS)
        if not isinstance(ingredient_values, list) or not ingredient_values:
            raise DishRequestValidationError(
                "Field 'ingredients' is required and must contain at least one element."
            )

        ingredients = [cls._parse_dish_ingredient(value) for value in ingredient_values]

        return CreateDishRequest(
            name=name,
            description=description,
            ingredients=ingredients,
        )

    @classmethod
    def _parse_dish_ingredient(cls, payload: JsonValue) -> DishIngredientRequest:
        if not isinstance(payload, dict):
            raise DishRequestValidationError("Each ingredient must be a JSON object.")

        ingredient_id = payload.get(DishIngredientRequestField.INGREDIENT_ID)
        if not isinstance(ingredient_id, int) or isinstance(ingredient_id, bool):
            raise DishRequestValidationError(
                "Field 'ingredient_id' is required and must be an integer."
            )

        amount_g = payload.get(DishIngredientRequestField.AMOUNT_G)
        if not isinstance(amount_g, (int, float)) or isinstance(amount_g, bool):
            raise DishRequestValidationError("Field 'amount_g' is required and must be a number.")

        return DishIngredientRequest(
            ingredient_id=ingredient_id,
            amount_g=amount_g,
        )
