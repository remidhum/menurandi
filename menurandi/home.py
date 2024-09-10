from dataclasses import dataclass

from menurandi.enums import CookingEquipments
from menurandi.people import Cooks
from menurandi.recipe import RecipeIngredient


Stock = dict[RecipeIngredient, int]


@dataclass
class Home:
	cooks: Cooks
	cooking_equipment: CookingEquipments
	stocks: Stock

	@property
	def cold_stocks(self) -> Stock:
		return {ingredient: stock for ingredient, stock in self.stocks.items() if ingredient.stored_in.Fridge}

	@property
	def frozen_stocks(self) -> Stock:
		return {ingredient: stock for ingredient, stock in self.stocks.items() if ingredient.stored_in.Freezer}

	@property
	def pantry_stocks(self) -> Stock:
		return {ingredient: stock for ingredient, stock in self.stocks.items() if ingredient.stored_in.Pantry}
