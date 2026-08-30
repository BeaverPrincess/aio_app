from decimal import Decimal

from sqlalchemy import select

from aio_fitness_app.database import db
from aio_fitness_app.models.ingredient import Ingredient


def test_database_transaction__allows_real_committed_queries(
    database_transaction: None,
) -> None:
    """It keeps a committed change available inside the current test."""
    ingredient = Ingredient()
    ingredient.fdc_id = 999_999
    ingredient.name = "Transaction test ingredient"
    ingredient.calories_kcal_per_100g = Decimal("100.00")
    ingredient.protein_g_per_100g = Decimal("10.00")
    ingredient.carb_g_per_100g = Decimal("10.00")
    ingredient.fat_g_per_100g = Decimal("10.00")

    db.session.add(ingredient)
    db.session.commit()

    statement = select(Ingredient).where(Ingredient.fdc_id == 999_999)
    saved_ingredient = db.session.scalars(statement).one()

    assert saved_ingredient.name == "Transaction test ingredient"
