# groceries
[![Build Status](https://travis-ci.org/tobiasli/groceries.svg?branch=master)](https://travis-ci.org/tobiasli/groceries)<br/>
[![Coverage Status](https://coveralls.io/repos/github/tobiasli/groceries/badge.svg?branch=master)](https://coveralls.io/github/tobiasli/groceries?branch=master)<br/>
[![PyPI version](https://badge.fury.io/py/groceries-tobiasli.svg)](https://badge.fury.io/py/tregex-tobiasli)<br/>

`groceries` is a package for parsing shopping lists and dinner menus and compiling shopping lists with all the items.

## Install

```
pip install groceries-tobiasli
```

## Usage

`groceries` contains a set of classes that solve a lot of shopping and food-related problems:

* `Ingredient` is a container for a food item, and parses amount, unit and item name from an arbitrary string.
* `GroceryList` is a container for `Ingredients` and handles summation of all ingredients, as well as algebra.
* `Cookbook` is a container for `Recipe`, and make them searchable.
* `Menu` is the class returned when you use a `Cookbook` to parse an actual, typed shopping list. It contains the recipes and ingredients that are parsed from the shopping list.

### GroceryList
`GroceryList` is the base component for most of the functionality in `groceries`. A `GroceryList` accepts groceries
as strings on a human readable format. They are added to a `GroceryList` as `Ingredient` instances. Groceries lists can
be added, subtracted and multiplied.

```python
from groceries import GroceryList

gl = GroceryList()

gl.add_ingredients([
    '2 pounds sugar',
    '2 kg sugar',
    'chocolate',
    '4 floz foo',
    '4 tbs foo'
])

print(gl)

# <GroceryList object: 3 ingredients
#                chocolate,
#        1.78 dl foo,
#        2.91 kg sugar
# >

gl = gl - GroceryList(ingredients=['953.5 g sugar', 'chocolate']) * 2
print(gl)

# <GroceryList object: 2 ingredients
#        1.78 dl foo,
#        1.00 kg sugar
# >
```

The base structure for an `Ingredient` string is 

`Optional[amount] Optional[unit] grocery_name, Optional[comment]`.

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
    how_to='''Cook pasta. As pasta is preparing, fry bacon. When bacon is done, add frozen pees and continue frying
    until pees are cooked. Mix finished pasta with bacon and pees. Add eggs and grated parmesan and stir. Season with
    salt and pepper.''',
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

To set a specific config, use `configs.set_config()`.

```python
from groceries import config, language

print(config.language.language_name)
# 'English'
config.set_config(language.norwegian.language)

print(config.language.language_name)
# 'Norwegian'
```

### Changing unit config

For Units, specifically, we need to reload the unit definition if the
config relating to unit handling is changed. This is done via
`units.reload_units()`

```python
from groceries.config.config_handler import config
from groceries.config.config_types import UnitDefinition
from groceries.config.unit_definition.metric_imperial import unit_definition
from groceries.units import units

from groceries.groceries import Ingredient

ing = Ingredient('2.75 inches')

print(ing.ingredient_formatted())
# 2 3/4 inches
```
The unit is formatted according to formatting rules that prioritize
perfect fractions of inches. But we want to force formatting to metric.

We look at the rules and remove the formatting rule for inches:
```
for rule in config.unit_definition.formatting['length']:
    print(rule)
# {'unit': 'cm', 'checks': [EqualTo(0)]}
# {'unit': 'inch', 'checks': [LessThan(0.5), FractionOf(0.0254)]}
# {'unit': 'mm', 'checks': [LessThan(0.01)]}
# {'unit': 'cm', 'checks': [GreaterThanOrEqualTo(0.01), LessThan(1)]}
# {'unit': 'm', 'checks': [AlwaysTrue()]}

# Remove inches from formatting rule for length:
new_formatting = unit_definition.formatting
new_formatting['length'] = [rule for rule in new_formatting['length'] if rule['unit'] != 'inch']

new_definition = UnitDefinition(
    units=unit_definition.units,
    formatting=new_formatting,
    constants=unit_definition.constants
)
```
Now we can set the new config and reload the units definition:
```
config.set_config(new_definition)
units.reload_units()
```
The new formatting will yield metric, as inches is removed from the
formatting definition.
```
print(Ingredient('2 3/4 inches').ingredient_formatted())
# 6.98 cm
```

So, happy shopping!
