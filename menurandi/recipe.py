import datetime
from dataclasses import dataclass
from typing import Literal

from menurandi.enums import (
	CookingEquipments, ImperialVolumeUnit, ImperialVolumetricConversionMap, IngredientType, MetricVolumeUnit,
	MetricVolumetricConversionMap, PreciseUnit, RecipeType,
	StorageType, Unit, VolumeUnit, VolumetricConversionMap,
)
from menurandi.people import Cook


@dataclass
class RecipeIngredient:
	name: str
	type: IngredientType
	stored_in: StorageType
	expiration_date: datetime.date | None = None


RecipeIngredients = list[RecipeIngredient]


def cycle_unit_factor(unit_a: PreciseUnit,
					  unit_b: PreciseUnit,
					  conversion_map: dict[PreciseUnit, tuple[PreciseUnit, float]],
					  scaling_factor: float = 1) -> float:
	"""
	Recursive function that cycles through the conversion map until the destination unit (b) is reached.
	"""
	next_unit, new_scaling_factor = conversion_map[unit_a]
	if next_unit == unit_b:
		return scaling_factor * new_scaling_factor
	return cycle_unit_factor(next_unit, unit_b, conversion_map=conversion_map, scaling_factor=scaling_factor)


x = {
	'to_metric': ((MetricVolumeUnit.Milliliter, ImperialVolumeUnit.Cup), 1),
}


def cycle_and_transfer_unit_factor(unit_a: PreciseUnit,
								   unit_b: PreciseUnit,
								   direction: Literal['to_imperial', 'to_metric']) -> float:
	scaling_factor = cycle_unit_factor(unit_a, MetricVolumeUnit.Milliliter,
									   conversion_map=MetricVolumetricConversionMap)
	scaling_factor *= VolumetricConversionMap[(MetricVolumeUnit.Milliliter, ImperialVolumeUnit.Cup)]
	return cycle_unit_factor(ImperialVolumeUnit.Cup, unit_b, conversion_map=ImperialVolumetricConversionMap,
							 scaling_factor=scaling_factor)


def get_volume_scaling_factor(unit_a: VolumeUnit, unit_b: VolumeUnit) -> float:
	if isinstance(unit_a, ImperialVolumeUnit) and isinstance(unit_b, ImperialVolumeUnit):
		return cycle_unit_factor(unit_a, unit_b, conversion_map=ImperialVolumetricConversionMap)
	if isinstance(unit_a, MetricVolumeUnit) and isinstance(unit_b, MetricVolumeUnit):
		return cycle_unit_factor(unit_a, unit_b, conversion_map=MetricVolumetricConversionMap)
	if isinstance(unit_a, MetricVolumeUnit) and isinstance(unit_b, ImperialVolumeUnit):
		scaling_factor = cycle_unit_factor(unit_a, MetricVolumeUnit.Milliliter,
										   conversion_map=MetricVolumetricConversionMap)
		scaling_factor *= VolumetricConversionMap[(MetricVolumeUnit.Milliliter, ImperialVolumeUnit.Cup)]
		return cycle_unit_factor(ImperialVolumeUnit.Cup, unit_b, conversion_map=ImperialVolumetricConversionMap, scaling_factor=scaling_factor)


def get_quantity_scaling_factor(unit_a: PreciseUnit, unit_b: PreciseUnit) -> float:
	pass


@dataclass
class Quantity:
	unit: Unit
	amount: float

	def __add__(self, other):
		assert self.unit == other.unit, f"Cannot add quantities with mismatched types ({self.unit} / {other.unit})."
		return Quantity(unit=self.unit, amount=self.amount + other.amount)

	def __iadd__(self, other):
		assert self.unit == other.unit, f"Cannot add quantities with mismatched types ({self.unit} / {other.unit})."
		self.amount += other.amount
		return self

	def convert_to(self, new_unit: PreciseUnit) -> None:
		"""
		Convert the quantity to a new type.
		"""
		assert new_unit in PreciseUnit, "Cannot convert an imprecise Unit."
		assert self.unit in PreciseUnit, "Cannot convert an imprecise Unit."

		qty_scaling_factor = get_quantity_scaling_factor(self.unit, new_unit)
		self.amount *= qty_scaling_factor
		self.unit = new_unit


Quantities = dict[RecipeIngredient, Quantity]


def add_quantities(quantities_list: list[Quantities]) -> Quantities:
	"""
	Adding quantities together requires a type check to make sure we're adding matching values together.
	"""
	overall_quantities: Quantities = dict()
	for quantities in quantities_list:
		for ingredient, quantity in quantities.items():
			# If new, add in and move on
			if ingredient not in overall_quantities.keys():
				overall_quantities[ingredient] = quantity
				break
			# If already existing, make sure the units match, convert otherwise before adding in.
			if quantity.unit != (current_qt_unit := overall_quantities[ingredient].unit):
				quantity.convert_to(current_qt_unit)
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
