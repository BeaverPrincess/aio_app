from decimal import Decimal
from unittest.mock import Mock, call, patch

from aio_fitness_app.dto.ingredient_dto import IngredientImportData
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.settings import UsdaFoodApiSettings


class TestUsdaFoodImporter:
    def test_import_batch_foods_page__returns_valid_ingredients(self) -> None:
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
        client.fetch_foods_by_page.return_value = [valid_food, incomplete_food]

        with patch(
            "aio_fitness_app.services.usda_food_importer.UsdaFoodMapper",
            autospec=True,
        ) as mapper_type:
            mapper = mapper_type.return_value
            mapper.map_foundation_food.side_effect = [ingredient_data, None]
            importer = UsdaFoodImporter(client)

            result = importer.import_batch_foods_page(page_number=1)

        assert result == [ingredient_data]
        assert mapper_type.call_args == call(verbose=False)
        assert client.fetch_foods_by_page.call_args_list == [call(1)]
        assert mapper.map_foundation_food.call_args_list == [
            call(valid_food),
            call(incomplete_food),
        ]

    def test_fetch_food_by_fdc_id__returns_one_food(self) -> None:
        """It requests one abridged USDA food with required nutrients."""
        result = {"fdcId": 123, "description": "Example food", "foodNutrients": []}
        response = Mock()
        response.json.return_value = result
        client = UsdaFoodClient(UsdaFoodApiSettings(api_str="test-key"))

        with patch(
            "aio_fitness_app.services.usda_food_client.requests.get",
            autospec=True,
            return_value=response,
        ) as mock_get:
            food = client.fetch_food_by_fdc_id(fdc_id=123)

        assert food == result
        assert mock_get.call_args == call(
            url="https://api.nal.usda.gov/fdc/v1/food/123",
            params={
                "api_key": "test-key",
                "format": "abridged",
                "nutrients": "208,203,204,205",
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )

    def test_fetch_foods_by_fdc_ids__returns_foods(self) -> None:
        """It requests several USDA foods in one request."""
        result = [
            {"fdcId": 123, "description": "First food", "foodNutrients": []},
            {"fdcId": 456, "description": "Second food", "foodNutrients": []},
        ]
        response = Mock()
        response.json.return_value = result
        client = UsdaFoodClient(UsdaFoodApiSettings(api_str="test-key"))

        with patch(
            "aio_fitness_app.services.usda_food_client.requests.get",
            autospec=True,
            return_value=response,
        ) as mock_get:
            foods = client.fetch_foods_by_fdc_ids(fdc_ids=[123, 456])

        assert foods == result
        assert mock_get.call_args == call(
            url="https://api.nal.usda.gov/fdc/v1/foods",
            params={
                "api_key": "test-key",
                "fdcIds": "123,456",
                "format": "abridged",
                "nutrients": "208,203,204,205",
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
