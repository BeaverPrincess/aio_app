from flask import Blueprint

test_blueprint = Blueprint(
    "usda_food",
    __name__,
)


@test_blueprint.get("/test")
def test_usda_food_endpoint() -> dict[str, str]:
    """Provide a temporary endpoint for manually testing application code."""
    return {"status": "ok", "message": "USDA food test endpoint is ready."}
