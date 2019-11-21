'''
-------------------------------------------------------------------------------
 Name:          groceries
 Purpose:       Module containing classes for handling Units,  Ingredients and
                lists of Ingredients.

 Author:        Tobias Litherland

 Created:       17.03.2015
 Copyright:     (c) Tobias Litherland 2015

-------------------------------------------------------------------------------
'''

import re
import copy
import numpy
from typing import Union, Tuple, List, TYPE_CHECKING

import tregex
from groceries.units import units, Unit

from groceries.configs.config_handler import config

if TYPE_CHECKING:
    from groceries import recipes


class IngredientComponent:
    """A class for a single ingredient component. Technically the same information
    as an Ingredient,  but contained in this class to simplify summing of
    several ingredients and keeping the origin of every single ingredient
    component when summarizing a chain of ingredients.

    An Ingredient does not have to be a litteral ingredient,  but can be
    absolutely anything the user needs to buy."""

    def __init__(self, ingredient_input: str, recipe: "recipes.Recipe" = None) -> None:
        """Constructor.

        Input:
            ingredient_input:   string representing an ingredient. Parsed for
                                amount,  unit,  ingredient name and comment (i.e.
                                "(cut to small pieces)" or ",  preferably Uncle
                                Bens").
            recipe:             recipe object where the ingredient component
                                came from. Used to track the amounts of
                                ingredients that come from where.
        """
        self.scale = 1  # Used to handle subtracted ingredients (in that case, scale = -1).
        self.recipe = recipe

        ingredient_string = self.process_input_string(ingredient_input)

        # Get the amount,  return the matched amount string and remove from ingredient_string.
        self.number, number_text = self._parse_amount(ingredient_string)
        ingredient_string = re.sub(number_text, '', ingredient_string, 1).strip()

        # Get the unit,  return the matched unit string and remove from ingredient_string.
        self.unit, self.unit_scale, unit_text = self._parse_unit(ingredient_string)
        ingredient_string = re.sub(unit_text, '', ingredient_string, 1).strip()

        # Get the comment(s),  return the matched comment string and remove from ingredient_string.
        self.comments, comment_match_string = self._parse_comments(ingredient_string)

        for k in comment_match_string:
            ingredient_string = re.sub(k, '', ingredient_string).strip()

        # What is left should be the name of the ingredient.
        self.name = ingredient_string
        self.original_string = ingredient_input

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return '<%s object: %s %s: %s>' % ('IngredientComponent', self.amount_formatted(), self.name, str(self.unit))

    @staticmethod
    def process_input_string(ingredient_input: str) -> str:
        """The input might contain some crazy unicode characters to represent
        fractions and other crazyness. Replace these."""

        ingredient_input = ingredient_input.strip()

        for fraction in config.constants.fractions:
            ingredient_input = re.sub(fraction, config.constants.fractions[fraction], ingredient_input)

        return ingredient_input

    @staticmethod
    def _parse_amount(ingredient_string: str) -> Tuple[numpy.array, str]:
        """Find the assumed amounts of a specific ingredient. If the ingredient
        is specified as a range (i.e. 2 - 2 1/2 ounces) the method will return
        all numbers present in the range ([2,  2.5]). If no amount is found,
        method returns None,  as an unspecified is something different than
        0 of something."""
        aprox_prefixes = '|'.join(config.language.aprox_prefixes)
        number_combo = '^(?:%s)?[ ]*%s(?:[ -]+%s)?(?(1)|(?!))' % (
            aprox_prefixes, config.constants.number_format, config.constants.number_format)
        all_amounts = []
        amount_text = ''

        # Purge named groups:
        # TODO: Fix this more elegantly.
        import re
        namedGroupDetection = r'(\(\?P<\w+>)'
        namedGroupReferenceDetection = r'\(\?\(\w+\)'
        number_combo2 = re.sub(namedGroupDetection, '(', number_combo)  # Remove named groups.
        number_combo2 = re.sub(namedGroupReferenceDetection, '(', number_combo2)  # Remove named groups.

        numbers = tregex.match(number_combo2, ingredient_string)

        if numbers:
            amount_text = numbers[0]
            amount_alternatives = tregex.to_dict(config.constants.number_format, amount_text)

            for a in amount_alternatives:
                amount = 0
                numerator = 0
                denominator = 1
                if a['amount']: amount = float(a['amount'].replace(',', '.'))
                if a['numerator']: numerator = float(a['numerator'])
                if a['denominator']: denominator = float(a['denominator'])

                all_amounts += [amount + numerator / denominator]

        # Convert array to numpy array,  for easier manipulation:
        all_amounts = numpy.array(all_amounts)

        return all_amounts, amount_text

    @staticmethod
    def _parse_unit(ing: str) -> Tuple[Unit, Union[float, int], str]:
        """Get the unit object of the ingredient."""
        unit_text = re.findall(r'^\w+', ing)
        if not unit_text:
            unit_text = ''
        else:
            unit_text = unit_text[0]

        unit, scale, text = units.match(unit_text)

        return unit, scale, text

    @staticmethod
    def _parse_comments(ing: str) -> Tuple[list, str]:
        """Get all individual comments from the ingredient and return them as a list."""

        comment_match_string = tregex.to_tuple(r'(\(.*?\)|, .*?$)', ing)
        if comment_match_string:
            comment_match_string = [re.escape(s[0]) for s in comment_match_string]
            comments = tregex.to_tuple(r'(?:(?<=\()|(?<=, ))(.+?)(?:(?=\))|(?=$))',
                                    ing)  # Comments without containers ( "([comment])" and ",  [comment]"
            comments = [s[0] for s in comments]
        else:
            comments = []

        return comments, comment_match_string  # TODO: Change in tregex now produces different output.

    def amount(self) -> numpy.array:
        """Return the normalized amount of the ingredient component."""

        if self.number.all():
            amount = self.number * self.scale * self.unit_scale
        else:
            amount = None  # No amount, different from zero.

        return amount

    def amount_formatted(self) -> str:
        return self.unit.amount_formatted(self.amount())

    def scale_ingredient_amount(self, scale: Union[int, float]) -> None:
        """Multiply all IngredientComponent amounts with the given scale.
        Primarily used to multiply all IngredientComponents with -1, so that
        the contents of one GroceryList can be subtracted from the contents of
        another GroceryList."""
        self.scale *= scale


