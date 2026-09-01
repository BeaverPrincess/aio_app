from decimal import Decimal
from typing import ClassVar
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
from aio_fitness_app.tests.base_test_class import BaselineRowsByModel, BaseTestClass


@pytest.mark.usefixtures("database_baseline")
class TestUsdaFoodImporterDatabase(BaseTestClass):
    INITIAL_FOUNDATION_PAGE: ClassVar[int] = 2
    INITIAL_FNDDS_PAGE: ClassVar[int] = 3

    @classmethod
    def _get_init_tables(cls) -> BaselineRowsByModel:
        return {
            GlobalConstant: [
                {
                    "id": GLOBAL_CONSTANT_ROW_ID,
                    "current_foundation_food_page": 2,
                    "current_fndds_food_page": 3,
                }
            ]
        }

    def test_global_constant_baseline__is_available_to_every_test(
        self,
        database_transaction: None,
    ) -> None:
        """It exposes the committed importer checkpoint baseline."""
        statement = select(GlobalConstant).where(GlobalConstant.id == GLOBAL_CONSTANT_ROW_ID)
        global_constant = db.session.scalars(statement).one()

        assert global_constant.current_foundation_food_page == self.INITIAL_FOUNDATION_PAGE
        assert global_constant.current_fndds_food_page == self.INITIAL_FNDDS_PAGE

    def test_import_batch_foods_page__persists_mapped_ingredient_and_advances_checkpoint(
        self,
        database_transaction: None,
    ) -> None:
        """It saves valid mapped data and advances only the Foundation checkpoint."""
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

            result = importer.import_batch_foods_page(page_number=self.INITIAL_FOUNDATION_PAGE)

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
        assert client.fetch_foods_by_page.call_args_list == [call(self.INITIAL_FOUNDATION_PAGE)]
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
        assert global_constant.current_foundation_food_page == self.INITIAL_FOUNDATION_PAGE + 1
        assert global_constant.current_fndds_food_page == self.INITIAL_FNDDS_PAGE
