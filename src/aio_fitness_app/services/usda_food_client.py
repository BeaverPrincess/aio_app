from __future__ import annotations

from http import HTTPStatus

import requests
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    JSONDecodeError,
    RequestException,
    Timeout,
)

from aio_fitness_app.error import UsdaFoodApiError, UsdaFoodApiRateLimitError
from aio_fitness_app.settings import UsdaFoodApiSettings
from shared_logging import AppLogger


class UsdaFoodClient:
    """Fetches foods pages from USDA FoodData Central"""

    _API_URL = "https://api.nal.usda.gov/fdc/v1/foods/list"
    _FOUNDATION_DATA_TYPE = "Foundation"
    _PAGE_SIZE = 200
    _REQUEST_TIMEOUT_SECONDS = 30

    def __init__(self, settings: UsdaFoodApiSettings) -> None:
        self._api_key = settings.api_str
        self._logger = AppLogger()

    def fetch_foundation_foods_page(self, page_number: int) -> list[dict[str, object]]:
        if page_number < 1:
            raise ValueError("page_number must be at least 1.")

        query_params = {
            "api_key": self._api_key,
            "dataType": self._FOUNDATION_DATA_TYPE,
            "pageNumber": page_number,
            "pageSize": self._PAGE_SIZE,
            "sortBy": "fdcId",
            "sortOrder": "asc",
        }
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(
                url=self._API_URL,
                params=query_params,
                headers=headers,
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
            message = "USDA request failed."
            self._logger.error(f"❌ {message}")
            raise UsdaFoodApiError(message) from None

        try:
            payload: object = response.json()
        except JSONDecodeError:
            error_message = "USDA FoodData Central returned invalid JSON."
            self._logger.error(f"❌ {error_message}")
            raise UsdaFoodApiError(error_message) from None

        if not isinstance(payload, list):
            message = "USDA FoodData Central returned an unexpected response shape."
            self._logger.error(f"❌ {message}")
            raise UsdaFoodApiError(message)

        return self._extract_food_items_from_payload(payload)

    def _extract_food_items_from_payload(
        self,
        payload: list[object],
    ) -> list[dict[str, object]]:
        foods: list[dict[str, object]] = []

        for item in payload:
            if not isinstance(item, dict):
                message = "USDA FoodData Central returned an invalid food record."
                self._logger.error(f"❌ {message}")
                raise UsdaFoodApiError(message)

            food: dict[str, object] = {}
            for key, value in item.items():
                if not isinstance(key, str):
                    message = "USDA FoodData Central returned an invalid food-record key."
                    self._logger.error(f"❌ {message}")
                    raise UsdaFoodApiError(message)
                food[key] = value

            foods.append(food)

        return foods
