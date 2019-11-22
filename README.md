# groceries
[![Build Status](https://travis-ci.org/tobiasli/groceries.svg?branch=master)](https://travis-ci.org/tobiasli/groceries)<br/>
[![Coverage Status](https://coveralls.io/repos/github/tobiasli/groceries/badge.svg?branch=master)](https://coveralls.io/github/tobiasli/groceries?branch=master)<br/>
[![PyPI version](https://badge.fury.io/py/groceries-tobiasli.svg)](https://badge.fury.io/py/groceries-tobiasli)<br/>

`groceries` Tools for parsing human readable shopping lists and recipe ingredients.

## Install

```
pip install groceries-tobiasli
```

## Usage

`groceries` contains a set of classes that solve a lot of shopping and food-related problems:

* `Ingredient` is a container for a food item, and parses amount, unit and item name from an arbitrary string. The base structure for an `Ingredient` string is `Optional[amount] Optional[unit] grocery_name, Optional[comment]`.
* `GroceryList` is a container for `Ingredients` and handles summation of all ingredients, as well as algebra.
* `Cookbook` is a container for `Recipe`, and make them searchable.
* `Menu` is the class returned when you use a `Cookbook` to parse an actual, typed shopping list. It contains the recipes and ingredients that are parsed from the shopping list.

### Ingredient
`Ingredient` is a class that takes any arbitrary string describing an 
amount of an grocery item. The amount and unit is generalized and with 
the formatting in `groceries` the unit can be represented in 

```python
from groceries import Ingredient

print(repr(Ingredient('10 2/3 tbs soy sauce')))
# <Ingredient object: 1.60 dl soy sauce: <Unit: volume: [liter, litre, liters, ...]>>
```
To simply get the most reasonable representation of the `Ingredient`, 
simply convert it to a string:
```python
print(Ingredient('302.3949133 grams baked beans'))
# 1 lbs baked beans
```



### GroceryList
`GroceryList` is the base component for most of the functionality in `groceries`. A `GroceryList` accepts groceries
as strings on a human readable format. They are added to a `GroceryList` as `Ingredient` instances.

```python
from groceries import GroceryList

gl = GroceryList()

gl.add_ingredients([
    '2 pounds sugar',
    '2 kg sugar',
    'chocolate',
    '1/4 floz foo',
    '1 2/9 tbs foo'
])

print(gl)

# <GroceryList object: 3 ingredients
#                chocolate,
#        0.26 dl foo,
#      2907.18 g sugar
# >
```
`GroceryList` instances can be added, subtracted with other `GroceryLists`. They can also be multiplied with skalars.
```
gl = gl - GroceryList(ingredients=['953.5 g sugar', 'chocolate']) * 2
print(gl)

# <GroceryList object: 2 ingredients
#        0.26 dl foo,
#        1.00 kg sugar
# >
```

### Recipe and Cookbooks

The `GroceryList` class is used to represent ingredients in recipes. `Recipe` is a class that contains information
on how to cook a specific meal. You can have multiple `Recipes` and add them to a `Cookbook`.

The recipes are searchable both on name and tags. 

```python
# Demo scripts for grocery readme.
from groceries import Recipe, Cookbook


recipe1 = Recipe(
    name='Carbonara',
    tags=['pasta', 'fast', 'egg', 'bacon'],
    time=20,
    serves=2,
    how_to='''Cook pasta. As pasta is preparing, fry bacon. 
    When bacon is done, add frozen pees and continue frying until pees are cooked.
    Mix finished pasta with bacon and pees. Add eggs and grated parmesan and stir.
    Season with salt and pepper.''',
    ingredients=[
        '150 g spaghetti',
        '100 g bacon',
        '100 g frozen green pees',
        '2 eggs',
        '50 g parmesan',
        'salt',
        'pepper'
    ])

recipe2 = Recipe(name="Mac'n cheese", tags=['pasta', 'fast'], time=5, serves=2,
                 how_to='''Cook mac. Add cheese. serve.''', ingredients=['150 g maccaroni', '100 g cheese', ])

recipe3 = Recipe(name='Chocolate', tags=['sweet', 'dessert'], time=2, serves=2, how_to='''Eat chocolate.''',
                 ingredients=['200 g chocolate'])

cookbook = Cookbook(recipes=[recipe1, recipe2, recipe3])

# Accepts fuzzy string matching:

print(cookbook.find_recipe('mac cheese'))

# <Recipe object: Mac'n cheese>

# Mac'n cheese is the first match for pasta, but searches are cycling. 
# So when performing a category match again you won't be presented 
# with the same recipe again:

print(cookbook.find_recipe('pasta'))

# <Recipe object: Carbonara>
```

### Menu
`Menu` is a class for parsing an entire weeks worth of shopping,
with syntax for meals on specific days as well as regular groceries.

```python
# Continuation from previous code block.
menu = cookbook.parse_menu('''Monday: mac cheese
    Tuesday: sweet
    Wednesday: pasta
    2 tbs coffee
    1 floz baked beans
    1 banana
    2 banana
    4 liters coffee''')

print(menu.generate_processed_menu_str())
# Monday: Mac'n cheese til 2
# Tuesday: Chocolate til 2
# Wednesday: Carbonara til 2
# 0.30 dl coffee
# 0.30 dl baked beans
# 1 banana
# 2 banana
# 4 l coffee

print(menu.groceries)
# <GroceryList object: 13 ingredients
#          100 g bacon,
#        0.30 dl baked beans,
#              3 banana,
#          100 g cheese,
#          200 g chocolate,
#         4.03 l coffee,
#              2 eggs,
#          100 g frozen green pees,
#          150 g maccaroni,
#           50 g parmesan,
#                pepper,
#                salt,
#          150 g spaghetti
# >
```

### Changing configs
`groceries` has built in functionality to change whatever configuration
defines the units, ingredient rules and formatting.

To change a particular config, either
* modify an existing config at runtime,
* use one of the other supplied configs, or
* create your own from one of the `groceries.configs.config_types`.

To finally set a specific config, use `configs.set_config()`.

```python
from groceries import config, language

print(config.language.language_name)
# 'English'
config.set_config(language.norwegian.language)

print(config.language.language_name)
# 'Norwegian'
```
A special condition applies if you are changing unit configs.

### Changing unit config

For Units, specifically, we need to reload the unit definition if the
config relating to unit handling is changed. This is done via
`units.reload_units()`

```python
from groceries import config, configs, units, Ingredient

print(Ingredient('2 lbs butter'))
# 2 lb butter
```
But we want to force a different config for units. We want to use a 
purely metric unit definition that will always format `Ingredient`s as 
metric. 

To do that we have to find the unit definition that we want, and set
that config. Since we are changing the units, we also have to reload 
the units.
```python
config.set_config(configs.unit_definition.metric.unit_definition)
units.units.reload_units()
```
The new formatting will yield metric, as inches is removed from the
formatting definition.
```python
print(Ingredient('2 lb butter'))
# 907.18 g butter
```

So, happy shopping!
