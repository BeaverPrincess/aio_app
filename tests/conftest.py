from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from src.aio_fitness_app import create_app


@pytest.fixture
def app() -> Iterator[Flask]:
    """Create a Flask application for testing."""
    yield create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite+pysqlite:///:memory:",
        }
    )


@pytest.fixture
def client(app: Flask) -> Iterator[FlaskClient]:
    """Create a test client for the Flask application."""
    yield app.test_client()
