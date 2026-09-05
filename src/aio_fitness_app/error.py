class UsdaFoodApiError(RuntimeError):
    """Raised when the USDA FoodData Central API cannot provide food data."""


class UsdaFoodApiRateLimitError(UsdaFoodApiError):
    """Raised when the USDA FoodData Central API rate limit is exceeded."""


class DishRequestValidationError(ValueError):
    """Raised when a create-dish request does not match the required JSON shape."""


class DishValidationError(ValueError):
    """Raised when dish data violates a business rule."""
