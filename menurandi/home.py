from dataclasses import dataclass

from menurandi.enums import CookingEquipments
from menurandi.people import Cooks
from menurandi.recipe import RecipeIngredient


@dataclass
class Home:
	cooks: Cooks
	cooking_equipment: CookingEquipments
	stocks: dict[RecipeIngredient, int]
