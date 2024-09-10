import datetime
from dataclasses import dataclass

from menurandi.enums import (
	CookingEquipments, IngredientType, RecipeType,
	StorageType,
)
from menurandi.people import Cook
from menurandi.unit import Unit, get_si_unit


@dataclass
class RecipeIngredient:
	"""
	Base level ingredient to be used for recipe handling and pantry management.
	"""
	name: str
	type: IngredientType
	stored_in: StorageType
	expiration_date: datetime.date | None = None


RecipeIngredients = list[RecipeIngredient]


@dataclass
class Quantity:
	"""
	Uniform interface for dealing with quantities to allow cross unit handling.
	"""
	unit: Unit
	amount: float

	def __post_init__(self):
		# Force precise to be in S.I. to avoid conflicts when combining quantities
		if self.unit.is_precise:
			self.amount *= self.unit.to_si_factor
			self.unit = get_si_unit(unit=self.unit)

	def __add__(self, other):
		assert self.unit == other.unit, f"Cannot add quantities with mismatched units ({self.unit} / {other.unit})."
		return Quantity(unit=self.unit, amount=self.amount + other.amount)

	def __iadd__(self, other):
		assert self.unit == other.unit, f"Cannot add quantities with mismatched units ({self.unit} / {other.unit})."
		self.amount += other.amount
		return self


Quantities = dict[RecipeIngredient, Quantity]


def add_quantities(quantities_list: list[Quantities]) -> Quantities:
	"""
	Adding quantities together leaving the unit matching to the quantity itself.
	"""
	overall_quantities: Quantities = dict()
	for quantities in quantities_list:
		for ingredient, quantity in quantities.items():
			# Could use a default dict if a default quantity exists
			if ingredient not in overall_quantities.keys():
				overall_quantities[ingredient] = quantity
			else:
				overall_quantities[ingredient] += quantity
	return overall_quantities


def scale_quantities(quantities: Quantities, factor: float) -> Quantities:
	"""
	Simplistic scaling model for now where a recipe's quantities are scaled according to a factor.
	This factor can be between 0 and 1 to normalize it for a single portion.
	"""
	assert factor > 0, "A negative scaling factor makes no sense in its current meaning."
	return {i: Quantity(unit=q.unit, amount=q.amount * factor) for i, q in quantities.items()}


@dataclass
class RecipeInstructions:
	"""
	Store the concrete instructions/implementation for a recipe.
	"""
	quantities: Quantities
	servings: int
	instructions: str | None
	required_equipment: CookingEquipments | None = None
	estimated_duration: datetime.timedelta = datetime.timedelta(hours=0)
	original_link: str = ""
	attached_media: None = None  # TODO: support videos and/or photos

	@property
	def ingredients(self) -> RecipeIngredients:
		return list(self.quantities.keys())

	@property
	def normalized_quantities(self) -> Quantities:
		"""
		Make sure the quantities are normalized.
		This is a simplistic approach that does not work for recipes that require a minimum serving size.
		TODO: upgrade?
		"""
		return scale_quantities(quantities=self.quantities, factor=1 / self.servings)


@dataclass
class Recipe:
	"""
	Store all the relevant info and data for a given recipe.
	TODO: consider having a SimpleRecipe and a Advanced/Complete Recipe?
	"""
	name: str
	type: RecipeType
	instructions: RecipeInstructions
	tags: list[str] | None = None
	last_cooked: datetime.date | None = None
	cook: Cook | None = None

	@property
	def ingredients(self) -> RecipeIngredients:
		return self.instructions.ingredients


Recipes = set[Recipe]
