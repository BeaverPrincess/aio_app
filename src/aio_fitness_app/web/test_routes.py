from flask import Blueprint

from aio_fitness_app.services.usda_food_client import UsdaFoodClient
from aio_fitness_app.services.usda_food_importer import UsdaFoodImporter
from aio_fitness_app.settings import UsdaFoodApiSettings

test_blueprint = Blueprint(
    "test",
    __name__,
)


@test_blueprint.get("/test")
def test_usda_food_endpoint() -> dict[str, str]:
    """Endpoint for manually testing."""
    client = UsdaFoodClient(UsdaFoodApiSettings.from_env())
    importer = UsdaFoodImporter(client, True)
    importer.continue_batch_food_import()
    return {"status": "ok", "message": "USDA food test endpoint is ready."}
