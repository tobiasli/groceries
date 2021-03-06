﻿# -------------------------------------------------------------------------------
# Name:        GroceryShopping_Test_Suite
# Purpose:      Test the components of the groceries class.
#
# Author:      Tobias
#
# Created:     01.05.2015
# Copyright:   (c) Tobias 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import unittest

from groceries import recipes, groceries
from groceries.test.bin import cookbook_reader
from groceries import Recipe, Cookbook, Menu

RECIPE_EXAMPLE_1 = {}
RECIPE_EXAMPLE_1['name'] = 'Chili con Carne'
RECIPE_EXAMPLE_1['tags'] = ['kjøtt', 'gryte']
RECIPE_EXAMPLE_1['time'] = 45
RECIPE_EXAMPLE_1[
    'how_to'] = 'Stek løk, hvitløk blankt. Ha i kjøttdeig og stek til kjøttdeig er gjennomstekt. Ha i paprika og tomatpure, stek litt videre. Ha i hakket tomat, bønner og krydder. Stek i 30 minutter. Salat ved siden av.'
RECIPE_EXAMPLE_1['serves'] = 2
RECIPE_EXAMPLE_1['ingredients'] = [
    '400g kjøttdeig',
    '2 bokser hakket tomat',
    '1 2/3 paprika',
    '1.25 ts sennep',
    '1 boks chillibønner (kidneybønner med chillisaus)',
    '2 fedd hvitløk',
    '1 paprika',
    '1/2 hjertesalat',
]

RECIPE_EXAMPLE_2 = {}
RECIPE_EXAMPLE_2['name'] = 'TACOPARTY!'
RECIPE_EXAMPLE_2['tags'] = ['kjøtt', 'digg']
RECIPE_EXAMPLE_2['time'] = 45
RECIPE_EXAMPLE_2['how_to'] = 'Gjør det vanlige!'
RECIPE_EXAMPLE_2['serves'] = 4
RECIPE_EXAMPLE_2['ingredients'] = [
    '200g kjøttdeig',
    '0.2kg pulled pork',
    '2 rødløk',
    '2 1/2 avokado',
    '1 paprika',
    '1/2 hjertesalat',
    '1 3/4 dl sennep',
]

RECIPE1_INGREDIENTS_FORMATED = [
    '1 boks chillibønner',
    '2 bokser hakket tomat',
    '1/2 hjertesalat',
    '2 fedd hvitløk',
    '400 g kjøttdeig',
    '2 2/3 paprika',
    '1 1/4 ts sennep']

RECIPE_COMBINATION_GROCERY_LIST_COMPONENTS = [
    {'amount': '2 1/2',
     'components': [{'amount': '2 1/2',
                     'comments': [],
                     'name': 'avokado',
                     'recipe': 'TACOPARTY!'}],
     'name': 'avokado'},
    {'amount': '1 boks',
     'components': [{'amount': '1 boks',
                     'comments': ['kidneybønner med chillisaus'],
                     'name': 'chillibønner',
                     'recipe': 'Chili con Carne'}],
     'name': 'chillibønner'},
    {'amount': '2 bokser',
     'components': [{'amount': '2 bokser',
                     'comments': [],
                     'name': 'hakket tomat',
                     'recipe': 'Chili con Carne'}],
     'name': 'hakket tomat'},
    {'amount': '1',
     'components': [{'amount': '1/2',
                     'comments': [],
                     'name': 'hjertesalat',
                     'recipe': 'Chili con Carne'},
                    {'amount': '1/2',
                     'comments': [],
                     'name': 'hjertesalat',
                     'recipe': 'TACOPARTY!'}],
     'name': 'hjertesalat'},
    {'amount': '2 fedd',
     'components': [{'amount': '2 fedd',
                     'comments': [],
                     'name': 'hvitløk',
                     'recipe': 'Chili con Carne'}],
     'name': 'hvitløk'},
    {'amount': '600 g',
     'components': [{'amount': '400 g',
                     'comments': [],
                     'name': 'kjøttdeig',
                     'recipe': 'Chili con Carne'},
                    {'amount': '200 g',
                     'comments': [],
                     'name': 'kjøttdeig',
                     'recipe': 'TACOPARTY!'}],
     'name': 'kjøttdeig'},
    {'amount': '3 2/3',
     'components': [{'amount': '1 2/3',
                     'comments': [],
                     'name': 'paprika',
                     'recipe': 'Chili con Carne'},
                    {'amount': '1',
                     'comments': [],
                     'name': 'paprika',
                     'recipe': 'Chili con Carne'},
                    {'amount': '1',
                     'comments': [],
                     'name': 'paprika',
                     'recipe': 'TACOPARTY!'}],
     'name': 'paprika'},
    {'amount': '200 g',
     'components': [{'amount': '200 g',
                     'comments': [],
                     'name': 'pulled pork',
                     'recipe': 'TACOPARTY!'}],
     'name': 'pulled pork'},
    {'amount': '2',
     'components': [{'amount': '2',
                     'comments': [],
                     'name': 'rødløk',
                     'recipe': 'TACOPARTY!'}],
     'name': 'rødløk'},
    {'amount': '1.81 dl',
     'components': [{'amount': '1 1/4 ts',
                     'comments': [],
                     'name': 'sennep',
                     'recipe': 'Chili con Carne'},
                    {'amount': '1 3/4 dl',
                     'comments': [],
                     'name': 'sennep',
                     'recipe': 'TACOPARTY!'}],
     'name': 'sennep'}]

