'''
-------------------------------------------------------------------------------
 Name:          recipe
 Purpose:       Module containing functions for handling recipes and cookbooks.

 Author:        Tobias Litherland

 Created:       17.03.2015
 Copyright:     (c) Tobias Litherland 2015
-------------------------------------------------------------------------------
'''

import re
import random
from typing import Union, List, Sequence, Tuple

import tregex
from groceries.groceries import GroceryList, Ingredient
from groceries.configs.config_handler import config


class Recipe:
    """Class for handling a recipe. A recipe has several properties and a list of
    ingredients.

    Recipe needs to differentiate between scaling to a number of people, and
    scaling by multiplication."""

    def __init__(self, name: str = '', tags: list = None, time: Union[float, int] = None,
                 serves: Union[float, int] = None, how_to: str = '', ingredients: list = None) -> None:
        if not tags:
            tags = []
        if not ingredients:
            ingredients = []
        self.name = name
        self.tags = tags
        self.time = time
        self.serves = serves
        self.how_to = how_to
        self.ingredients = GroceryList(ingredients, self)

    def __repr__(self) -> str:
        return '<Recipe object: %s>' % self.name


class RecipeChoice(Recipe):
    """Class for handling a specific recipe choice. A recipe choice has a
    specified amount of people it serves, and this is handled by the choice,
    and not by the actual recipe objects. Inherits properties from Recipe"""

    def __init__(self, recipe: Recipe = Recipe(), plan_tag: str = '', made_for: Union[float, int] = None,
                 multiplier: Union[float, int] = None) -> None:
        Recipe.__init__(self, **recipe.__dict__)
        self.plan_tag = plan_tag

        if not made_for and multiplier:
            self.made_for = self.serves
            self.multiplier = multiplier
        elif made_for and not multiplier:
            self.made_for = made_for
            self.multiplier = 1
        elif made_for and multiplier:
            self.made_for = made_for
            self.multiplier = multiplier
        else:
            self.made_for = config.constants.default_recipe_servings
            self.multiplier = 1

        if self.serves:
            self.scale = self.made_for / self.serves * self.multiplier
        else:
            self.scale = 1

        # Set Recipe choice property of all ingredients:
        # Copy ingredient object (de-link them from Recipe in cookbook).
        self.ingredients.copy(in_place=True)
        self.ingredients.set_recipe(self)

        self.ingredients *= self.scale  # In-place multiplication of GroceryList.

    def __str__(self) -> str:
        if self.plan_tag and not self.name:
            return '%s: %s' % (self.plan_tag, config.language.no_recipe)
        elif self.plan_tag and self.name and self.multiplier != 1:
            return '%s: %s x%d' % (self.plan_tag, self.name, self.multiplier)
        elif self.plan_tag and self.name and self.made_for:
            return '%s: %s %s %s' % (self.plan_tag, self.name, config.language.servings_prefix, self.made_for)
        if self.plan_tag and self.name:
            return '%s: %s' % (self.plan_tag, self.name)
        else:
            return 'Unknown formatting of recipe'

    def __repr__(self) -> str:
        if self.plan_tag and self.name:
            return '<RecipeChoice object: %s: %s>' % (self.plan_tag, self.name)
        elif self.plan_tag and not self.name:
            return '<RecipeChoice object: %s: %s>' % (self.plan_tag, config.language.no_recipe)
        else:
            return '<RecipeChoice object: %s>' % self.name


class RecipeConfigType:
    name: str
    tags: List[str]
    time: Union[float, int]
    how_to: str
    serves: Union[float, int]
    ingredients: List[str]

    def __init__(self, name: str,
                 tags: List[str],
                 time: Union[float, int],
                 how_to: str,
                 serves: Union[float, int],
                 ingredients: List[str]):
        """Class for defining the recipe information from a cookbook-configs."""
        self.name = name
        self.tags = tags
        self.time = time
        self.how_to = how_to
        self.serves = serves
        self.ingredients = ingredients


