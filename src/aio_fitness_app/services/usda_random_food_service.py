from __future__ import annotations

from random import choice, randint

from aio_fitness_app.error import UsdaFoodApiError
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from shared_logging import AppLogger


class UsdaRandomFoodService:
    """Fetches one random USDA Foundation food."""

    _MIN_PAGE_NUMBER = 1
    _MAX_PAGE_NUMBER = 2

    def __init__(self, client: UsdaFoodClient, verbose: bool = False) -> None:
        self._client = client
        self._logger = AppLogger(verbose)

    def fetch_random_food(self) -> dict[str, object]:
        """Fetch a random page, select an FDC ID, and fetch its detail record."""
        page_number = randint(self._MIN_PAGE_NUMBER, self._MAX_PAGE_NUMBER)
        foods = self._client.fetch_foods_by_page(page_number)

        fdc_ids: list[int] = []
        for food in foods:
            fdc_id = food.get("fdcId")
            if isinstance(fdc_id, int) and not isinstance(fdc_id, bool) and fdc_id > 0:
                fdc_ids.append(fdc_id)

        if not fdc_ids:
            raise UsdaFoodApiError("USDA FoodData Central returned no valid FDC IDs.")

        fdc_id = choice(fdc_ids)
        self._logger.info(
            f"ℹ️ Fetching USDA food detail for FDC ID {fdc_id} from page {page_number}."
        )
        return self._client.fetch_food_by_fdc_id(fdc_id)
