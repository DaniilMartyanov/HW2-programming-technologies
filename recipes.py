class Ingredient:

  def __init__(self, name, quantity, unit):
    self.name = name
    self.quantity = quantity
    self.unit = unit
  
  @property
  def quantity(self): return self._quantity

  @quantity.setter
  def quantity(self, value):
    val = float(value)
    if val > 0: self._quantity = val
    else: raise ValueError("Количество должно быть положительным")
  
  def __str__(self): return f"{self.name}: {self.quantity} {self.unit}"

  def __repr__(self): return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

  def __eq__(self, other):
    if not isinstance(other, Ingredient): return False
    return self.name == other.name and self.unit == other.unit


class Recipe:

  def __init__(self, title, ingredients):
    self.title = title
    self.ingredients = list(ingredients)
  
  def add_ingredient(self, ingredient: Ingredient):
    if ingredient in self.ingredients:
      for i, ing in enumerate(self.ingredients):
        if ing == ingredient:
          self.ingredients[i] = Ingredient(ing.name, ing.quantity + ingredient.quantity, ing.unit)
          break
    else:
      self.ingredients.append(ingredient)
  
  @staticmethod
  def is_valid_ratio(ratio): return (isinstance(ratio, int) or isinstance(ratio, float)) and ratio > 0

  def scale(self, ratio: float):
    if not self.is_valid_ratio(ratio): raise ValueError("Множитель должен быть положительным")
    new_ingredients = [Ingredient(ing.name, ing.quantity * ratio, ing.unit) for ing in self.ingredients]
    return Recipe(self.title, new_ingredients)
  
  def __len__(self): return len(self.ingredients)

  def __str__(self):
    ingredients_str = '\n'.join(str(ing) for ing in self.ingredients)
    return f"{self.title}: Ингредиенты\n{ingredients_str}"


class ShoppingList:

  def __init__(self, items=None):
    self._items = items if items is not None else list()
  
  def add_recipe(self, recipe: Recipe, portions: float):
    if portions <= 0: raise ValueError("Количество порций должно быть положительным")
    scaled_recipe = recipe.scale(portions)
    for ing in scaled_recipe.ingredients:
      self._items.append((ing, scaled_recipe.title))
  
  def remove_recipe(self, title: str):
    self._items = [item for item in self._items if item[1] != title]
  
  def get_list(self):
    _dict = dict()
    for ing, tit in self._items:
      if (ing.name, ing.unit) in _dict: _dict[(ing.name, ing.unit)] += ing.quantity
      else: _dict[(ing.name, ing.unit)] = ing.quantity
    final_list = list()
    for ing_tuple, quantity in _dict.items():
      final_list.append(Ingredient(ing_tuple[0], quantity, ing_tuple[1]))
    final_list.sort(key=lambda ing: ing.name)
    return final_list

  def __add__(self, other):
    first_items = self._items.copy()
    second_items = other._items.copy()
    sl = ShoppingList(first_items + second_items)
    return sl


class DietaryRecipe(Recipe):

  def __init__(self, title, diet_type, ingredients=None):
    ingredients = ingredients if ingredients is not None else list()
    super().__init__(title, ingredients)
    self.diet_type = diet_type
  
  def scale(self, ratio:float):
    return DietaryRecipe(self.title, self.diet_type, super().scale(ratio).ingredients)

  def __str__(self): return f"[{self.diet_type}] {super().__str__()}"
