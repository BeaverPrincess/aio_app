from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from aio_fitness_app.constants import GLOBAL_CONSTANT_ROW_ID
from aio_fitness_app.database import db
from aio_fitness_app.error import UsdaFoodApiError
from aio_fitness_app.models.global_constant import GlobalConstant
from aio_fitness_app.models.ingredient import Ingredient
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_mapper import UsdaFoodMapper
from shared_logging import AppLogger

if TYPE_CHECKING:
    from decimal import Decimal


class UsdaFoodImporter:
    """USDA Foods importer."""

    def __init__(
        self,
        client: UsdaFoodClient,
        verbose: bool = False,
    ) -> None:
        self._client = client
        self._mapper = UsdaFoodMapper(verbose=verbose)
        self._logger = AppLogger(verbose)

    def import_batch_foods_page(self, page_number: int) -> bool:
        """Fetch and map one USDA Foundation Foods page."""
        foods = self._client.fetch_foods_by_page(page_number)
        if not foods:
            self._logger.info(f"ℹ️ USDA returned no food records on page {page_number}.")
            return False

        ingredient_data_list: list[dict[str, str | int | Decimal]] = []
        for food in foods:
            ingredient_data = self._mapper.map_foundation_food(food)
            if ingredient_data:
                ingredient_data_list.append(ingredient_data)

        self._logger.info(
            f"ℹ️ Prepared {len(ingredient_data_list)} USDA ingredients from "
            f"{len(foods)} food records on page {page_number}."
        )
        self._save_ingredient_data_to_db(ingredient_data_list, next_page_number=page_number + 1)
        return True

    def continue_batch_food_import(self) -> None:
        try:
            while True:
                next_usda_food_page_query = select(GlobalConstant.current_usda_food_page).where(
                    GlobalConstant.id == GLOBAL_CONSTANT_ROW_ID
                )
                next_usda_food_page = db.session.execute(
                    next_usda_food_page_query
                ).scalar_one_or_none()
                if next_usda_food_page is None:
                    self._logger.error("❌ No last food page.")
                    return

                has_foods = self.import_batch_foods_page(next_usda_food_page)
                if not has_foods:
                    return

        except UsdaFoodApiError:
            db.session.rollback()
            raise

    def _save_ingredient_data_to_db(
        self, ingredient_data_list: list[dict[str, str | int | Decimal]], next_page_number: int
    ) -> None:
        try:
            if ingredient_data_list:
                db.session.execute(insert(Ingredient), ingredient_data_list)

            update_current_page_statement = (
                update(GlobalConstant)
                .where(GlobalConstant.id == GLOBAL_CONSTANT_ROW_ID)
                .values(current_usda_food_page=next_page_number)
            )
            db.session.execute(update_current_page_statement)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            self._logger.error("❌ Could not save USDA ingredients and update the page checkpoint.")
            raise
