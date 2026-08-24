from __future__ import annotations

from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal

from src.aio_fitness_app.dto.ingredient_dto import IngredientImportData


class UsdaFoodMapper:
    """Maps USDA food records to import data."""

    _ENERGY_NUTRIENT_NUMBER = 208
    _PROTEIN_NUTRIENT_NUMBER = 203
    _FAT_NUTRIENT_NUMBER = 204
    _CARBOHYDRATE_NUTRIENT_NUMBER = 205

    _NUTRIENT_UNITS = {
        _ENERGY_NUTRIENT_NUMBER: "KCAL",
        _PROTEIN_NUTRIENT_NUMBER: "G",
        _FAT_NUTRIENT_NUMBER: "G",
        _CARBOHYDRATE_NUTRIENT_NUMBER: "G",
    }
    _REQUIRED_NUTRIENT_NUMBERS = frozenset(_NUTRIENT_UNITS)
    _NUTRITION_QUANTUM = Decimal("0.01")
    _MAX_INGREDIENT_NAME_LENGTH = 255

    def map_foundation_food(self, food: Mapping[str, object]) -> IngredientImportData | None:
        """Map one USDA food record."""
        fdc_id = self._get_positive_integer(food.get("fdcId"))
        name = self._get_ingredient_name(food.get("description"))
        nutrients = self._extract_required_nutrients(food.get("foodNutrients"))
        if fdc_id is None or name is None or nutrients is None:
            return None

        calories = nutrients.get(self._ENERGY_NUTRIENT_NUMBER)
        protein = nutrients.get(self._PROTEIN_NUTRIENT_NUMBER)
        fat = nutrients.get(self._FAT_NUTRIENT_NUMBER)
        carbohydrate = nutrients.get(self._CARBOHYDRATE_NUTRIENT_NUMBER)
        if calories is None or protein is None or fat is None or carbohydrate is None:
            return None

        return IngredientImportData(
            fdc_id=fdc_id,
            name=name,
            calories_kcal_per_100g=calories,
            protein_g_per_100g=protein,
            carb_g_per_100g=carbohydrate,
            fat_g_per_100g=fat,
        )

    def _get_positive_integer(self, value: object) -> int | None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            return None

        return value

    def _get_ingredient_name(self, value: object) -> str | None:
        if not isinstance(value, str):
            return None

        name = value.strip()
        if not name or len(name) > self._MAX_INGREDIENT_NAME_LENGTH:
            return None

        return name

    def _extract_required_nutrients(self, value: object) -> dict[int, Decimal] | None:
        if not isinstance(value, list):
            return None

        nutrients: dict[int, Decimal] = {}
        for nutrient in value:
            if not isinstance(nutrient, Mapping):
                return None

            nutrient_number = self._get_nutrient_number(nutrient.get("number"))
            if nutrient_number not in self._REQUIRED_NUTRIENT_NUMBERS:
                continue

            if nutrient_number in nutrients:
                return None

            expected_unit = self._NUTRIENT_UNITS[nutrient_number]
            unit_name = nutrient.get("unitName")
            amount = self._get_non_negative_decimal(nutrient.get("amount"))
            if (
                not isinstance(unit_name, str)
                or unit_name.upper() != expected_unit
                or amount is None
            ):
                return None

            nutrients[nutrient_number] = amount

        return nutrients

    def _get_nutrient_number(self, value: object) -> int | None:
        if isinstance(value, bool):
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, str) and value.isdecimal():
            return int(value)

        return None

    def _get_non_negative_decimal(self, value: object) -> Decimal | None:
        if isinstance(value, bool) or not isinstance(value, int | float | Decimal):
            return None

        decimal_value = Decimal(str(value))
        if not decimal_value.is_finite() or decimal_value < 0:
            return None

        return decimal_value.quantize(self._NUTRITION_QUANTUM, rounding=ROUND_HALF_UP)
