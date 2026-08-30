from enum import IntEnum, StrEnum


class UsdaNutritionCode(IntEnum):
    ENERGY = 208
    PROTEIN = 203
    FAT = 204
    CARB = 205


class IngredientImportDataKey(StrEnum):
    FDC_ID = "fdc_id"
    FOOD_NAME = "name"
    CALORIES_PER_100G = "calories_kcal_per_100g"
    PROTEIN_PER_100G = "protein_g_per_100g"
    CARB_PER_100G = "carb_g_per_100g"
    FAT_PER_100G = "fat_g_per_100g"
