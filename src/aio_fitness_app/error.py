class UsdaFoodApiError(RuntimeError):
    """Raised when the USDA FoodData Central API cannot provide food data."""


class UsdaFoodApiRateLimitError(UsdaFoodApiError):
    """Raised when the USDA FoodData Central API rate limit is exceeded."""