class Ingredient:
    """Class for handling an ingredient. Returning unit,  summing of several units
    and plurals of units.
    An Ingredient consists of at least one IngredientComponent. If combining
    two ingredients with the same unit and name, the IngredientComponent lists
    are simply combined.

    An Ingredient does not have to be a literal ingredient, but can represent
    absolutely anything the user needs to buy."""

    def __init__(self, ingredient_input: Union[str, "Ingredient"], recipe: "recipes.Recipe" = None) -> None:

        if isinstance(ingredient_input, str):
            initial_ingredient = IngredientComponent(ingredient_input, recipe)
            self.components = [initial_ingredient]
        elif isinstance(ingredient_input, Ingredient):
            # If input is Ingredient, copy all components into this new Ingredient instance.
            # If not copy, the original Ingredient will be modified when we modify this ingredient.
            initial_ingredient = ingredient_input
            self.components = [copy.copy(component) for component in initial_ingredient.components]
        else:
            raise

        self.name = initial_ingredient.name
        self.unit = initial_ingredient.unit
        self.id = self.name + '_' + self.unit.dimension

    def __str__(self) -> str:
        return str(self.__repr__())

    def __repr__(self) -> str:
        return '<%s object: %s %s: %s>' % ('Ingredient', self.amount_formatted(), self.name, str(self.unit))

    def __eq__(self, other: "Ingredient") -> bool:
        """When comparing ingredients,  we only compare the name and the unit.
        We can then continue with combining the components of each ingredient."""
        return self.name == other.name and self.unit == other.unit

    def contains(self, other: "Ingredient", amount: bool = True,
                 aprox_name_limit: Union[float, int] = config.constants.ingredient_match_limit, verbose: bool = False) -> \
            Union[dict, bool]:
        """Check if one ingredient is a superset of another ingredient. Returns
        variants of (bool, bool) according to the different matches of name and
        amount."""

        output = {'result': False, 'amount': 0, 'name': 0}

        name_match = tregex.similarity(self.name, other.name)

        # Punish mismatch stricter if the word is short. Punishment is reduced to zero at 6 characters.
        name_length_punish_limit = 6

        min_name_length = min([len(self.name), len(other.name)])
        new_limit = aprox_name_limit + (1 - aprox_name_limit) * (name_length_punish_limit - min_name_length) / name_length_punish_limit
        limit = max(aprox_name_limit, new_limit)


        # average_length = (len(self.name) + len(other.name)) / 2
        # if average_length <= name_length_punish_limit:
        #     exponent = max([0, name_length_punish_limit - (len(self.name) + len(other.name)) / 2]) + 3
        #     name_match = name_match ** exponent

        output['name'] = name_match
        if name_match >= limit:
            if not amount or self.amount().size == 0 or other.amount().size == 0:
                output['amount'] = 1  # No specified amount means amount may be unimportant.
                output['result'] = True
            elif amount:
                # Calculate scores for amounts:
                self_amount = self.amount().max()
                other_amount = other.amount().max()

                if self.unit == other.unit:
                    if self_amount >= other_amount:
                        output['amount'] = 1  # Full score of other is less than self.
                        # amount = 0 if other more than self.
                        output['result'] = True
                else:
                    output['result'] = False
        if verbose:
            return output
        else:
            return output['result']

    def combine_with_ingredient(self, other: object) -> None:
        assert isinstance(other, Ingredient)

        if self == other:  # Ingredient equals compares names and units.
            self.components += other.components
        else:
            raise Exception('Attempt to combine non-comparable ingredients.')

    def amount(self) -> numpy.array:
        """Return the amount of this ingredient (the sum of the ingredient
        components). When the amount is zero, check the scales of the ingredients. If the amounts are zero, and a scale
        is negative, we assume that the negative weight comes from the user already having the ingredient."""

        # If the ingredient is not specified by an amount, return 0 if the sum of component
        # scales is 0
        amount = sum([component.amount() for component in self.components])
        if amount.size == 0:
            positive_scale_count = sum([1 for component in self.components if component.scale > 0])
            if positive_scale_count < len(self.components):
                # If one is a negative, then we assume that we have the ingredient.
                return numpy.array([0])
        return amount

    def amount_check(self) -> bool:
        if self.amount().size == 0:
            return False
        else:
            return True

    def amount_formatted(self) -> str:
        """Return a string representation of the ingredient amount."""
        return self.unit.amount_formatted(self.amount())

    def ingredient_formatted(self, pretty: bool = False, pretty_right_offset: int = 15,
                             include_comments: bool = False) -> str:
        """Return a string representation of the ingredient."""
        if self.amount_check():
            amount_unit = self.amount_formatted() + ' '
        else:
            amount_unit = ''

        if include_comments:
            comments = []
            for comp in self.components:
                comments += comp.comments

            comments = ', '.join(comments)
            if comments:
                comments = ', ' + comments
        else:
            comments = ''

        name = self.name
        if pretty:
            frame = '%%(amount_unit)%ds%%(name)s%%(comments)s' % pretty_right_offset
            string = frame % locals()
        else:
            string = '%(amount_unit)s%(name)s%(comments)s' % locals()

        return string

    def scale_ingredient_amount(self, scale: Union[float, int]):
        """Multiply all IngredientComponent amounts with the given scale.
        Primarily used to multiply all IngredientComponents with -1, so that
        the contents of one GroceryList can be subtracted from the contents of
        another GroceryList."""
        for i in range(len(self.components)):
            self.components[i].scale_ingredient_amount(scale)

    def dict(self) -> dict:
        """Return a more easily accessible dictionary of all the information in the Ingredient."""
        properties = {
            'name': self.name,
            'amount': self.amount_formatted(),
            'components': []
        }

        for ing in self.components:
            component_dict = {}
            if ing.recipe:
                component_dict['recipe'] = ing.recipe.name
                if hasattr(ing.recipe, 'made_for') and hasattr(ing.recipe, 'multiplier') and hasattr(ing.recipe,
                                                                                                     'scale'):
                    component_dict['recipe_made_for'] = ing.recipe.made_for
                    component_dict['recipe_multiplier'] = ing.recipe.multiplier
                    component_dict['recipe_scale'] = ing.recipe.scale
            else:
                component_dict['recipe'] = config.language.no_recipe_name

            component_dict['name'] = ing.name
            component_dict['amount'] = ing.amount_formatted()
            component_dict['comments'] = ing.comments

            properties['components'] += [component_dict]

        return properties

    def set_component_recipe(self, recipe: object):
        """Set the recipe property of all IngredientComponents in Ingredient."""
        for i in range(len(self.components)):
            self.components[i].recipe = recipe


