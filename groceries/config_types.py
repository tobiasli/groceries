"""Classes for containing various config information."""
import typing as ty

Number = ty.Union[float, int]


class Settings:
    def __init__(self,
                 unit_formatting_variant: str ='metric_imperial',
                 small_fractions: bool = False
                 ) -> None:
        """
        :param unit_formatting_variant: Name of the unit formatting rule you choose to use. Can be either 'metric_impterial' or 'metric'.
        :param small_fractions: Choose to use either large fractions (1/2) or small fractions (unicode fractions chars).
        """
        self.small_fractions = small_fractions
        self.unit_formatting_variant = unit_formatting_variant+'_formatting'


class LanguagePack:
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
        self.recipe_not_found_message = recipe_not_found_message
        self.no_recipe = no_recipe


class Constants:
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
