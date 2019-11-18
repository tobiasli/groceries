# groceries
[![Build Status](https://travis-ci.org/tobiasli/tregex.svg?branch=master)](https://travis-ci.org/tobiasli/tregex)<br/>
[![Coverage Status](https://coveralls.io/repos/github/tobiasli/tregex/badge.svg?branch=master)](https://coveralls.io/github/tobiasli/tregex?branch=master)<br/>
[![PyPI version](https://badge.fury.io/py/tregex-tobiasli.svg)](https://badge.fury.io/py/tregex-tobiasli)<br/>

`groceries` is a package for parsing shopping lists and dinner menus and compiling shopping lists with all the items.

## Install

```
pip install groceries-tobiasli
```

## Usage

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

gl = gl - GroceryList(ingredients=['953.5 kg sugar', 'chocolate']) * 2
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

The recipes are searchable both on name, tags and their ingredients! You
can take what ingredients you have, and the cookbook will return the 
recipe that has the closest ingredient match with what you have available.

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
`Cookbook.Menu` is a class for parsing an entire weeks worth of shopping,
with syntax for meals on specific days as well as regular groceries.

To be able to 

The above methods patterns can be either a string or a compiled regular expression. `TregexCompiled` is a class for simply
containing the compiled regex to be run on the above methods. If patterns are long, this usage will speed things up
considerably.

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

So, happy shopping!
