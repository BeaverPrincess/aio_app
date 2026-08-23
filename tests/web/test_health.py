from flask.testing import FlaskClient


class TestHealth:
    """Test the health check endpoint of the Flask application."""

    def test_status_ok(self, client: FlaskClient) -> None:
        """Test that the health check endpoint returns status 'ok'."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json == {"status": "ok"}
