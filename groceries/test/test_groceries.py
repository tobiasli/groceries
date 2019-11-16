# -------------------------------------------------------------------------------
# Name:        GroceryShopping_Test_Suite
# Purpose:      Test the components of the groceries class.
#
# Author:      Tobias
#
# Created:     01.05.2015
# Copyright:   (c) Tobias 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import pytest
import numpy

from groceries import groceries

INGREDIENT_PARSING_EXAMPLES = [
    u'ca. 1/2 gram safran, finhakket',
    u'10-12 g safran (eller 1/2 kyllingbuljongterning)',
    u'2/3 løk',
    u'ca. 1 1/2 teskjeer soyasaus',
    u'10 ts soyasaus, eller annen salt væske',
    u'2,45kg smør',
    u'50-100 g smør',
    u'bananer',
    u'1 pakke spaghetti',
    u'2 pakker spaghetti',
]

INGREDIENTS_EXAMPLES_CORRECT_RESULTS = [  # amount, dimension, quantity,  grocery,  [comments]
    [numpy.array([0.5]), u'mass', '1/2 g', u'safran', [u'finhakket']],
    [numpy.array([10, 12]), u'mass', '10 - 12 g', u'safran', [u'eller 1/2 kyllingbuljongterning']],
    [numpy.array([2 / 3]), u'none', '2/3', u'løk', []],
    [numpy.array([0.0075]), u'volume', '1 1/2 ts', u'soyasaus', []],
    [numpy.array([0.05]), u'volume', '1/2 dl', u'soyasaus', [u'eller annen salt væske']],
    [numpy.array([2450]), u'mass', u'2.45 kg', 'smør', []],
    [numpy.array([50, 100]), u'mass', u'50 - 100 g', 'smør', []],
    [numpy.array([]), u'none', '', u'bananer', []],
    [numpy.array([1]), u'other_pakke', '1 pakke', u'spaghetti', []],
    [numpy.array([2]), u'other_pakke', '2 pakker', u'spaghetti', []],
]

INGREDIENT_CASES = [
    ['ca. 1/2 gram safran, finhakket', numpy.array([0.5]), 'mass', '1/2 g', 'safran', ['finhakket']],
    ['10-12 g safran (eller 1/2 kyllingbuljongterning)', numpy.array([10, 12]), 'mass', '10 - 12 g', 'safran',
     ['eller 1/2 kyllingbuljongterning']],
    ['2/3 løk', numpy.array([2 / 3]), 'none', '2/3', 'løk', []],
    ['ca. 1 1/2 teskjeer soyasaus', numpy.array([0.0075]), 'volume', '1 1/2 ts', 'soyasaus', []],
    ['10 ts soyasaus, eller annen salt væske', numpy.array([0.05]), 'volume', '1/2 dl', 'soyasaus',
     ['eller annen salt væske']],
    ['2,45kg smør', numpy.array([2450]), 'mass', '2.45 kg', 'smør', []],
    ['50-100 g smør', numpy.array([50, 100]), 'mass', '50 - 100 g', 'smør', []],
    ['bananer', numpy.array([]), 'none', '', 'bananer', []],
    ['1 pakke spaghetti', numpy.array([1]), 'other_pakke', '1 pakke', 'spaghetti', []],
    ['2 pakker spaghetti', numpy.array([2]), 'other_pakke', '2 pakker', 'spaghetti', []],
]

INGREDIENT_RESULT_PRE_COMBINE_NUMERICAL = [
    u'bananer',
    u'0.57 dl soyasaus',
    u'2/3 l\xf8k',
    u'2 1/2 - 2.55 kg sm\xf8r',
    u'3 pakker spaghetti',
    u'10 1/2 - 12 1/2 g safran',
]

INGREDIENT_RESULT_ALPHABETICAL = [
    u'bananer',
    u'2/3 l\xf8k',
    u'10 1/2 - 12 1/2 g safran',
    u'10.05 m skolisser',
    u'2 1/2 - 2.55 kg sm\xf8r',
    u'0.57 dl soyasaus',
    u'3 pakker spaghetti',
    u'tyttebær',
]

INGREDIENT_RESULT_NUMERICAL = [
    u'bananer',
    u'tyttebær',
    u'0.57 dl soyasaus',
    u'2/3 l\xf8k',
    u'2 1/2 - 2.55 kg sm\xf8r',
    u'3 pakker spaghetti',
    u'10.05 m skolisser',
    u'10 1/2 - 12 1/2 g safran',
]