RECIPECHOICE_COMBINATION_GROCERY_LIST_COMPONENTS = [
    {'amount': '1 7/8',
     'components': [{'amount': '1 7/8',
                     'comments': [],
                     'name': 'avokado',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'avokado'},
    {'amount': '4 bokser',
     'components': [{'amount': '4 bokser',
                     'comments': ['kidneybønner med chillisaus'],
                     'name': 'chillibønner',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0}],
     'name': 'chillibønner'},
    {'amount': '8 bokser',
     'components': [{'amount': '8 bokser',
                     'comments': [],
                     'name': 'hakket tomat',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0}],
     'name': 'hakket tomat'},
    {'amount': '2 3/8',
     'components': [{'amount': '2',
                     'comments': [],
                     'name': 'hjertesalat',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0},
                    {'amount': '3/8',
                     'comments': [],
                     'name': 'hjertesalat',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'hjertesalat'},
    {'amount': '1 hele',
     'components': [{'amount': '1 hele',
                     'comments': [],
                     'name': 'hvitløk',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0}],
     'name': 'hvitløk'},
    {'amount': '1 3/4 kg',
     'components': [{'amount': '1.60 kg',
                     'comments': [],
                     'name': 'kjøttdeig',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0},
                    {'amount': '150 g',
                     'comments': [],
                     'name': 'kjøttdeig',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'kjøttdeig'},
    {'amount': '11.42',
     'components': [{'amount': '6 2/3',
                     'comments': [],
                     'name': 'paprika',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0},
                    {'amount': '4',
                     'comments': [],
                     'name': 'paprika',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0},
                    {'amount': '3/4',
                     'comments': [],
                     'name': 'paprika',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'paprika'},
    {'amount': '150.00 g',
     'components': [{'amount': '150.00 g',
                     'comments': [],
                     'name': 'pulled pork',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'pulled pork'},
    {'amount': '1 1/2',
     'components': [{'amount': '1 1/2',
                     'comments': [],
                     'name': 'rødløk',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'rødløk'},
    {'amount': '1.56 dl',
     'components': [{'amount': '1/4 dl',
                     'comments': [],
                     'name': 'sennep',
                     'recipe': 'Chili con Carne',
                     'recipe_made_for': 4,
                     'recipe_multiplier': 2,
                     'recipe_scale': 4.0},
                    {'amount': '1.31 dl',
                     'comments': [],
                     'name': 'sennep',
                     'recipe': 'TACOPARTY!',
                     'recipe_made_for': 3,
                     'recipe_multiplier': 1,
                     'recipe_scale': 0.75}],
     'name': 'sennep'}]

SEARCH_STRING_RESULT_DICTIONARY = {
    'chili con carne': ['Chilli con Carne'],
    'fisk': ['Fiskeburgere',
             'Verdens beste fiskesuppe',
             'Lakselomper',
             'Tunfisksalat',
             'Fiskesuppe med kokos']
}

PLANNING_EXAMPLE = '''
    mandag: lakselomper x2
    tirsdag: fisk til 8
    onsdag: chili con carne til 6
    torsdag:
    fredag: nissefest

    3l melk
    200g medisterdeig
    1 pakke lomper
    1 kg karbonadedeig
    '''

PLANNING_RESULT_TYPES = [
    str,
    recipes.RecipeChoice,
    recipes.RecipeChoice,
    recipes.RecipeChoice,
    recipes.RecipeChoice,
    recipes.RecipeChoice,
    str,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    str,
]

CUPBOARD_GROCERIES = '''
    7.5 dl melk
    2 ounces medisterdeig
    2 laksefileter
    1/2 pakke lomper
    salt
    pepper
    salt og pepper
    mandag: lakselomper x2
    smør
    '''

CUPBOARD_RESULT_TYPES = [
    str,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    groceries.Ingredient,
    recipes.RecipeChoice,
    groceries.Ingredient,
    str,
]


def test_recipe_class():
    # Handle recipe dictionaries:
    recipe1 = recipes.Recipe(**RECIPE_EXAMPLE_1)
    recipe2 = recipes.Recipe(**RECIPE_EXAMPLE_2)

    combined_list = recipe1.ingredients + recipe2.ingredients

    # Checks scaling, combining and everything in one humungus assertion:
    assert combined_list.components() == RECIPE_COMBINATION_GROCERY_LIST_COMPONENTS


def test_RecipeChoice_class():
    recipe1 = recipes.Recipe(**RECIPE_EXAMPLE_1)
    recipe2 = recipes.Recipe(**RECIPE_EXAMPLE_2)

    recipeChoice1 = recipes.RecipeChoice(recipe1, plan_tag='monday', made_for=4, multiplier=2)
    recipeChoice2 = recipes.RecipeChoice(recipe2, plan_tag='Tuesday', made_for=3)

    combined_list = recipeChoice1.ingredients + recipeChoice2.ingredients

    # Checks scaling, combining and everything in one humungus assertion:
    assert combined_list.components() == RECIPECHOICE_COMBINATION_GROCERY_LIST_COMPONENTS

    # Check that contents of recipe1 have not changed:
    assert recipe1.ingredients.ingredients_formatted(sort='alphabetical') == RECIPE1_INGREDIENTS_FORMATED


def test_Cookbook_class():
    cookbook = recipes.Cookbook(cookbook_reader.recipes)  # cookbookcookbookcookbookcookbookcookbook

    # Tests various search patterns:
    assert isinstance(cookbook.find_recipe('fisk'), recipes.Recipe)

    for search in SEARCH_STRING_RESULT_DICTIONARY:
        assert cookbook.find_recipe(search).name in SEARCH_STRING_RESULT_DICTIONARY[search]
        if not cookbook.find_recipe(search):
            print(search)

    # Find blank recipe:
    assert isinstance(cookbook.find_recipe(''), recipes.Recipe)

    # Test menus:
    menu = cookbook.parse_menu(PLANNING_EXAMPLE)

    for item, instance in zip(menu.processed_lines, PLANNING_RESULT_TYPES):
        assert isinstance(item, instance)

    cupboard = cookbook.parse_menu(CUPBOARD_GROCERIES)

    for item, instance in zip(cupboard.processed_lines, CUPBOARD_RESULT_TYPES):
        assert isinstance(item, instance)


def test_Cookbook_recipe_search_with_grocery_list():
    cookbook = recipes.Cookbook(cookbook_reader.recipes)

    # Verify that any search using the ingredients of a recipe return that specific recipe:
    for recipe in cookbook.recipes.values():
        response = cookbook.find_recipe_with_groceries(recipe.ingredients, best=True, make_unavailable=False)
        assert recipe == response

    # Attempt to do a search for a specific recipe using a non-perfect grocery list to search:
    items = groceries.GroceryList(['300 g kjøttdeig', 'løk', 'avokado', 'mais'])

    fasit = cookbook.find_recipe('chili con carne', make_unavailable=False)
    response = cookbook.find_recipe_with_groceries(items, best=True, make_unavailable=False)
    assert fasit == response


def test_Cookbook_recipe_regular_search():
    cookbook = recipes.Cookbook(cookbook_reader.recipes)  # cookbookcookbookcookbookcookbookcookbook

    # Search for fish until fish is not available. What is returned?
    cookbook.when_choice_on_empty_selection_reset_available = False
    for number in range(100):
        recipe = cookbook.find_recipe('fisk')

        # Recipe is a recipe if recipe is found. When we reach the end of fisk-recipes
        # which are made unavailable after each successful search, return None.
        # Everything else is a fail.
        assert isinstance(recipe, recipes.Recipe) or recipe is None

    # Search for fish, with recipe reset when no fish is found.
    cookbook.when_choice_on_empty_selection_reset_available = True
    cookbook.reset_available_recipes()
    for number in range(100):
        recipe = cookbook.find_recipe('fisk')

        # Recipe is a recipe if recipe is found. When we reach the end of fisk-recipes
        # which are made unavailable after each successful search, return None.
        # Everything else is a fail.
        assert isinstance(recipe, recipes.Recipe)


def test_menu():

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

    menu = Menu(cookbook, '''Monday: mac cheese
    Tuesday: sweet
    Wednesday: pasta
    2 tbs coffee
    1 floz baked beans
    1 banana
    2 banana
    4 liters coffee''')

    assert menu.generate_processed_menu_str() == """Monday: Mac'n cheese for 2
Tuesday: Chocolate for 2
Wednesday: Carbonara for 2
0.30 dl coffee
0.30 dl baked beans
1 banana
2 banana
4 l coffee"""

    print(menu.groceries)

    print(menu.recipes)
