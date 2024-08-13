from typing import Any

from menurandi.recipe import RecipeIngredients, Recipes


def _sort_recipes_by(recipes: Recipes) -> Recipes:
	pass


def _group_recipes_by(recipes: Recipes) -> dict[Any, Recipes]:
	pass


def _sort_ingredients_by(ingredients: RecipeIngredients) -> RecipeIngredients:
	pass


def _group_ingredients_by(ingredients: RecipeIngredients) -> dict[Any, RecipeIngredients]:
	pass


# TODO: partial the above private functions to the applied ones below
# sort_recipes_by_name
# sort_recipes_by_last_cooked
# sort_recipes_by_possible
# sort_recipes_by_cooking_duration
#
# group_recipes_by_type
# group_recipes_by_tags
# group_recipes_by_cook
#
#
# sort_ingredients_by_name
# sort_ingredients_by_expiration_date
# sort_ingredients_by_price
# sort_ingredients_by_store_order
#
#
# group_ingredients_by_type
# group_ingredients_by_storage_type