# CATEGORICAL_ORDER = ['frukt og grønt']
# INGREDIENT_RESULT_CATEGORICAL

INGREDIENTS_IN_CUPBOARD = [
    'bananer',
    '1 løk',
    '250 deg smør',
    '2 pakker spaghetti',
]

INGREDIENTS_IN_CUPBOARD_FORMATED_ALPHABETICAL = [
    'bananer',
    '1 løk',
    '2 1/2 kg smør',
    '2 pakker spaghetti',
]

INGREDIENTS_AFTER_CUPBOARD_REMOVAL = [
    '10 1/2 - 12 1/2 g safran',
    '0 - 50 g smør',
    '0.57 dl soyasaus',
    '1 pakke spaghetti',
]

GROCERYLIST_MULTIPLICATION_TEST = [
    '21 - 25 g safran',
    '0 - 100 g smør',
    '1.15 dl soyasaus',
    '2 pakker spaghetti',
]


@pytest.mark.parametrize('candidate,amount,dimension,amount_str,unit_str,comments', INGREDIENT_CASES)
def test_ingredient_component_matching(candidate, amount, dimension, amount_str, unit_str, comments):
    ing = groceries.IngredientComponent(candidate)

    assert numpy.all(ing.amount() == amount)
    assert ing.unit.dimension == dimension
    assert ing.amount_formatted() == amount_str
    assert ing.name == unit_str
    assert ing.comments == comments


def test_ingredient():
    candidate_list = [
        u'ca. 1/2 rød chili,  finhakket',
        u'1 rød chili (uten frø)',
        u'2/3 løk',
        u'ca. 1 1/2 teskjeer soyasaus',
        u'10 ts soyasaus',
        u'4 bananer',
        u'olivenolje'
    ]

    expected_list = [
        u'2/3 l\xf8k',
        u'1 1/2 rød chili',
        u'0.57 dl soyasaus',
        u'4 bananer',
        u'olivenolje'
    ]

    # Which of the above ingredienst should combine with each other.
    combination_true_indexes = [(0, 1), (0, 1), (2,), (3, 4), (3, 4)]

    ingredients = []
    for example in candidate_list:
        ingredients += [groceries.Ingredient(example)]

    # Check ability to compare objects.
    for indexes in combination_true_indexes:
        if len(indexes) > 1:
            assert ingredients[indexes[0]] == ingredients[indexes[1]]

    # Check ability to combine objects.
    combine_list = {}
    for ing, m in zip(ingredients, range(len(ingredients))):
        if not ing.id in combine_list:
            combine_list[ing.id] = ing
        else:
            combine_list[ing.id].combine_with_ingredient(ing)

    # Check output from component dictionary return:
    for ing in combine_list.values():
        assert ing.ingredient_formatted() in expected_list


def test_ingredient_contains():
    superset = groceries.Ingredient('100 g rød chili')
    subset = groceries.Ingredient('50 g rød chili')
    too_much = groceries.Ingredient('150 g rød chili')
    close_match = groceries.Ingredient('50 g rød chilli')

    fuzzy_limit = 80

    assert superset.contains(subset, aprox_name_limit=100)
    assert superset.contains(superset, aprox_name_limit=100)
    assert not superset.contains(too_much, aprox_name_limit=100)
    assert superset.contains(too_much, amount=False, aprox_name_limit=100)  # Test amount flag for contains.

    assert not superset.contains(close_match, aprox_name_limit=100)
    assert superset.contains(close_match, aprox_name_limit=fuzzy_limit)

    no_amount_superset = groceries.Ingredient('paprikapotetgull')
    no_amount_subset_close_match = groceries.Ingredient('paprikepotetgull')
    no_amount_subset_not_close = groceries.Ingredient('poprika pottegul')
    no_amount_subset_mismatch = groceries.Ingredient('nisse')

    assert no_amount_superset.contains(no_amount_superset)
    assert no_amount_superset.contains(no_amount_subset_close_match, aprox_name_limit=fuzzy_limit)
    assert not no_amount_superset.contains(no_amount_subset_close_match, aprox_name_limit=100)
    assert no_amount_superset.contains(no_amount_subset_not_close, aprox_name_limit=fuzzy_limit)
    assert not no_amount_superset.contains(no_amount_subset_not_close, aprox_name_limit=90)
    assert not no_amount_superset.contains(no_amount_subset_mismatch, aprox_name_limit=fuzzy_limit)


