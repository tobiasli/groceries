"""All config parameters related to language components."""

from groceries.config_types import LanguagePack

language_pack = LanguagePack(
    aprox_prefixes=[r'ca\.?', r'aprox\.?', r'aprx\.?', r'aproximately'],
    no_recipe_name='other',
    servings_prefix='made for',
    recipe_not_found_message='[Recipe not found.]',
    no_recipe='No recipe',
)
