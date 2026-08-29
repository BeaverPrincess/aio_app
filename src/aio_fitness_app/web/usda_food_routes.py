from flask import Blueprint

from aio_fitness_app.error import UsdaFoodApiError, UsdaFoodApiRateLimitError
from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_random_food_service import UsdaRandomFoodService
from aio_fitness_app.settings import UsdaFoodApiSettings

usda_food_blueprint = Blueprint(
    "usda_food",
    __name__,
    url_prefix="/usda/foods",
)


@usda_food_blueprint.get("/random")
def get_random_food() -> dict[str, object] | tuple[dict[str, str], int]:
    """Return one random USDA Foundation food with nutrient data."""
    try:
        client = UsdaFoodClient(UsdaFoodApiSettings.from_env())
        service = UsdaRandomFoodService(client, True)
        return service.fetch_random_food()
    except KeyError:
        return {"error": "USDA_FOOD_API_KEY is not configured."}, 500
    except UsdaFoodApiRateLimitError as error:
        return {"error": str(error)}, 429
    except UsdaFoodApiError as error:
        return {"error": str(error)}, 502
