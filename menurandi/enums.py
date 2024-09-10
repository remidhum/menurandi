from enum import StrEnum, auto


class RecipeType(StrEnum):
	"""
	Enum the different kinds of Recipe one can cook.
	To be extended as needed.
	"""
	Appetizer = auto()
	Soup = auto()
	Salad = auto()
	MainCourse = auto()
	Side = auto()
	Dish = auto()
	Dessert = auto()
	Bread = auto()
	Breakfast = auto()
	Snack = auto()
	Drink = auto()
	Sauce = auto()
	Casserole = auto()
	StirFry = auto()
	Grill = auto()


class IngredientType(StrEnum):
	"""
	Enum the different kinds of Ingredients used for cooking.
	To be extended as needed.
	"""
	Vegetable = auto()
	Fruit = auto()
	Meat = auto()
	Seafood = auto()
	Dairy = auto()
	Grain = auto()
	Legume = auto()
	Nut = auto()
	Seed = auto()
	Oil = auto()
	Fat = auto()
	Herb = auto()
	Spice = auto()
	Sweetener = auto()
	Condiment = auto()


class CookingEquipment(StrEnum):
	"""
	Enum the different kinds of Cooking equipment one might need to cook a dish.
	To be extended as needed.
	"""
	Mandoline = auto()
	MortarAndPestle = auto()
	FoodDehydrator = auto()
	SousVidePrecisionCooker = auto()
	ImmersionBlender = auto()
	MeatGrinder = auto()
	PressureCooker = auto()
	RiceCooker = auto()
	CrepePan = auto()
	Spiralizer = auto()
	CitrusZester = auto()
	FoodMill = auto()
	Siphon = auto()
	Tamis = auto()
	ButterChurn = auto()


CookingEquipments = set[CookingEquipment]


class StorageType(StrEnum):
	"""
	Enum the different kinds of storage for ingredients.
	"""
	Pantry = auto()
	Fridge = auto()
	Freezer = auto()


class QuantityType(StrEnum):
	"""
	Enum the different kinds of Quantities one can encounter in a recipe. Use for converting Volume to Mass units.
	To be extended as needed.
	"""
	Flour = auto()
	GranulatedSugar = auto()
	BrownSugar = auto()
	PowderedSugar = auto()
	BakingSoda = auto()
	BakingPowder = auto()
	Salt = auto()
	Cornstarch = auto()
	CocoaPowder = auto()
	Yeast = auto()
	Rice = auto()
	Pasta = auto()
	Breadcrumbs = auto()
	Oats = auto()
	Spices = auto()
	Milk = auto()
	HeavyCream = auto()
	Water = auto()
	VegetableOil = auto()
	OliveOil = auto()
	Vinegar = auto()
	SoySauce = auto()
	Broth = auto()
	Honey = auto()
	MapleSyrup = auto()
	VanillaExtract = auto()
	LemonJuice = auto()
	Wine = auto()
	TomatoSauce = auto()
	CoconutMilk = auto()
	Butter = auto()
	ChocolateChips = auto()


class MealType(StrEnum):
	"""
	Enum the different kinds of meals one can have.
	"""
	Breakfast = auto()
	Brunch = auto()
	Lunch = auto()
	Tea = auto()
	Diner = auto()


class AgeGroupType(StrEnum):
	"""
	Enum the age group of guests. Useful for scaling quantities in a recipe or warning from dangerous ingredients.
	"""
	Infant = auto()
	Child = auto()
	Teenager = auto()
	Adult = auto()
	Senior = auto()
