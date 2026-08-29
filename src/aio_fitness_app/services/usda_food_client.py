from __future__ import annotations

from collections.abc import Mapping
from http import HTTPStatus

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    JSONDecodeError,
    RequestException,
    Timeout,
)

from aio_fitness_app.constants import USDA_FOOD_PAGE_SIDE
from aio_fitness_app.enum import UsdaNutritionCode
from aio_fitness_app.error import UsdaFoodApiError, UsdaFoodApiRateLimitError
from aio_fitness_app.settings import UsdaFoodApiSettings
from shared_logging import AppLogger


class UsdaFoodClient:
    """Fetches food data from USDA FoodData Central."""

    _FOODS_LIST_URL = "https://api.nal.usda.gov/fdc/v1/foods/list"
    _FOOD_DETAILS_URL = "https://api.nal.usda.gov/fdc/v1/food"
    _FOODS_DETAILS_URL = "https://api.nal.usda.gov/fdc/v1/foods"
    _FOUNDATION_DATA_TYPE = "Foundation"
    _REQUEST_TIMEOUT_SECONDS = 30
    _DETAIL_FORMAT = "abridged"
    _REQUIRED_NUTRIENTS = (
        f"{UsdaNutritionCode.ENERGY.value},"
        f"{UsdaNutritionCode.PROTEIN.value},"
        f"{UsdaNutritionCode.FAT.value},"
        f"{UsdaNutritionCode.CARB.value}"
    )

    def __init__(self, settings: UsdaFoodApiSettings, verbose: bool = False) -> None:
        self._api_key = settings.api_str
        self._logger = AppLogger(verbose)
        self._headers = {"Accept": "application/json"}

    def fetch_foods_by_page(self, page_number: int) -> list[dict[str, object]]:
        """Fetch one sorted page of USDA Foundation Foods."""
        if page_number < 1:
            raise ValueError("page_number must be at least 1.")

        query_params = {
            "api_key": self._api_key,
            "dataType": self._FOUNDATION_DATA_TYPE,
            "pageNumber": page_number,
            "pageSize": USDA_FOOD_PAGE_SIDE,
            "sortBy": "fdcId",
            "sortOrder": "asc",
        }
        payload = self._fetch_payload(self._FOODS_LIST_URL, query_params)

        return self._extract_food_items_from_payload(payload)

    def fetch_food_by_fdc_id(self, fdc_id: int) -> dict[str, object]:
        """Fetch one USDA food by its FDC ID."""
        if isinstance(fdc_id, bool) or not isinstance(fdc_id, int) or fdc_id <= 0:
            raise ValueError("fdc_id must be a positive integer.")

        query_params = {
            "api_key": self._api_key,
            "format": self._DETAIL_FORMAT,
            "nutrients": self._REQUIRED_NUTRIENTS,
        }
        payload = self._fetch_payload(
            f"{self._FOOD_DETAILS_URL}/{fdc_id}",
            query_params,
        )

        return self._extract_food_item_from_payload(payload)

    def fetch_foods_by_fdc_ids(self, fdc_ids: list[int]) -> list[dict[str, object]]:
        """Fetch up to 20 USDA foods by their FDC IDs."""
        if not fdc_ids:
            raise ValueError("fdc_ids must contain at least one FDC ID.")

        if len(fdc_ids) > 20:
            raise ValueError("fdc_ids must contain at most 20 FDC IDs.")

        if any(
            isinstance(fdc_id, bool) or not isinstance(fdc_id, int) or fdc_id <= 0
            for fdc_id in fdc_ids
        ):
            raise ValueError("fdc_ids must contain only positive integers.")

        query_params = {
            "api_key": self._api_key,
            "fdcIds": ",".join(str(fdc_id) for fdc_id in fdc_ids),
            "format": self._DETAIL_FORMAT,
            "nutrients": self._REQUIRED_NUTRIENTS,
        }
        payload = self._fetch_payload(self._FOODS_DETAILS_URL, query_params)

        return self._extract_food_items_from_payload(payload)

    def _fetch_payload(
        self,
        url: str,
        query_params: Mapping[str, str | int],
    ) -> object:
        try:
            response = requests.get(
                url=url,
                params=query_params,
                headers=self._headers,
                timeout=self._REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except HTTPError as error:
            if (
                error.response is not None
                and error.response.status_code == HTTPStatus.TOO_MANY_REQUESTS
            ):
                error_message = "USDA rate limit exceeded."
                self._logger.warning(f"⚠️ {error_message}")
                raise UsdaFoodApiRateLimitError(error_message) from None

            error_message = "USDA returned unsuccessful response."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message) from None
        except ConnectionError, Timeout:
            error_message = "Couldnt connect to USDA."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message) from None
        except RequestException:
            error_message = "USDA request failed."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message) from None

        try:
            return response.json()
        except JSONDecodeError:
            error_message = "USDA FoodData Central returned invalid JSON."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message) from None

    def _extract_food_item_from_payload(self, payload: object) -> dict[str, object]:
        if not isinstance(payload, dict):
            error_message = "USDA FoodData Central returned an unexpected response shape."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message)

        return self._extract_food_items_from_payload([payload])[0]

    def _extract_food_items_from_payload(self, payload: object) -> list[dict[str, object]]:
        if not isinstance(payload, list):
            error_message = "USDA FoodData Central returned an unexpected response shape."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message)

        foods: list[dict[str, object]] = []
        for item in payload:
            if not isinstance(item, dict):
                error_message = "USDA FoodData Central returned an invalid food record."
                self._logger.error(f"❌ {error_message}")
                raise UsdaFoodApiError(error_message)

            food: dict[str, object] = {}
            for key, value in item.items():
                if not isinstance(key, str):
                    error_message = "USDA FoodData Central returned an invalid food-record key."
                    self._logger.error(f"❌ {error_message}")
                    raise UsdaFoodApiError(error_message)

                food[key] = value

            foods.append(food)

        return foods
