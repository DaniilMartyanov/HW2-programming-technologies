import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_init():
  ing = Ingredient("Мука", 500, "г")
  assert ing.name == "Мука"
  assert ing.quantity == 500
  assert ing.unit == "г"

def test_ingredient_str():
  ing = Ingredient("Мука", 500, "г")
  assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
  ing1 = Ingredient("Мука", 500, "г")
  ing2 = Ingredient("Мука", 600, "г")
  ing3 = Ingredient("Сахар", 500, "г")
  ing4 = Ingredient("Мука", 500, "кг")
  assert ing1 == ing2
  assert ing1 != ing3
  assert ing1 != ing4

def test_recipe_init():
  ing = Ingredient("Мука", 500, "г")
  recipe = Recipe("Пицца", [ing])
  assert recipe.title == "Пицца"
  assert recipe.ingredients == [ing]

def test_recipe_add_ingredient():
  ing1 = Ingredient("Мука", 500, "г")
  recipe = Recipe("Пицца", [ing1])
  ing2 = Ingredient("Сахар", 200, "г")
  recipe.add_ingredient(ing2)
  assert len(recipe.ingredients) == 2
  ing3 = Ingredient("Мука", 200, "г")
  recipe.add_ingredient(ing3)
  assert len(recipe.ingredients) == 2
  assert recipe.ingredients[0].quantity == 700

def test_recipe_scale():
  ing1 = Ingredient("Мука", 500, "г")
  ing2 = Ingredient("Сахар", 200, "г")
  recipe = Recipe("Пицца", [ing1, ing2])
  scaled_recipe = recipe.scale(2)
  assert scaled_recipe is not recipe
  assert scaled_recipe.ingredients[0].quantity == 1000
  assert scaled_recipe.ingredients[1].quantity == 400
  with pytest.raises(ValueError):
    recipe.scale(-1)

def test_recipe_len():
  ing1 = Ingredient("Мука", 500, "г")
  ing2 = Ingredient("Сахар", 200, "г")
  recipe = Recipe("Пицца", [ing1, ing2])
  assert len(recipe) == 2
  recipe.add_ingredient(ing1)
  assert len(recipe) == 2
  recipe.add_ingredient(Ingredient("Соль", 10, "г"))
  assert len(recipe) == 3

def test_shopping_list_add_recipe():
  recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г"), Ingredient("Сахар", 200, "г")])
  sl = ShoppingList()
  sl.add_recipe(recipe, 2)
  assert len(sl._items) == 2
  with pytest.raises(ValueError):
    sl.add_recipe(recipe, -1)

def test_shopping_list_remove_recipe():
  recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
  sl = ShoppingList()
  sl.add_recipe(recipe, 1)
  sl.remove_recipe("Пицца")
  assert len(sl._items) == 0
  sl.remove_recipe("Несуществующий рецепт")

def test_shopping_list_get_list():
  ing1 = Ingredient("Сахар", 200, "г")
  ing2 = Ingredient("Мука", 500, "г")
  recipe = Recipe("Пицца", [ing1, ing2])
  sl = ShoppingList()
  sl.add_recipe(recipe, 2)
  
  final_list = sl.get_list()
  assert len(final_list) == 2
  assert final_list[0].name == "Мука"
  assert final_list[0].quantity == 1000
  assert final_list[1].name == "Сахар"
  assert final_list[1].quantity == 400

def test_shopping_list_add():
  ing = Ingredient("Мука", 100, "г")
  sl1 = ShoppingList()
  sl1.add_recipe(Recipe("А", [ing]), 1)
  sl2 = ShoppingList()
  sl2.add_recipe(Recipe("Б", [ing]), 1)
  
  sl3 = sl1 + sl2
  assert len(sl3._items) == 2
  assert len(sl1._items) == 1
  assert len(sl2._items) == 1