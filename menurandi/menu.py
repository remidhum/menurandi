import datetime
import operator
from dataclasses import dataclass
from functools import reduce

from menurandi.enums import MealType
from menurandi.people import Cook, Guests
from menurandi.recipe import Quantities, Recipes, add_quantities, scale_quantities


@dataclass
class Meal:
	"""
	A Meal is a collection of Recipes to execute by a Cook for Guests.
	"""
	recipes: Recipes
	guests: Guests
	cook: Cook

	@property
	def cooking_time(self) -> datetime.timedelta:
		return reduce(operator.add, [recipe.instructions.estimated_duration for recipe in self.recipes])

	@property
	def portions(self) -> float:
		return sum([guest.portion for guest in self.guests])

	@property
	def quantities(self) -> Quantities:
		quantities_list = [recipe.instructions.normalized_quantities for recipe in self.recipes]
		normalized_quantities = add_quantities(quantities_list=quantities_list)
		return scale_quantities(quantities=normalized_quantities, factor=self.portions)


Meals = list[Meal]

DailyMeals = dict[MealType, Meal]


@dataclass(order=True)
class DailyMenu:
	"""
	A DailyMenu is set for a specific date and groups a collection of DailyMeal (one per meal type).
	"""
	date: datetime.date
	meals: DailyMeals

	@property
	def day(self) -> str:
		return self.date.strftime("%A")

	@property
	def quantities(self) -> Quantities:
		return add_quantities(quantities_list=[meal.quantities for meal in self.meals.values()])


DailyMenus = list[DailyMenu]


@dataclass
class Menu:
	"""
	A Menu is simply a collection of DailyMenu with some utility and grouping methods.
	"""
	daily_menus: DailyMenus

	@property
	def start_date(self) -> datetime.date:
		return min([daily_menu.date for daily_menu in self.daily_menus])

	@property
	def menu_dates(self) -> list[datetime.date]:
		return [daily_menu.date for daily_menu in self.daily_menus]

	@property
	def quantities(self) -> Quantities:
		return add_quantities(quantities_list=[menu.quantities for menu in self.daily_menus])

	def add_daily_menu(self, daily_menu: DailyMenu) -> None:
		assert daily_menu.date not in self.menu_dates, f"Cannot add a Menu for {daily_menu.date}."
		self.daily_menus.append(daily_menu)

	def __getitem__(self, item: int | datetime.date) -> DailyMenu:
		match item:
			case int():
				return self.daily_menus[item]
			case datetime.date():
				return [daily_menu for daily_menu in self.daily_menus if daily_menu.date == item][0]
			case _:
				raise NotImplementedError(f"{item} is of a type not currently supported for item fetching.")
