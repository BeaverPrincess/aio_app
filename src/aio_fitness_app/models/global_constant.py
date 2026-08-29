from sqlalchemy import CheckConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column

from aio_fitness_app.constants import GLOBAL_CONSTANT_ROW_ID
from aio_fitness_app.database import db


class GlobalConstant(db.Model):
    """Store application's single mutable settings."""

    __tablename__ = "global_constants"
    __table_args__ = (CheckConstraint(f"id={GLOBAL_CONSTANT_ROW_ID}", name="singleton_id"),)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=False, default=GLOBAL_CONSTANT_ROW_ID
    )
    current_usda_food_page: Mapped[int] = mapped_column(Integer)
