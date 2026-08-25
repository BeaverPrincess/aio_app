from decimal import Decimal
from unittest.mock import Mock, call

from aio_fitness_app.dto.ingredient_dto import IngredientImportData
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.services.usda_food_mapper import UsdaFoodMapper


class TestUsdaFoodImporter:
    def test_prepare_foundation_foods_page__returns_valid_ingredients(self) -> None:
        """It maps a fetched page and excludes incomplete food records."""
        valid_food: dict[str, object] = {"fdcId": 1}
        incomplete_food: dict[str, object] = {"fdcId": 2}
        ingredient_data = IngredientImportData(
            fdc_id=1,
            name="Apple",
            calories_kcal_per_100g=Decimal("52.00"),
            protein_g_per_100g=Decimal("0.26"),
            carb_g_per_100g=Decimal("13.81"),
            fat_g_per_100g=Decimal("0.17"),
        )
        client = Mock(spec=UsdaFoodClient)
        client.fetch_foundation_foods_page.return_value = [valid_food, incomplete_food]
        mapper = Mock(spec=UsdaFoodMapper)
        mapper.map_foundation_food.side_effect = [ingredient_data, None]
        importer = UsdaFoodImporter(client, mapper)

        result = importer.prepare_foundation_foods_page(page_number=1)

        assert result == [ingredient_data]
        assert client.fetch_foundation_foods_page.call_args_list == [call(1)]
        assert mapper.map_foundation_food.call_args_list == [
            call(valid_food),
            call(incomplete_food),
        ]
