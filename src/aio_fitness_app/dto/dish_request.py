from dataclasses import dataclass
from enum import StrEnum


class CreateDishRequestField(StrEnum):
    NAME = "name"
    DESCRIPTION = "description"
    INGREDIENTS = "ingredients"


class DishIngredientRequestField(StrEnum):
    INGREDIENT_ID = "ingredient_id"
    AMOUNT_G = "amount_g"


@dataclass(frozen=True, slots=True)
class DishIngredientRequest:
    """Represents a request to create or update a dish ingredient."""

    ingredient_id: int
    amount_g: int | float


@dataclass(frozen=True, slots=True)
class CreateDishRequest:
    """Represents a request to create a new dish."""

    name: str
    description: str | None
    ingredients: list[DishIngredientRequest]
