from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aio_fitness_app.database import db

if TYPE_CHECKING:
    from .dish_ingredient import DishIngredient


class Dish(db.Model):
    """Represents a dish in the database."""

    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    dish_ingredients: Mapped[list[DishIngredient]] = relationship(back_populates="dish")
