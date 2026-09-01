from collections.abc import Iterator

import pytest
from sqlalchemy import URL, delete

from aio_fitness_app import create_app
from aio_fitness_app.constants import GLOBAL_CONSTANT_ROW_ID
from aio_fitness_app.database import db
from aio_fitness_app.models.global_constant import GlobalConstant


class BaseTestClass:
    """Base class for all test classes."""

    @pytest.fixture(scope="class")
    @classmethod
    def database_baseline(cls, migrated_test_database: URL) -> Iterator[tuple[int, int]]:
        foundation_page = 1
        fndds_page = 1
        global_constant = GlobalConstant()
        global_constant.id = GLOBAL_CONSTANT_ROW_ID
        global_constant.current_foundation_food_page = foundation_page
        global_constant.current_fndds_food_page = fndds_page
        app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": migrated_test_database,
            }
        )

        with app.app_context():
            db.session.add(global_constant)
            db.session.commit()

        try:
            yield foundation_page, fndds_page
        finally:
            with app.app_context():
                db.session.execute(
                    delete(GlobalConstant).where(GlobalConstant.id == GLOBAL_CONSTANT_ROW_ID)
                )
                db.session.commit()
