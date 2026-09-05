from decimal import Decimal
from typing import ClassVar

import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from aio_fitness_app.database import db
from aio_fitness_app.dto.dish_request import CreateDishRequest, DishIngredientRequest
from aio_fitness_app.error import DishValidationError
from aio_fitness_app.models.dish import Dish
from aio_fitness_app.models.ingredient import Ingredient
from aio_fitness_app.services.dish_service import DishService
from aio_fitness_app.tests.base_test_class import BaselineRowsByModel, BaseTestClass


@pytest.mark.usefixtures("database_baseline")
class TestDishService(BaseTestClass):
    CHICKEN_INGREDIENT_ID: ClassVar[int] = 1
    RICE_INGREDIENT_ID: ClassVar[int] = 2

    @classmethod
    def _get_init_tables(cls) -> BaselineRowsByModel:
        return {
            Ingredient: [
                {
                    "id": cls.CHICKEN_INGREDIENT_ID,
                    "fdc_id": 10_001,
                    "name": "Chicken breast",
                    "calories_kcal_per_100g": Decimal("165.00"),
                    "protein_g_per_100g": Decimal("31.00"),
                    "carb_g_per_100g": Decimal("0.00"),
                    "fat_g_per_100g": Decimal("3.60"),
                },
                {
                    "id": cls.RICE_INGREDIENT_ID,
                    "fdc_id": 10_002,
                    "name": "White rice",
                    "calories_kcal_per_100g": Decimal("130.00"),
                    "protein_g_per_100g": Decimal("2.70"),
                    "carb_g_per_100g": Decimal("28.00"),
                    "fat_g_per_100g": Decimal("0.30"),
                },
            ]
        }

    def test_create_dish__valid_request_persists_dish_and_ingredients(
        self,
        database_transaction: None,
    ) -> None:
        service = DishService(verbose=False)

        created_dish = service.create_dish(
            CreateDishRequest(
                name="  Chicken rice bowl  ",
                description="High-protein lunch",
                ingredients=[
                    DishIngredientRequest(
                        ingredient_id=self.CHICKEN_INGREDIENT_ID,
                        amount_g=180,
                    ),
                    DishIngredientRequest(
                        ingredient_id=self.RICE_INGREDIENT_ID,
                        amount_g=150.5,
                    ),
                ],
            )
        )

        saved_dish = db.session.scalars(
            select(Dish)
            .options(selectinload(Dish.dish_ingredients))
            .where(Dish.id == created_dish.id)
        ).one()

        assert saved_dish.name == "chicken rice bowl"
        assert saved_dish.description == "High-protein lunch"
        assert {
            (dish_ingredient.ingredient_id, dish_ingredient.quantity_g)
            for dish_ingredient in saved_dish.dish_ingredients
        } == {
            (self.CHICKEN_INGREDIENT_ID, Decimal("180")),
            (self.RICE_INGREDIENT_ID, Decimal("150.5")),
        }

    def test_create_dish__empty_name_raises_validation_error(
        self,
        database_transaction: None,
    ) -> None:
        service = DishService(verbose=False)

        with pytest.raises(DishValidationError, match="Dish name cannot be empty."):
            service.create_dish(
                CreateDishRequest(
                    name="   ",
                    description=None,
                    ingredients=[
                        DishIngredientRequest(
                            ingredient_id=self.CHICKEN_INGREDIENT_ID,
                            amount_g=100,
                        )
                    ],
                )
            )

    def test_create_dish__duplicate_ingredient_ids_raise_validation_error(
        self,
        database_transaction: None,
    ) -> None:
        service = DishService(verbose=False)

        with pytest.raises(
            DishValidationError,
            match="Each ingredient may appear only once in a dish.",
        ):
            service.create_dish(
                CreateDishRequest(
                    name="Chicken bowl",
                    description=None,
                    ingredients=[
                        DishIngredientRequest(
                            ingredient_id=self.CHICKEN_INGREDIENT_ID,
                            amount_g=100,
                        ),
                        DishIngredientRequest(
                            ingredient_id=self.CHICKEN_INGREDIENT_ID,
                            amount_g=50,
                        ),
                    ],
                )
            )

    def test_create_dish__unknown_ingredient_raises_validation_error(
        self,
        database_transaction: None,
    ) -> None:
        service = DishService(verbose=False)

        with pytest.raises(
            DishValidationError,
            match="One or more requested ingredients do not exist.",
        ):
            service.create_dish(
                CreateDishRequest(
                    name="Unknown ingredient dish",
                    description=None,
                    ingredients=[
                        DishIngredientRequest(
                            ingredient_id=999,
                            amount_g=100,
                        )
                    ],
                )
            )

    @pytest.mark.parametrize(
        ("amount_g", "message"),
        [
            (0, "amount_g must be positive."),
            (1.234, "amount_g must have no more than two decimal places."),
        ],
    )
    def test_create_dish__invalid_amount_raises_validation_error(
        self,
        amount_g: int | float,
        message: str,
        database_transaction: None,
    ) -> None:
        service = DishService(verbose=False)

        with pytest.raises(DishValidationError, match=message):
            service.create_dish(
                CreateDishRequest(
                    name="Chicken bowl",
                    description=None,
                    ingredients=[
                        DishIngredientRequest(
                            ingredient_id=self.CHICKEN_INGREDIENT_ID,
                            amount_g=amount_g,
                        )
                    ],
                )
            )

    def test_create_dish__duplicate_normalized_name_raises_validation_error(
        self,
        database_transaction: None,
    ) -> None:
        service = DishService(verbose=False)
        service.create_dish(
            CreateDishRequest(
                name="Chicken bowl",
                description=None,
                ingredients=[
                    DishIngredientRequest(
                        ingredient_id=self.CHICKEN_INGREDIENT_ID,
                        amount_g=100,
                    )
                ],
            )
        )

        with pytest.raises(
            DishValidationError,
            match="A dish with the name 'chicken bowl' already exists.",
        ):
            service.create_dish(
                CreateDishRequest(
                    name="CHICKEN BOWL",
                    description=None,
                    ingredients=[
                        DishIngredientRequest(
                            ingredient_id=self.RICE_INGREDIENT_ID,
                            amount_g=100,
                        )
                    ],
                )
            )
