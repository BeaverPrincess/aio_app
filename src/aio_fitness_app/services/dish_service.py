from decimal import Decimal, InvalidOperation

from sqlalchemy import select

from aio_fitness_app.database import db
from aio_fitness_app.dto.dish_request import CreateDishRequest, DishIngredientRequest
from aio_fitness_app.error import DishValidationError
from aio_fitness_app.models import Ingredient
from aio_fitness_app.models.dish import Dish
from aio_fitness_app.models.dish_ingredient import DishIngredient
from shared_logging import AppLogger

MAX_DISH_NAME_LENGTH = 255
MAX_QUANTITY_G = Decimal("99999999.99")


class DishService:
    """Service class for managing dishes."""

    def __init__(self, verbose: bool) -> None:
        self._logger = AppLogger(verbose)

    def create_dish(self, create_dish_request: CreateDishRequest) -> Dish:
        """Create a new dish in the database."""
        dish_name = self._validate_dish_name(create_dish_request.name)
        validated_ingredients = self._validate_ingredients(create_dish_request.ingredients)

        with db.session.begin():
            dish_name_lower = dish_name.lower()
            existing_dish_id = db.session.scalar(
                select(Dish.id).where(Dish.name == dish_name_lower)
            )
            if existing_dish_id is not None:
                raise DishValidationError(f"A dish with the name '{dish_name}' already exists.")

            request_ingredient_ids = [id for id, _ in validated_ingredients]
            existing_ingredient_ids = set(
                db.session.scalars(
                    select(Ingredient.id).where(Ingredient.id.in_(request_ingredient_ids))
                )
            )
            if len(request_ingredient_ids) != len(existing_ingredient_ids):
                raise DishValidationError("One or more requested ingredients do not exist.")

            new_dish = Dish()
            new_dish.name = dish_name_lower
            new_dish.description = (
                create_dish_request.description if create_dish_request.description else None
            )
            new_dish_ingredients = []
            for id, amount_g in validated_ingredients:
                dish_ingredient = DishIngredient()
                dish_ingredient.dish = new_dish
                dish_ingredient.ingredient_id = id
                dish_ingredient.quantity_g = amount_g
                new_dish_ingredients.append(dish_ingredient)

            db.session.add(new_dish)
            db.session.add_all(new_dish_ingredients)

        return new_dish

    def _validate_dish_name(self, dish_name: str) -> str:
        normalize_name = dish_name.strip().lower()
        if not normalize_name:
            raise DishValidationError("Dish name cannot be empty.")

        if len(normalize_name) > MAX_DISH_NAME_LENGTH:
            raise DishValidationError(f"Dish name cannot exceed {MAX_DISH_NAME_LENGTH} characters.")

        return normalize_name

    def _validate_ingredients(
        self, ingredient_requests: list[DishIngredientRequest]
    ) -> list[tuple[int, Decimal]]:
        if not ingredient_requests:
            raise DishValidationError("A dish must contain at least one ingredient.")

        ingredient_ids = [
            ingredient_request.ingredient_id for ingredient_request in ingredient_requests
        ]
        if len(set(ingredient_ids)) != len(ingredient_ids):
            raise DishValidationError("Each ingredient may appear only once in a dish.")

        validated_ingredients: list[tuple[int, Decimal]] = []
        for ingredient_request in ingredient_requests:
            if ingredient_request.ingredient_id <= 0:
                raise DishValidationError("ingredient_id must be positive.")

            validated_amount_g = self._validate_quantity_g(ingredient_request.amount_g)
            validated_ingredients.append((ingredient_request.ingredient_id, validated_amount_g))

        return validated_ingredients

    def _validate_quantity_g(self, amount_g: int | float) -> Decimal:
        try:
            quantity_g = Decimal(str(amount_g))
        except InvalidOperation as error:
            raise DishValidationError("amount_g must be a valid number.") from error

        if not quantity_g.is_finite() or quantity_g <= 0:
            raise DishValidationError("amount_g must be positive.")

        exponent = quantity_g.as_tuple().exponent
        if not isinstance(exponent, int):
            raise DishValidationError("amount_g must be a finite number.")

        if exponent < -2:
            raise DishValidationError("amount_g must have no more than two decimal places.")

        if quantity_g > MAX_QUANTITY_G:
            raise DishValidationError(f"amount_g must not exceed {MAX_QUANTITY_G}.")

        return quantity_g
