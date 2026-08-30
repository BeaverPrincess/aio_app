from __future__ import annotations

from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal

from aio_fitness_app.enum import IngredientImportDataKey, UsdaNutritionCode
from shared_logging import AppLogger


class UsdaFoodMapper:
    """Maps USDA food records to import data."""

    _NUTRIENT_UNITS = {
        UsdaNutritionCode.ENERGY: "KCAL",
        UsdaNutritionCode.PROTEIN: "G",
        UsdaNutritionCode.FAT: "G",
        UsdaNutritionCode.CARB: "G",
    }
    _REQUIRED_NUTRIENT_CODES = frozenset(_NUTRIENT_UNITS)
    _NUTRITION_QUANTUM = Decimal("0.01")
    _MAX_INGREDIENT_NAME_LENGTH = 255

    def __init__(self, verbose: bool = False) -> None:
        self._logger = AppLogger(verbose)

    def map_foundation_food(self, food: Mapping[str, object]) -> dict[str, str | int | Decimal]:
        """Map one USDA food record."""
        fdc_id = self._get_positive_integer(food.get("fdcId"))
        name = self._get_ingredient_name(food.get("description"))
        nutrients = self._extract_required_nutrients(food.get("foodNutrients"))
        if fdc_id is None or name is None or nutrients is None:
            self._logger.debug("Skipping a USDA food record with incomplete ingredient data.")
            return {}

        calories = nutrients.get(UsdaNutritionCode.ENERGY)
        protein = nutrients.get(UsdaNutritionCode.PROTEIN)
        fat = nutrients.get(UsdaNutritionCode.FAT)
        carbohydrate = nutrients.get(UsdaNutritionCode.CARB)
        if calories is None or protein is None or fat is None or carbohydrate is None:
            self._logger.debug("Skipping a USDA food record with missing required nutrients.")
            return {}

        return {
            IngredientImportDataKey.FDC_ID: fdc_id,
            IngredientImportDataKey.FOOD_NAME: name,
            IngredientImportDataKey.CALORIES_PER_100G: calories,
            IngredientImportDataKey.PROTEIN_PER_100G: protein,
            IngredientImportDataKey.CARB_PER_100G: carbohydrate,
            IngredientImportDataKey.FAT_PER_100G: fat,
        }

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

    def _extract_required_nutrients(
        self,
        value: object,
    ) -> dict[UsdaNutritionCode, Decimal] | None:
        if not isinstance(value, list):
            return None

        nutrients: dict[UsdaNutritionCode, Decimal] = {}
        for nutrient in value:
            if not isinstance(nutrient, Mapping):
                return None

            nutrient_code = self._get_nutrition_code(nutrient.get("number"))
            if nutrient_code is None or nutrient_code not in self._REQUIRED_NUTRIENT_CODES:
                continue

            if nutrient_code in nutrients:
                return None

            expected_unit = self._NUTRIENT_UNITS[nutrient_code]
            unit_name = nutrient.get("unitName")
            amount = self._get_non_negative_decimal(nutrient.get("amount"))
            if (
                not isinstance(unit_name, str)
                or unit_name.upper() != expected_unit
                or amount is None
            ):
                return None

            nutrients[nutrient_code] = amount

        return nutrients

    def _get_nutrition_code(self, value: object) -> UsdaNutritionCode | None:
        if isinstance(value, bool):
            return None

        if isinstance(value, int):
            nutrient_number = value
        elif isinstance(value, str) and value.isdecimal():
            nutrient_number = int(value)
        else:
            return None

        try:
            return UsdaNutritionCode(nutrient_number)
        except ValueError:
            return None

    def _get_non_negative_decimal(self, value: object) -> Decimal | None:
        if isinstance(value, bool) or not isinstance(value, int | float | Decimal):
            return None

        decimal_value = Decimal(str(value))
        if not decimal_value.is_finite() or decimal_value < 0:
            return None

        return decimal_value.quantize(self._NUTRITION_QUANTUM, rounding=ROUND_HALF_UP)
