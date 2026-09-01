from decimal import Decimal
from unittest.mock import Mock, call, patch

import pytest
from sqlalchemy import select

from aio_fitness_app.constants import GLOBAL_CONSTANT_ROW_ID
from aio_fitness_app.database import db
from aio_fitness_app.enum import IngredientImportDataKey
from aio_fitness_app.models.global_constant import GlobalConstant
from aio_fitness_app.models.ingredient import Ingredient
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.settings import UsdaFoodApiSettings
from aio_fitness_app.tests.base_test_class import BaseTestClass


class TestUsdaFoodImporter:
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


@pytest.mark.usefixtures("database_baseline")
class TestUsdaFoodImporterDatabase(BaseTestClass):
    def test_global_constant_baseline__is_available_to_every_test(
        self,
        database_transaction: None,
        database_baseline: tuple[int, int],
    ) -> None:
        """It exposes the committed importer checkpoint baseline."""
        expected_foundation_page, expected_fndds_page = database_baseline

        statement = select(GlobalConstant).where(GlobalConstant.id == GLOBAL_CONSTANT_ROW_ID)
        global_constant = db.session.scalars(statement).one()

        assert global_constant.current_foundation_food_page == expected_foundation_page
        assert global_constant.current_fndds_food_page == expected_fndds_page

    def test_import_batch_foods_page__persists_mapped_ingredient_and_advances_checkpoint(
        self,
        database_transaction: None,
        database_baseline: tuple[int, int],
    ) -> None:
        """It saves valid mapped data and advances only the Foundation checkpoint."""
        expected_foundation_page, expected_fndds_page = database_baseline
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

            result = importer.import_batch_foods_page(page_number=expected_foundation_page)

        ingredient_statement = select(Ingredient).where(Ingredient.name == "Apple")
        saved_ingredient = db.session.scalars(ingredient_statement).one()

        missing_ingredient_statement = select(Ingredient).where(
            Ingredient.name == "Not an imported ingredient"
        )
        missing_ingredient = db.session.scalars(missing_ingredient_statement).one_or_none()

        global_constant_statement = select(GlobalConstant).where(
            GlobalConstant.id == GLOBAL_CONSTANT_ROW_ID
        )
        global_constant = db.session.scalars(global_constant_statement).one()

        assert result is True
        assert mapper_type.call_args == call(verbose=False)
        assert client.fetch_foods_by_page.call_args_list == [call(expected_foundation_page)]
        assert mapper.map_foundation_food.call_args_list == [
            call(valid_food),
            call(incomplete_food),
        ]
        assert saved_ingredient.fdc_id == 1
        assert saved_ingredient.calories_kcal_per_100g == Decimal("52.00")
        assert saved_ingredient.protein_g_per_100g == Decimal("0.26")
        assert saved_ingredient.carb_g_per_100g == Decimal("13.81")
        assert saved_ingredient.fat_g_per_100g == Decimal("0.17")
        assert missing_ingredient is None
        assert global_constant.current_foundation_food_page == expected_foundation_page + 1
        assert global_constant.current_fndds_food_page == expected_fndds_page
