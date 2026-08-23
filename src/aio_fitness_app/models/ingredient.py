from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.aio_fitness_app.database import db

if TYPE_CHECKING:
    from .dish_ingredient import DishIngredient


class Ingredient(db.Model):
    """Represents an ingredient in the database."""

    __tablename__ = "ingredients"
    __table_args__ = (
        CheckConstraint("calories_kcal_per_100g >= 0", name="check_calories_non_negative"),
        CheckConstraint("protein_g_per_100g >= 0", name="check_protein_non_negative"),
        CheckConstraint("carb_g_per_100g >= 0", name="check_carb_non_negative"),
        CheckConstraint("fat_g_per_100g >= 0", name="check_fat_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    calories_kcal_per_100g: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    protein_g_per_100g: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    carb_g_per_100g: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    fat_g_per_100g: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    dish_ingredients: Mapped[list[DishIngredient]] = relationship(back_populates="ingredient")
