from dataclasses import dataclass

from menurandi.enums import AgeGroupType, RecipeType


@dataclass
class Person:
	name: str
	last_name: str


@dataclass
class Cook(Person):
	"""
	Identify who will be cooking. Useful in non-singular households.
	"""
	specialty: RecipeType


Cooks = set[Cook]


@dataclass
class Guest:
	"""
	Identify who will be eating a meal. Useful to scale recipe amounts.
	"""
	age_group: AgeGroupType
	# allergies: RecipeIngredients  # TODO: fix circularity
	scaling_factor: float  # How many portions does the guest consume?  TODO: transform into a recipe based map?


Guests = set[Guest]