IngredientInputType = Union[Ingredient, str]
IngredientOptionalSequenceInputType = Union[List[IngredientInputType], IngredientInputType]


class GroceryList:
    """Class for handling a list of Ingredients. Methods for combining lists,  and
    for collating the ingrediens by combining duplicates."""

    def __init__(self, ingredients: IngredientOptionalSequenceInputType = None, recipe: object = None):

        self.ingredient_list = []

        if ingredients:
            if isinstance(ingredients, str):
                ingredients = [ingredients]

            if isinstance(ingredients, list) and all(isinstance(ing, (str, Ingredient)) for ing in ingredients):
                self.add_ingredients(ingredients, recipe=recipe)
            elif isinstance(ingredients, GroceryList):
                self.add_ingredients(ingredients.ingredient_list, recipe=recipe)
            else:
                raise TypeError()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        ingredients = self.ingredients_formatted(sort='alphabetical', pretty=True)
        output = '<GroceryList object: %d ingredients\n%s\n>' % (len(ingredients), ',\n'.join(ingredients))
        return output

    def __add__(self, other: object) -> "GroceryList":
        assert isinstance(other, GroceryList)
        new_list = GroceryList(self._combine_lists(other.ingredient_list))
        return new_list

    def __iadd__(self, other: object) -> "GroceryList":
        assert isinstance(other, GroceryList)
        self.ingredient_list = self._combine_lists(other.ingredient_list)
        return self

    def __sub__(self, other: object) -> "GroceryList":
        assert isinstance(other, GroceryList)
        new_list = GroceryList(self._combine_lists(other.ingredient_list, subtract=True))
        return new_list

    def __isub__(self, other: object) -> "GroceryList":
        assert isinstance(other, GroceryList)
        self.ingredient_list = self._combine_lists(other.ingredient_list, subtract=True)
        return self

    def __mul__(self, number: Union[float, int]) -> "GroceryList":
        """Multiplication (left hand: GroceryList * x) of a GroceryList with an
        integer or a float."""
        assert isinstance(number, (int, float))
        # This is not in place multiply, so we need to copy the ingredients:
        ingredients = [Ingredient(ing) for ing in self.ingredient_list]
        for i in range(len(ingredients)):
            ingredients[i].scale_ingredient_amount(number)

        new_list = GroceryList(ingredients)
        return new_list

    def __rmul__(self, number: Union[float, int]) -> "GroceryList":
        """Multiplication (right hand: x * GroceryList) of a GroceryList with an
        integer or a float. Use same method as left hand multiplication."""
        return self.__mul__(number)

    def __imul__(self, number: Union[float, int]) -> "GroceryList":
        assert isinstance(number, (int, float))
        # This is in place multiply, so we modify ingredients directly.
        for i in range(len(self.ingredient_list)):
            self.ingredient_list[i].scale_ingredient_amount(number)
        return self

    def __contains__(self, other: object) -> bool:
        """Method called by the in-keyword."""
        if isinstance(other, str):
            other = Ingredient(other)
        return self.contains(other)['result']

    def ingredients_formatted(self, pretty: bool = False, sort: str = None, include_comments: bool = False) -> List[
        str]:
        """Return a list of string representations of each ingredient."""
        return [ing.ingredient_formatted(pretty=pretty, include_comments=include_comments) for ing in
                self.ingredients(sort)]

    def ingredients(self, sort: str = None, collate: bool = True) -> List[Ingredient]:
        """Return collated list of ingredients in GroceryList. CONSIDER REVISING
         FOR SPEED. Might be just as effective to solve the collation right
         away when adding the individual ingredients. Or maybe not."""

        if collate:
            ingredients = self.collate_ingredients()
        else:
            ingredients = self.ingredient_list

        if sort:
            if sort == 'alphabetical':
                ingredients.sort(key=lambda x: x.name)  # , reverse=baklengsSortering)
            elif sort == 'numerical':
                ingredients.sort(key=lambda x: x.name)  # Sort alphabetically first, for equal amounts.
                no_amount = [ing for ing in ingredients if not ing.amount_check()]
                amount = [ing for ing in ingredients if ing.amount_check()]
                amount.sort(key=lambda x: min(x.unit.scale_amount(x.amount())))  # , reverse=baklengsSortering)
                ingredients = no_amount + amount
            elif sort == 'other':
                # ADD CUSTOM CATEGORY SORT SO GROCERIES CAN BE SORTED IN STORE
                # TRAVERSE ORDER.
                pass

        return ingredients

    def collate_self(self) -> None:
        """Force a collation of all ingredients in self."""
        self.ingredient_list = self.collate_ingredients()

    def _combine_lists(self, ingredients: IngredientOptionalSequenceInputType, subtract: bool = False, recipe: object = None) -> List[object]:
        """Combine ingredients in list with the ingredients in the current
        instance of GroceryList. Return ingredient list."""
        ingredient_list = []

        if not isinstance(ingredients, list):
            ingredients = [ingredients]

        if all(isinstance(ing, Ingredient) for ing in ingredients) and subtract:
            # When subtracting, we modify the scale property of the ingredient
            # components. If the input is Ingredient objects, the original
            # ingredients will be modified. So we make copyies:
            ingredients = [Ingredient(ing, recipe) for ing in ingredients]
        elif all(isinstance(ing, str) for ing in ingredients):
            ingredients = [Ingredient(ing, recipe) for ing in ingredients]

        assert all(isinstance(ing, Ingredient) for ing in ingredients)

        if subtract:  # If subtracted, scale all Ingredient amounts with -1.
            for i in range(len(ingredients)):
                ingredients[i].scale_ingredient_amount(-1)

        ingredient_list += self.ingredient_list

        ingredient_list += ingredients

        return ingredient_list

    def add_ingredients(self, ingredients: IngredientOptionalSequenceInputType, recipe: "recipes.Recipe" = None) -> None:
        """Add ingredients as strings or Ingredient objects to the GroceryList.
        Input can aalso be a list. If subtract = True, all input ingredient
        amounts are scaled to -1 so they are subtracted from the Ingredient
        total."""
        ingredient_list = self._combine_lists(ingredients, recipe=recipe)
        self.ingredient_list = ingredient_list

    def subtract_ingredients(self, ingredients: IngredientOptionalSequenceInputType) -> None:
        """Subtract ingredients as strings from the GroceryList. Ingredients can
        be a single string or a list of strings. The subtracted string(s) will
        be parsed and added to the GroceryList with all amounts multiplied by
        -1."""
        ingredient_list = self._combine_lists(ingredients, subtract=True)
        self.ingredient_list = ingredient_list

    def collate_ingredients(self) -> list:
        """Collate a list of ingredients so that all ingredients with comparable
        unit and name are combined."""
        collated_dict = {}
        for ing in self.ingredient_list:
            if not ing.id in collated_dict:
                collated_dict[ing.id] = Ingredient(
                    ing)  # Create a new Ingredient object as a copy of the existing ingredient.
            else:
                collated_dict[ing.id].combine_with_ingredient(ing)

        # If any amounts in the collated list are reduced to zero, remove from list:
        collated_list = [ing for ing in collated_dict.values() if sum(ing.amount()) > 0 or not ing.amount_check()]

        return collated_list

    def components(self, sort: str = 'alphabetical', pretty: bool = False) -> list:
        """Return a list ingredient properties as ready formatted strings."""

        if not pretty:
            return [ing.dict() for ing in self.ingredients(sort)]
        else:
            raise Exception('This method is not done')

    def set_recipe(self, recipe: object) -> None:
        """Set the recipe property of each Ingredient to a specified Recipe-object."""
        for i in range(len(self.ingredient_list)):
            self.ingredient_list[i].set_component_recipe(recipe)

    def copy(self, in_place: bool = False) -> list:
        """Return a copy of this list, where all Ingredients are new instances."""
        new_ingredients = self.copy_ingredients()
        if in_place:
            self.ingredient_list = new_ingredients
        else:
            new_list = GroceryList(self.copy_ingredients())
            return new_list

    def copy_ingredients(self) -> list:
        """return a copy of this lists Ingredients, where all new Ingredients
        are new instances."""
        new_ingredients = [Ingredient(ing) for ing in self.ingredient_list]
        return new_ingredients

    def contains(self, ingredient: Ingredient, amount: bool = True, verbose: bool = False):
        """Check if an ingredient exists within the GroceryList. Returns
            (True, True) if name and amounts are present.
            (True, False) if name and not amount is present.
            (False, False) if name is not present."""

        # TODO: This method can't be finished. The output does not look complete.

        assert isinstance(ingredient, Ingredient)

        for ing in self.ingredients():
            match = ing.contains(ingredient, amount=amount, verbose=verbose)

            if verbose:
                if match['result']:
                    return match
            else:
                if match:
                    return match

        if verbose:
            return {'result': False, 'name': 0, 'amount': 0}
        else:
            False

    def compare_with(self, other: object, amount: bool = True, verbose: bool = False) -> Union[List[float], float]:
        """Compare the contents of one list with the contents of this list. If
        self is a superset of other (taking amounts into account) a score of 1
        is returned. For mismatches in amounts or names, reduce score."""

        # TODO: This method is probably not done either.

        assert isinstance(other, GroceryList)

        score_vector = []
        for other_ing in other.ingredients():
            match = self.contains(other_ing, amount=amount, verbose=True)
            score = min([match['name'] * 0.7 + match['amount'] * 0.3, 1])  # Cap at 100.

            score_vector += [(other_ing.name, score, match['result'], match['name'], match['amount'])]

        if verbose:
            return score_vector
        else:
            # Create an aggregate score based on the ingredients that have a match.
            score = sum([item[1] for item in score_vector if item[2]]) / len(score_vector)
            return score
