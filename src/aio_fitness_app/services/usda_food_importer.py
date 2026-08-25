from __future__ import annotations

from aio_fitness_app.dto.ingredient_dto import IngredientImportData
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_mapper import UsdaFoodMapper
from shared_logging import AppLogger


class UsdaFoodImporter:
    """USDA Foods importer."""

    def __init__(
        self,
        client: UsdaFoodClient,
        mapper: UsdaFoodMapper,
        verbose: bool = False,
    ) -> None:
        self._client = client
        self._mapper = mapper
        self._logger = AppLogger(verbose)

    def import_batch_foods_page(self, page_number: int) -> list[IngredientImportData]:
        """Fetch and map one USDA Foundation Foods page."""
        foods = self._client.fetch_foods_by_page(page_number)
        ingredient_data_list: list[IngredientImportData] = []
        for food in foods:
            ingredient_data = self._mapper.map_foundation_food(food)
            if ingredient_data is not None:
                ingredient_data_list.append(ingredient_data)

        self._logger.info(
            f"ℹ️ Prepared {len(ingredient_data_list)} USDA ingredients from "
            f"{len(foods)} food records on page {page_number}."
        )
        return ingredient_data_list
