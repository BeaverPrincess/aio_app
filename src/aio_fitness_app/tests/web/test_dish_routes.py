from flask.testing import FlaskClient


class TestDishRoutes:
    def test_create_dish__valid_request(self, client: FlaskClient) -> None:
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

        assert response.status_code == 200
        assert response.json == {"status": "validated", "name": "Test Dish"}

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
