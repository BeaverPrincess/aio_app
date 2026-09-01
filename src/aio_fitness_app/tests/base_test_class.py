from collections.abc import Iterator
from decimal import Decimal

import pytest
from flask_sqlalchemy.model import Model as FlaskSqlAlchemyModel
from sqlalchemy import URL

from aio_fitness_app import create_app
from aio_fitness_app.database import db

type BaselineColumnValue = int | str | Decimal | None
type BaselineRowValues = dict[str, BaselineColumnValue]
type BaselineRowsByModel = dict[
    type[FlaskSqlAlchemyModel],
    list[BaselineRowValues],
]


class BaseTestClass:
    """Provide class-owned baseline rows to PostgreSQL integration tests."""

    @classmethod
    def _get_init_tables(cls) -> BaselineRowsByModel:
        """Return the models and row values required by this test class."""
        raise NotImplementedError(f"{cls.__name__} must define _get_init_tables().")

    @classmethod
    def _get_baseline_table_values(cls) -> list[FlaskSqlAlchemyModel]:
        """Construct fresh ORM instances from the test class's row values."""
        baseline_rows: list[FlaskSqlAlchemyModel] = []
        for model, model_rows in cls._get_init_tables().items():
            for row_values in model_rows:
                row = model()
                for attribute_name, value in row_values.items():
                    setattr(row, attribute_name, value)

                baseline_rows.append(row)

        return baseline_rows

    @pytest.fixture(scope="class")
    @classmethod
    def database_baseline(cls, migrated_test_database: URL) -> Iterator[None]:
        """Insert and remove this test class's committed baseline rows."""
        app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": migrated_test_database,
            }
        )
        baseline_rows = cls._get_baseline_table_values()
        with app.app_context():
            db.session.add_all(baseline_rows)
            db.session.commit()

        try:
            yield
        finally:
            with app.app_context():
                for row in reversed(baseline_rows):
                    db.session.delete(row)

                db.session.commit()