class Cookbook:
    """Class for handling a collection of Recipes. Contains search functions for
    the recipes contained within."""

    def __init__(self, recipes: Sequence[Recipe]) -> None:
        """the constructor only accepts a cookbook_dictionary already parsed
        the location where the cookbook should be stored."""
        self.recipes = {recipe.name: recipe for recipe in recipes}
        self.tags = []

        self.make_recipe_unavailable_after_search_match = True
        self.when_choice_on_empty_selection_reset_available = True

        self.available_recipes = []
        self.available_tags = dict()

        self.reset_available_recipes()  # Populate self.available_recipes and self.available_tags

        self.tags = [k for k in self.available_tags.keys()]

    def _create_tag_lookup(self) -> dict:
        tag_lookup = {}
        for recipe in self.recipes.values():
            for tag in recipe.tags:
                if tag not in tag_lookup:
                    tag_lookup[tag] = []
                tag_lookup[tag] += [recipe.name]

        return tag_lookup

    def find_recipe_with_groceries(self, grocery_list: GroceryList, best: bool = False,
                                   make_unavailable: list = None, verbose: bool = False) -> Union[list, None]:
        """Return a recipe from the cookbook using an existing grocery list."""

        candidates = []
        scores = []

        if make_unavailable is None:
            make_unavailable = self.make_recipe_unavailable

        for recipe in self.available_recipes:
            score_matrix = self.recipes[recipe].ingredients.compare_with(grocery_list, verbose=True)
            score = sum([score for name, score, check, name_score, amount_score in score_matrix]) / len(score_matrix)

            if score > 0:
                candidates += [(recipe, score, score_matrix)]
                scores += [score]

        results = [c for s, c in sorted(zip(scores, candidates))]

        if not results:
            return None
        else:
            if verbose:
                return results
            elif best:
                # Get the recipes with the highest score.
                selection = [r for r in results if r[1] == results[-1][1]]
            else:
                # Get the top 10% of candidates:
                index = min(max(int(len(results) / 10) + 1, 4), len(
                    results))  # Top 10%, rounded up, but not less than 4. Also, not ever more than length of results.
                selection = results[-index:]

            selected = random.choice(selection)
            output = self.recipes[selected[0]]

            if output and make_unavailable:
                self.make_recipe_unavailable(output)

            return output

    def find_recipe(self, search_string: str, make_unavailable: bool = None) -> Recipe:
        """Return a recipe from the cookbook using a search string."""

        fuzzy_match_limit = 0.8

        output = None

        if make_unavailable is None:
            make_unavailable = self.make_recipe_unavailable

        while True:
            # Blank input:
            if not search_string:
                if self.when_choice_on_empty_selection_reset_available:
                    if len(self.available_recipes) == 0:
                        self.reset_available_recipes()
                recipe_name = random.choice(self.available_recipes)
                output = self.recipes[recipe_name]
                break

            # If search_string is not empty, lowercase the string:
            search_string = search_string.lower()

            # Direct match for name:
            if not output:
                if search_string in self.recipes:
                    output = self.recipes[search_string]
                    break

            # Fuzzy name match (override self.available_recipes).
            # You get what you specifically ask for.
            if not output:
                for name in self.recipes:
                    ratio = tregex.similarity(search_string, name.lower())
                    if ratio >= fuzzy_match_limit:
                        output = self.recipes[name]
                        break

            # If no match yet found, assume tag and check for tags:
            if not output:
                if search_string in self.available_tags:
                    if self.when_choice_on_empty_selection_reset_available:
                        if len(self.available_tags[search_string]) == 0:
                            self.reset_available_recipes()
                    if len(self.available_tags[search_string]) == 0:
                        # No available recipes with tag.
                        pass
                    else:
                        recipe_name = random.choice(self.available_tags[search_string])
                        output = self.recipes[recipe_name]
                        break

            break

        if output and make_unavailable:
            self.make_recipe_unavailable(output)

        # Any other search type can be added to list or as a seperate method.

        # Used to have an ingredient search, but I removed it for the time beeing.

        # No matches for anything, return nothing:
        return output

    def make_recipe_unavailable(self, recipe: list = None) -> None:
        """Take a list of recipes as input, and set the selected recipes as
        unavailable for the search function. This avoids the same recipe being
        chosen the same time in the same plan. If not specified, this method
        is automatically run each time a search is performed, to make the chosen
        recipe unavailable."""

        if not recipe:
            recipe = []
        if not isinstance(recipe, list):
            recipe = [recipe]
        for rec in recipe:
            if rec.name in self.available_recipes:
                self.available_recipes.remove(rec.name)
                for t in rec.tags:
                    self.available_tags[t].remove(rec.name)

    def reset_available_recipes(self, unavailable_recipes: list = None) -> None:
        """Make all recipes available for search again."""
        self.available_recipes = list(self.recipes.keys())  # Recipe names.
        self.available_tags = self._create_tag_lookup()  # Tags and recipe names.

        # If the user has a list of recipes that still should be unavailable,
        # these can be passed as unavailable_recipes and are handled here:
        if unavailable_recipes:
            self.make_recipe_unavailable(unavailable_recipes)

    def match_ingredients(self, grocery_list: GroceryList, number_of_matches: int) -> None:
        """Take the contents of a GroceryList-object and find a number of
        the Recipes that match the ingredients. Pick randomly from the number of
        matches so multiple calls return different recipes."""
        # TODO: This method does nothing.
        pass

    def parse_menu(self, menu_text: str) -> object:
        """Return a menu object from the parsed text."""
        return Menu(self, menu_text)


