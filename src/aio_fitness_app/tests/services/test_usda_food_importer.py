from decimal import Decimal
from unittest.mock import Mock, call, patch

from aio_fitness_app.enum import IngredientImportDataKey
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.settings import UsdaFoodApiSettings


class TestUsdaFoodImporter:
    def test_import_batch_foods_page__saves_valid_ingredients_and_returns_true(self) -> None:
        """It maps a fetched page and excludes incomplete food records."""
        valid_food: dict[str, object] = {"fdcId": 1}
        incomplete_food: dict[str, object] = {"fdcId": 2}
        ingredient_data = {
            IngredientImportDataKey.FDC_ID: 1,
            IngredientImportDataKey.FOOD_NAME: "Apple",
            IngredientImportDataKey.CALORIES_PER_100G: Decimal("52.00"),
            IngredientImportDataKey.PROTEIN_PER_100G: Decimal("0.26"),
            IngredientImportDataKey.CARB_PER_100G: Decimal("13.81"),
            IngredientImportDataKey.FAT_PER_100G: Decimal("0.17"),
        }
        client = Mock(spec=UsdaFoodClient)
        client.fetch_foods_by_page.return_value = [valid_food, incomplete_food]

        with patch(
            "aio_fitness_app.services.usda_food_importer.UsdaFoodMapper",
            autospec=True,
        ) as mapper_type:
            mapper = mapper_type.return_value
            mapper.map_foundation_food.side_effect = [ingredient_data, {}]
            importer = UsdaFoodImporter(client)

            with patch.object(importer, "_save_ingredient_data_to_db", autospec=True) as mock_save:
                result = importer.import_batch_foods_page(page_number=1)

        assert result is True
        assert mapper_type.call_args == call(verbose=False)
        assert client.fetch_foods_by_page.call_args_list == [call(1)]
        assert mapper.map_foundation_food.call_args_list == [
            call(valid_food),
            call(incomplete_food),
        ]
        assert mock_save.call_args_list == [
            call([ingredient_data], next_page_number=2),
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
