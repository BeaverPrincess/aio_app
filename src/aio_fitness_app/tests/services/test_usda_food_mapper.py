from decimal import Decimal

from aio_fitness_app.enum import IngredientImportDataKey
from aio_fitness_app.services.usda_food_mapper import UsdaFoodMapper


class TestUsdaFoodMapper:
    def test_map_foundation_food__returns_validated_ingredient_data(self) -> None:
        """It maps USDA nutrient values to the ingredient nutrition columns."""
        food: dict[str, object] = {
            "fdcId": 171413,
            "description": "  Apple, raw, with skin  ",
            "foodNutrients": [
                {"number": 208, "unitName": "KCAL", "amount": 52.126},
                {"number": 203, "unitName": "G", "amount": 0.26},
                {"number": 204, "unitName": "G", "amount": 0.17},
                {"number": 205, "unitName": "G", "amount": 13.81},
                {"number": 303, "unitName": "MG", "amount": 0.12},
            ],
        }
        mapper = UsdaFoodMapper()

        result = mapper.map_foundation_food(food)

        assert result == {
            IngredientImportDataKey.FDC_ID: 171413,
            IngredientImportDataKey.FOOD_NAME: "Apple, raw, with skin",
            IngredientImportDataKey.CALORIES_PER_100G: Decimal("52.13"),
            IngredientImportDataKey.PROTEIN_PER_100G: Decimal("0.26"),
            IngredientImportDataKey.CARB_PER_100G: Decimal("13.81"),
            IngredientImportDataKey.FAT_PER_100G: Decimal("0.17"),
        }

    def test_map_foundation_food__returns_empty_mapping_when_a_required_nutrient_is_missing(
        self,
    ) -> None:
        """It rejects foods that cannot populate every nutrition column."""
        food: dict[str, object] = {
            "fdcId": 171413,
            "description": "Apple, raw, with skin",
            "foodNutrients": [
                {"number": 208, "unitName": "KCAL", "amount": 52},
                {"number": 203, "unitName": "G", "amount": 0.26},
                {"number": 204, "unitName": "G", "amount": 0.17},
            ],
        }
        mapper = UsdaFoodMapper()

        result = mapper.map_foundation_food(food)

        assert result == {}