def test_grocerylist():
    ingredient_result_numeric_sort = [0, 1, 2, 3]
    ingredient_result_alphabetic_sort = [0, 1, 2, 3]

    grocery_list = groceries.GroceryList()

    grocery_list.add_ingredients(INGREDIENT_PARSING_EXAMPLES)

    # Test numerical sort and formatting.
    assert grocery_list.ingredients_formatted(sort='numerical') == INGREDIENT_RESULT_PRE_COMBINE_NUMERICAL

    # Test grocery list addition:
    grocery_list2 = groceries.GroceryList()
    grocery_list2.add_ingredients(u'tyttebær')
    grocery_list2.add_ingredients(u'10 m skolisser')
    grocery_list2.add_ingredients(u'5 cm skolisser')

    grocery_list += grocery_list2

    # Test sorting and formatting after addition:
    assert grocery_list.ingredients_formatted(sort='alphabetical') == INGREDIENT_RESULT_ALPHABETICAL
    assert grocery_list.ingredients_formatted(sort='numerical') == INGREDIENT_RESULT_NUMERICAL
    # assert grocery_list.ingredients_formatted(sort='categorical') == INGREDIENT_RESULT_CATEGORICAL

    # Test ingredient subtraction:
    new_list = groceries.GroceryList()
    new_list.add_ingredients(['2 kg bøtte', 'snørr'])
    new_list.subtract_ingredients('200 g bøtte')
    new_list.subtract_ingredients('18 hg bøtte')

    assert new_list.ingredients_formatted() == ['snørr']
    new_list.subtract_ingredients('snørr')

    assert new_list.ingredients_formatted() == []  # List should now be empty.

    # Need groceries, and have some allready in the cupboard, what do i have to buy:
    shopping_list = groceries.GroceryList(INGREDIENT_PARSING_EXAMPLES)
    cupboard_list = groceries.GroceryList(INGREDIENTS_IN_CUPBOARD)

    what_to_buy = shopping_list - cupboard_list

    assert what_to_buy.ingredients_formatted(sort='alphabetical') == INGREDIENTS_AFTER_CUPBOARD_REMOVAL
    # Make sure cupboard-contents is not modified in process:
    assert cupboard_list.ingredients_formatted(sort='alphabetical') == INGREDIENTS_IN_CUPBOARD_FORMATED_ALPHABETICAL

    # Test multiplication (regular and in-place):
    multiplication = what_to_buy * 2
    assert multiplication.ingredients_formatted(sort='alphabetical') == GROCERYLIST_MULTIPLICATION_TEST
    what_to_buy *= 2
    assert what_to_buy.ingredients_formatted(sort='alphabetical') == GROCERYLIST_MULTIPLICATION_TEST

    # Test multiple addition/subtraction with no amount:
    simple1 = groceries.GroceryList(['salt og pepper', 'salt'])
    simple2 = groceries.GroceryList('salt og pepper', 'nisse')

    result1 = simple1 + simple1 + simple1
    result2 = result1 - simple2

    assert result2.ingredients_formatted() == ['salt']


def test_grocerylist_contains():
    superset = ['50-100g smør', 'salt', 'chili', '1 ts kanel', '10 ounces sukker']
    superset_list = groceries.GroceryList(superset)

    for item in superset:
        assert superset_list.contains(groceries.Ingredient(item))

    not_contains = ['salat', 'senep', 'brød', 'suketter']

    for item in not_contains:
        assert not superset_list.contains(groceries.Ingredient(item))

    contains_without_amount = ['200 g smør', '1 oz kanel', '100 tonn sukker']

    for item in contains_without_amount:
        assert not superset_list.contains(groceries.Ingredient(item))
        assert superset_list.contains(groceries.Ingredient(item), amount=False)


def test_grocerylist_compare_with():
    superset = ['50-100g smør', 'salt', 'chili', '1 ts kanel', '10 ounces sukker']
    subset = ['0.05 kg smør', 'salt', 'chili', '3/4 teskje kanel']
    subset_mismatch = ['0.05 kg smør', 'salat', 'chilli', 'kanel']
    no_match = ['nisse', '1 kg troll', 'esel']

    superset_list = groceries.GroceryList(superset)

    groceries.Ingredient('1 ts kanel').contains(groceries.Ingredient('kanel'))

    assert superset_list.compare_with(groceries.GroceryList(subset)) == 100
    assert 70 <= superset_list.compare_with(groceries.GroceryList(subset_mismatch)) <= 80
    assert superset_list.compare_with(groceries.GroceryList(no_match)) == 0
