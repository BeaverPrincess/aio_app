import os
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from flask import Flask
from flask.testing import FlaskClient
from psycopg import connect, sql
from sqlalchemy import URL, create_engine, make_url

from aio_fitness_app import create_app
from aio_fitness_app.database import db

PROJECT_ROOT = Path(__file__).resolve().parents[3]
TEST_DATABASE_ADMIN_URL_NAME = "TEST_DATABASE_ADMIN_URL"


def _get_test_database_admin_url() -> URL:
    try:
        return make_url(os.environ[TEST_DATABASE_ADMIN_URL_NAME])
    except KeyError:
        pytest.skip(f"{TEST_DATABASE_ADMIN_URL_NAME} is required for PostgreSQL integration tests.")


@pytest.fixture(scope="session")
def test_database_url() -> Iterator[URL]:
    """Create one uniquely named PostgreSQL database for this pytest session."""
    admin_url = _get_test_database_admin_url()
    database_name = f"aio_fitness_test_{uuid4().hex}"
    test_database_url = admin_url.set(database=database_name)
    admin_connection_string = admin_url.set(drivername="postgresql").render_as_string(
        hide_password=False
    )
    try:
        with connect(admin_connection_string, autocommit=True) as admin_connection:
            with admin_connection.cursor() as cursor:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))

        yield test_database_url
    finally:
        with connect(admin_connection_string, autocommit=True) as admin_connection:
            with admin_connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                        sql.Identifier(database_name)
                    )
                )


@pytest.fixture(scope="session")
def migrated_test_database(test_database_url: URL) -> Iterator[URL]:
    """Apply all Alembic migrations to the disposable test database."""
    engine = create_engine(test_database_url)
    try:
        with engine.begin() as connection:
            alembic_config = Config(str(PROJECT_ROOT / "alembic.ini"))
            alembic_config.attributes["connection"] = connection
            command.upgrade(alembic_config, "head")

        yield test_database_url
    finally:
        engine.dispose()


@pytest.fixture
def database_app(migrated_test_database: URL) -> Iterator[Flask]:
    """Create a Flask application connected to the migrated test database."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": migrated_test_database,
        }
    )

    with app.app_context():
        yield app


@pytest.fixture
def database_transaction(database_app: Flask) -> Iterator[None]:
    """Roll back all database changes made by one integration test."""
    connection = db.engine.connect()
    outer_transaction = connection.begin()

    db.session.remove()
    db.session.configure(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield
    finally:
        db.session.remove()

        try:
            outer_transaction.rollback()
        finally:
            connection.close()
            db.session.configure(
                bind=None,
                join_transaction_mode="conditional_savepoint",
            )


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
