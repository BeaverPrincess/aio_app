from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aio_fitness_app.database import db

if TYPE_CHECKING:
    from .dish import Dish
    from .ingredient import Ingredient


class DishIngredient(db.Model):
    """The amount of one ingredient used in one dish"""

    __tablename__ = "dish_ingredients"
    __table_args__ = (
        UniqueConstraint("dish_id", "ingredient_id", name="uq_dish_ingredient"),
        CheckConstraint("quantity_g > 0", name="check_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    dish_id: Mapped[int] = mapped_column(ForeignKey("dishes.id"), nullable=False)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), nullable=False)
    quantity_g: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    dish: Mapped[Dish] = relationship(back_populates="dish_ingredients")
    ingredient: Mapped[Ingredient] = relationship(back_populates="dish_ingredients")
