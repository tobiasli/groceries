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
import unittest
import numpy

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


class TestGroceriesModule(unittest.TestCase):
    def test_IngredientComponent_class(self):
        from groceryshopping import groceries
        # Class for testing the parsing of ingredients.
        ingredients = []
        for example in INGREDIENT_PARSING_EXAMPLES:
            ingredients += [groceries.IngredientComponent(example)]

        for i, ing in enumerate(ingredients):
            self.assertTrue(numpy.all(ing.amount() == INGREDIENTS_EXAMPLES_CORRECT_RESULTS[i][0]))
            self.assertTrue(ing.unit.dimension == INGREDIENTS_EXAMPLES_CORRECT_RESULTS[i][1])
            self.assertTrue(ing.amount_formatted() == INGREDIENTS_EXAMPLES_CORRECT_RESULTS[i][2])
            self.assertTrue(ing.name == INGREDIENTS_EXAMPLES_CORRECT_RESULTS[i][3])
            self.assertTrue(ing.comments == INGREDIENTS_EXAMPLES_CORRECT_RESULTS[i][4])

    def test_Ingredient_class(self):
        from groceryshopping import groceries
        INGREDIENT_PARSING_EXAMPLES = [
            u'ca. 1/2 rød chili,  finhakket',
            u'1 rød chili (uten frø)',
            u'2/3 løk',
            u'ca. 1 1/2 teskjeer soyasaus',
            u'10 ts soyasaus',
            u'4 bananer',
            u'olivenolje'
        ]

        ingredient_result = [
            u'2/3 l\xf8k',
            u'1 1/2 rød chili',
            u'0.57 dl soyasaus',
            u'4 bananer',
            u'olivenolje'
        ]

        # Which of the above ingredienst should combine with each other.
        combination_true_indexes = {0: [0, 1], 1: [0, 1], 2: [2], 3: [3, 4], 4: [3, 4]}

        ingredients = []
        for example in INGREDIENT_PARSING_EXAMPLES:
            ingredients += [groceries.Ingredient(example)]

        # Check ability to compare objects.
        self.assertTrue(ingredients[0] == ingredients[1])
        self.assertFalse(ingredients[1] == ingredients[2])
        self.assertFalse(ingredients[2] == ingredients[3])
        self.assertTrue(ingredients[3] == ingredients[4])

        # Check ability to combine objects.
        combine_list = {}
        for ing, m in zip(ingredients, range(len(ingredients))):
            if not ing.id in combine_list:
                combine_list[ing.id] = ing
            else:
                combine_list[ing.id].combine_with_ingredient(ing)

        # Check output from component dictionary return:
        for ing in combine_list.values():
            self.assertTrue(ing.ingredient_formatted() in ingredient_result)

    def test_Ingredient_contains_method(self):
        from groceryshopping.groceries import Ingredient
        superset = Ingredient('100 g rød chili')
        subset = Ingredient('50 g rød chili')
        too_much = Ingredient('150 g rød chili')
        close_match = Ingredient('50 g rød chilli')

        fuzzy_limit = 80

        self.assertTrue(superset.contains(subset, aprox_name_limit=100))
        self.assertTrue(superset.contains(superset, aprox_name_limit=100))
        self.assertFalse(superset.contains(too_much, aprox_name_limit=100))
        self.assertTrue(superset.contains(too_much, amount=False, aprox_name_limit=100))

        self.assertFalse(superset.contains(close_match, aprox_name_limit=100))
        self.assertTrue(superset.contains(close_match, aprox_name_limit=fuzzy_limit))

        no_amount_superset = Ingredient('paprikapotetgull')
        no_amount_subset_close_match = Ingredient('paprikepotetgull')
        no_amount_subset_not_close = Ingredient('poprika pottegul')
        no_amount_subset_mismtch = Ingredient('nisse')

        self.assertTrue(no_amount_superset.contains(no_amount_superset))
        self.assertTrue(no_amount_superset.contains(no_amount_subset_close_match, aprox_name_limit=fuzzy_limit))
        self.assertFalse(no_amount_superset.contains(no_amount_subset_close_match, aprox_name_limit=100))
        self.assertTrue(no_amount_superset.contains(no_amount_subset_not_close, aprox_name_limit=fuzzy_limit))
        self.assertFalse(no_amount_superset.contains(no_amount_subset_not_close, aprox_name_limit=90))
        self.assertFalse(no_amount_superset.contains(no_amount_subset_mismtch, aprox_name_limit=fuzzy_limit))

    def test_GroceryList_class(self):
        from groceryshopping import groceries
        ingredient_result_numeric_sort = [0, 1, 2, 3]
        ingredient_result_alphabetic_sort = [0, 1, 2, 3]

        grocery_list = groceries.GroceryList()

        grocery_list.add_ingredients(INGREDIENT_PARSING_EXAMPLES)

        # Test numerical sort and formatting.
        self.assertTrue(grocery_list.ingredients_formatted(sort='numerical') == INGREDIENT_RESULT_PRE_COMBINE_NUMERICAL)

        # Test grocery list addition:
        grocery_list2 = groceries.GroceryList()
        grocery_list2.add_ingredients(u'tyttebær')
        grocery_list2.add_ingredients(u'10 m skolisser')
        grocery_list2.add_ingredients(u'5 cm skolisser')

        grocery_list += grocery_list2

        # Test sorting and formatting after addition:
        self.assertTrue(grocery_list.ingredients_formatted(sort='alphabetical') == INGREDIENT_RESULT_ALPHABETICAL)
        self.assertTrue(grocery_list.ingredients_formatted(sort='numerical') == INGREDIENT_RESULT_NUMERICAL)
        #self.assertTrue(grocery_list.ingredients_formatted(sort='categorical') == INGREDIENT_RESULT_CATEGORICAL)

        # Test ingredient subtraction:
        new_list = groceries.GroceryList()
        new_list.add_ingredients(['2 kg bøtte', 'snørr'])
        new_list.subtract_ingredients('200 g bøtte')
        new_list.subtract_ingredients('18 hg bøtte')

        self.assertTrue(new_list.ingredients_formatted() == ['snørr'])
        new_list.subtract_ingredients('snørr')

        self.assertTrue(new_list.ingredients_formatted() == [])  # List should now be empty.

        # Need groceries, and have some allready in the cupboard, what do i have to buy:
        shopping_list = groceries.GroceryList(INGREDIENT_PARSING_EXAMPLES)
        cupboard_list = groceries.GroceryList(INGREDIENTS_IN_CUPBOARD)

        what_to_buy = shopping_list - cupboard_list

        self.assertTrue(what_to_buy.ingredients_formatted(sort='alphabetical') == INGREDIENTS_AFTER_CUPBOARD_REMOVAL)
        # Make sure cupboard-contents is not modified in process:
        self.assertTrue(
            cupboard_list.ingredients_formatted(sort='alphabetical') == INGREDIENTS_IN_CUPBOARD_FORMATED_ALPHABETICAL)

        # Test multiplication (regular and in-place):
        multiplication = what_to_buy * 2
        self.assertTrue(multiplication.ingredients_formatted(sort='alphabetical') == GROCERYLIST_MULTIPLICATION_TEST)
        what_to_buy *= 2
        self.assertTrue(what_to_buy.ingredients_formatted(sort='alphabetical') == GROCERYLIST_MULTIPLICATION_TEST)

        # Test multiple addition/subtraction with no amount:
        simple1 = groceries.GroceryList(['salt og pepper', 'salt'])
        simple2 = groceries.GroceryList('salt og pepper', 'nisse')

        result1 = simple1 + simple1 + simple1
        result2 = result1 - simple2

        self.assertTrue(result2.ingredients_formatted() == ['salt'])

    def test_GroceryList_contains_method(self):
        from groceryshopping.groceries import GroceryList, Ingredient
        superset = ['50-100g smør', 'salt', 'chili', '1 ts kanel', '10 ounces sukker']
        superset_list = GroceryList(superset)

        for item in superset:
            self.assertTrue(superset_list.contains(Ingredient(item)))

        not_contains = ['salat', 'senep', 'brød', 'suketter']

        for item in not_contains:
            try:
                self.assertFalse(superset_list.contains(Ingredient(item)))
            except:
                self.assertFalse(superset_list.contains(Ingredient(item)))

        contains_without_amount = ['200 g smør', '1 oz kanel', '100 tonn sukker']

        for item in contains_without_amount:
            self.assertFalse(superset_list.contains(Ingredient(item)))
            self.assertTrue(superset_list.contains(Ingredient(item), amount=False))

    def test_GroceryList_compare_with_method(self):
        from groceryshopping.groceries import GroceryList

        superset = ['50-100g smør', 'salt', 'chili', '1 ts kanel', '10 ounces sukker']
        subset = ['0.05 kg smør', 'salt', 'chili', '3/4 teskje kanel']
        subset_mismatch = ['0.05 kg smør', 'salat', 'chilli', 'kanel']
        no_match = ['nisse', '1 kg troll', 'esel']

        superset_list = GroceryList(superset)

        from groceryshopping.groceries import Ingredient

        Ingredient('1 ts kanel').contains(Ingredient('kanel'))

        self.assertTrue(superset_list.compare_with(GroceryList(subset)) == 100)
        self.assertTrue(70 <= superset_list.compare_with(GroceryList(subset_mismatch)) <= 80)
        self.assertTrue(superset_list.compare_with(GroceryList(no_match)) == 0)
