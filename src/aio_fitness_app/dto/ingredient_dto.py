from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class IngredientImportData:
    fdc_id: int
    name: str
    calories_kcal_per_100g: Decimal
    protein_g_per_100g: Decimal
    carb_g_per_100g: Decimal
    fat_g_per_100g: Decimal
