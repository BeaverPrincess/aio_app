from unittest.mock import Mock, call, patch

import pytest
from src.aio_fitness_app.services.usda_food_client import UsdaFoodClient
from src.aio_fitness_app.settings import UsdaFoodApiSettings


class TestUsdaFoodClient:
    def test_fetch_foundation_foods_page__returns_foods(self) -> None:
        """It requests one sorted Foundation Foods page and returns its records."""
        result = [{"fdcId": 123, "description": "Example food", "foodNutrients": []}]
        response = Mock()
        response.json.return_value = result
        client = UsdaFoodClient(UsdaFoodApiSettings(api_str="test-key"))

        with patch(
            "src.aio_fitness_app.services.usda_food_client.requests.get",
            autospec=True,
            return_value=response,
        ) as mock_get:
            foods = client.fetch_foundation_foods_page(page_number=1)

        assert foods == result
        assert mock_get.call_count == 1
        assert mock_get.call_args == call(
            url="https://api.nal.usda.gov/fdc/v1/foods/list",
            params={
                "api_key": "test-key",
                "dataType": "Foundation",
                "pageNumber": 1,
                "pageSize": 200,
                "sortBy": "fdcId",
                "sortOrder": "asc",
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
        assert response.raise_for_status.call_count == 1
        assert response.json.call_count == 1

    def test_fetch_foundation_foods_page__rejects_page_zero(self) -> None:
        """It rejects a page number that USDA does not support."""
        client = UsdaFoodClient(UsdaFoodApiSettings(api_str="test-key"))

        with pytest.raises(ValueError, match="page_number must be at least 1"):
            client.fetch_foundation_foods_page(page_number=0)
