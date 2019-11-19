"""Classes for containing various config information."""
import typing as ty
import types as tys
import abc
import re


Number = ty.Union[float, int]


class ConfigBase(metaclass=abc.ABCMeta):
    """Base class for all config types."""
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of he current config."""


class Settings(ConfigBase):
    name = 'settings'

    def __init__(self,
                 unit_formatting_variant: str,
                 small_fractions: bool
                 ) -> None:
        """
        :param unit_formatting_variant: Name of the unit formatting rule you choose to use. Can be either 'metric_impterial' or 'metric'.
        :param small_fractions: Choose to use either large fractions (1/2) or small fractions (unicode fractions chars).
        """
        self.small_fractions = small_fractions
        self.unit_formatting_variant = unit_formatting_variant


class Language(ConfigBase):
    name = 'language'

    def __init__(self,
                 aprox_prefixes: ty.List[str],
                 no_recipe_name: str,
                 servings_prefix: str,
                 recipe_not_found_message: str,
                 no_recipe: str
                 ):
        """
        Class containing all config properties pertaining to Language options in the application.

        :param aprox_prefixes: Prefixes used to denote approximate amounts in Ingredients.
        :param no_recipe_name: Category used to group Ingredients in a shopping list that do not come from a specific
                               Recipe.
        :param servings_prefix: When mentioning servings in text, what is the typical prefix for the number of servings.
                                If the Recipe serves 2, the prefix is "serves" would make it "serves 2".
        :param recipe_not_found_message: When parsing a menu, if a recipe is not found when looking for a recipe, this
                                         is the message that is displayed for the user.
        :param no_recipe: String that is used to identify tags without a recipe. Tags can be left open in a menu,
                          denoting that we don't need anything specific for a given day.
        """
        self.aprox_prefixes = aprox_prefixes
        self.no_recipe_name = no_recipe_name
        self.servings_prefix = servings_prefix
        self.recipe_not_found_message = re.escape(recipe_not_found_message)
        self.no_recipe = no_recipe


class Constants(ConfigBase):
    name = 'constants'

    def __init__(self,
                 number_format: str,
                 intuitive_denominators: ty.List[int],
                 fractions: ty.Dict[str, str],
                 default_recipe_servings: int,
                 ingredient_match_limit: float,
                 week_plan_comment_prefix: str,
                 ) -> None:
        """
        Class containing all constants used in various places around the groceries module.
        :param number_format: This is a complex regex pattern identifying all kinds of numbers.
        :param intuitive_denominators: A list of denominators that are in reasonable use when cooking food.
        :param fractions: A lookup table between unicode small fractions and regular ascii fractions.
        :param default_recipe_servings: The default amount of servings if not specified for a Recipe.
        :param ingredient_match_limit: The difflib.Sequence score lower limit for matching similar ingredients.
        :param week_plan_comment_prefix: Which prefix to use when parsing for comments in a menu.
        """
        self.number_format = number_format
        self.intuitive_denominators = intuitive_denominators
        self.fractions = fractions
        self.fractions_inverse = {v: k for k, v in self.fractions.items()}
        self.default_recipe_servings = default_recipe_servings
        self.ingredient_match_limit = ingredient_match_limit
        self.week_plan_comment_prefix = week_plan_comment_prefix


class MenuFormat(ConfigBase):
    name = 'menu_format'

    def __init__(self,
                 scaling_number_format: str,
                 tag_identifier: str,
                 tag_separator: str,
                 recipe_identifier: str,
                 ) -> None:
        """
        Config container for all rules regarding pattern recognition in menus:
        tag: recipe
        tag2: recipe2

        ingredient1
        ingredient2

        etc
        :param scaling_number_format: Number formatting for scaling recipes.
        :param tag_identifier: Pattern to recognize recipe tags.
        :param tag_separator: The separator between tags and recipes.
        :param recipe_identifier: Pattern to recognize recipe names.
        """
        self.scaling_number_format = scaling_number_format
        self.tag_identifier = tag_identifier
        self.tag_separator = tag_separator
        self.recipe_identifier = recipe_identifier


class UnitDefinition(ConfigBase):
    name = 'unit_definition'

    def __init__(self,
                 units: ty.Dict[str, ty.Dict[str, ty.Union[Number, str, ty.List[str], ty.Dict[str, Number]]]],
                 formatting: ty.Dict[str, ty.List[ty.Dict[str, ty.Union[str, ty.Callable[[Number], bool]]]]],
                 constants: tys.ModuleType,
                 ) -> None:
        """
        Container for a all rules regarding units for the groceries package.
        :param units: Dictionary containing information on all available units.
        :param formatting: Dictionary keyed on dimension. Each dimension contains a unit name and a set of criteria for
                           when this specific unit should be used when formatting an Ingredient.
        :param constants: Constants used for unit representation.
        """
        self.constants = constants
        self.formatting = formatting
        self.units = units
