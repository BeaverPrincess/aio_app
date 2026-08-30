from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL


def test_migrated_test_database__contains_application_tables(
    migrated_test_database: URL,
) -> None:
    """It applies the complete Alembic schema to the disposable test database."""
    engine = create_engine(migrated_test_database)

    try:
        with engine.connect() as connection:
            table_names = set(inspect(connection).get_table_names())
    finally:
        engine.dispose()

    assert {
        "alembic_version",
        "dishes",
        "dish_ingredients",
        "global_constants",
        "ingredients",
    } <= table_names
