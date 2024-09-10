from dataclasses import dataclass
from enum import StrEnum, auto


class UnitName(StrEnum):
	Teaspoon = auto()
	Tablespoon = auto()
	Cup = auto()
	Milliliter = auto()
	Deciliter = auto()
	Liter = auto()
	Ounce = auto()
	Pound = auto()
	Milligram = auto()
	Gram = auto()
	Kilogram = auto()

	Drop = auto()
	Pinch = auto()
	Dash = auto()
	Slice = auto()
	Piece = auto()
	Bundle = auto()


class UnitType(StrEnum):
	Volume = auto()
	Mass = auto()
	Other = auto()


class UnitConvention(StrEnum):
	"""
	Enum the different kinds of units to switch to and from.
	"""
	Metric = auto()
	Imperial = auto()


@dataclass
class Unit:
	name: UnitName
	type: UnitType
	convention: UnitConvention | None

	def __post_init__(self):
		self.to_si_factor = SI_FACTOR_MAP.get(self.name)

	@property
	def is_precise(self) -> bool:
		return self.convention is not None

	@property
	def from_si_factor(self) -> float | None:
		if self.to_si_factor is None:
			return None
		return 1 / self.to_si_factor


def get_si_unit(unit: Unit) -> Unit:
	return Unit(name=SI_UNIT_MAP[unit.type], type=unit.type, convention=UnitConvention.Metric)


SI_UNIT_MAP = {UnitType.Volume: UnitName.Liter, UnitType.Mass: UnitName.Gram}
SI_FACTOR_MAP = {
	UnitName.Teaspoon: 0.00492892,
	UnitName.Tablespoon: 0.0147868,
	UnitName.Cup: 0.2400005716272,
	UnitName.Milliliter: 0.001,
	UnitName.Deciliter: 0.01,
	UnitName.Liter: 1,
	UnitName.Ounce: 28.3495,
	UnitName.Pound: 453.592,
	UnitName.Milligram: 0.001,
	UnitName.Gram: 1,
	UnitName.Kilogram: 1000,
}