class Menu(object):

    def __init__(self, cookbook: Cookbook, menu_text: str) -> None:
        """Class for handling a single menu. A Plan object handles two Menu objects
        in the form of a plan and a cupboard contents list (which is handled in
        the same way as a menu."""
        self.cookbook = cookbook
        self.recipes = []
        self.groceries = GroceryList()

        # String construction for Menu parsing:
        sep = r'\s*'  # General seperator
        start = r'^'
        tag_pattern = fr'(?P<plan_tag>{config.menu_format.tag_identifier})'
        recipe_pattern = fr'(?P<recipe>{config.menu_format.recipe_identifier})?'
        scaling_pattern = fr'(?:[x\*] ?(?P<multiplier>{config.menu_format.scaling_number_format})|{config.language.servings_prefix} (?P<made_for>{config.menu_format.scaling_number_format})|$)'

        self.menu_pattern = start + sep + sep.join([tag_pattern, config.menu_format.tag_separator, recipe_pattern, scaling_pattern]) + sep

        self.input_plan, self.input_lines, self.processed_lines, self.processed_plan = self.process_plan(menu_text)

        self.process_input()

    def process_input(self) -> None:
        self.recipes = [item for item in self.processed_lines if isinstance(item, RecipeChoice)]

        self.groceries = self.grocery_list(self.processed_lines)

    def __sub__(self, other: object) -> object:
        assert isinstance(other, Menu)
        return self.groceries - other.groceries

    def __isub__(self, other: object) -> None:
        assert isinstance(other, Menu)
        self.groceries -= other.groceries

    def process_plan(self, menu_text: str) -> Tuple:
        """Take a plan as a string, and parse the file according to a set of rules."""

        # Split into lines:
        input_plan = menu_text

        lines = menu_text.split('\n')
        input_lines = [line.strip() for line in lines]

        processed_lines = [self.process_line(line) for line in input_lines]
        processed_plan = self.create_output_lines(processed_lines)
        return input_plan, input_lines, processed_lines, processed_plan

    def process_line(self, line: str) -> Union[str, Ingredient, RecipeChoice]:

        line = re.sub(config.language.recipe_not_found_message, '', line)

        if not line:
            return line

        elif line[0] == config.constants.week_plan_comment_prefix:
            return line

        elif config.menu_format.tag_separator in line:
            match = tregex.to_dict(self.menu_pattern, line)[0]

            if match['recipe'] == '-':
                return RecipeChoice(plan_tag=match['plan_tag'])

            else:
                if match['multiplier']:
                    match['multiplier'] = float(match['multiplier'])
                if match['made_for']:
                    match['made_for'] = float(match['made_for'])

                recipe = self.cookbook.find_recipe(match['recipe'], make_unavailable=True)

                if recipe:
                    return RecipeChoice(recipe=recipe, plan_tag=match['plan_tag'], made_for=match['made_for'],
                                        multiplier=match['multiplier'])
                else:
                    return RecipeChoice(Recipe(name=config.language.recipe_not_found_message), plan_tag=match[
                        'plan_tag'])  # Blank recipe choice. Makes handling later easier as other methods don't fail.

        else:
            return Ingredient(line)

    @staticmethod
    def create_output_lines(lines: list) -> str:
        output_lines = []
        for line in lines:
            if isinstance(line, str):
                output_lines += [line]

            elif isinstance(line, RecipeChoice):
                tag = line.plan_tag
                recipe = line.name

                if not recipe:
                    output_lines += ['%s%s %s' % (tag, config.menu_format.tag_separator, config.language.no_recipe)]
                else:
                    if not line.multiplier == 1:
                        scale = 'x%0.1f' % line.multiplier
                    else:
                        scale = '%s %d' % (config.language.servings_prefix, line.made_for)
                    output_lines += ['%s%s %s %s' % (tag, config.menu_format.tag_separator, recipe, scale)]

            elif isinstance(line, Ingredient):
                output_lines += [line.ingredient_formatted()]

        output = '\n'.join(output_lines)

        return output

    @staticmethod
    def grocery_list(processed_lines: list) -> GroceryList:
        # Combine the groceries of all recipes and loose ingredients.
        grocery_total = GroceryList()
        for line in processed_lines:
            if isinstance(line, RecipeChoice):
                grocery_total += line.ingredients
            elif isinstance(line, Ingredient):
                grocery_total.add_ingredients(line)

        return grocery_total

    def generate_menu_str(self) -> str:
        '''Create a text based on the contents of the menu'''
        newline = '\n'
        text = ''
        for item in self.processed_lines:
            if isinstance(item, str):
                text += item + newline
            elif isinstance(item, RecipeChoice):
                text += '== %s ==%s' % (str(item), newline)
                if item.name:
                    text += item.how_to + newline
                    for ing in item.ingredients.ingredients_formatted(sort='alphabetical', pretty=True,
                                                                      include_comments=True):
                        text += ing + newline

        return text

    def generate_processed_menu_str(self) -> str:
        """Create a string representation of the processed menu."""
        return self.create_output_lines(self.processed_lines)
