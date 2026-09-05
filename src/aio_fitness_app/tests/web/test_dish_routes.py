from unittest.mock import call, patch

from flask.testing import FlaskClient

from aio_fitness_app.dto.dish_request import CreateDishRequest, DishIngredientRequest
from aio_fitness_app.models.dish import Dish


class TestDishRoutes:
    def test_create_dish__valid_request(self, client: FlaskClient) -> None:
        created_dish = Dish()
        created_dish.name = "test dish"

        with patch("aio_fitness_app.web.dish_routes.DishService", autospec=True) as service_type:
            service = service_type.return_value
            service.create_dish.return_value = created_dish

            response = client.post(
                "/dish",
                json={
                    "name": "Test Dish",
                    "ingredients": [
                        {"ingredient_id": 1, "amount_g": 100},
                        {"ingredient_id": 2, "amount_g": 200},
                    ],
                },
            )

        assert service_type.call_args == call(verbose=True)
        assert service.create_dish.call_args == call(
            CreateDishRequest(
                name="Test Dish",
                description=None,
                ingredients=[
                    DishIngredientRequest(ingredient_id=1, amount_g=100),
                    DishIngredientRequest(ingredient_id=2, amount_g=200),
                ],
            )
        )
        assert response.status_code == 201
        assert response.json == {"status": "created", "name": "test dish"}

    def test_create_dish__missing_amount_g(self, client: FlaskClient) -> None:
        response = client.post(
            "/dish",
            json={
                "name": "Test Dish",
                "ingredients": [
                    {"ingredient_id": 1},
                ],
            },
        )

        assert response.status_code == 400
        assert response.json == {
            "status": "invalid_request",
            "message": "Field 'amount_g' is required and must be a number.",
        }
