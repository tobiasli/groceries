"""All config parameters related to language components."""

from groceries.config_types import LanguagePack

language_pack = LanguagePack(
    aprox_prefixes=[r'ca\.?', r'aprox\.?', r'aprx\.?', r'aproximately', r'omtrent', r'minst', r'circar'],
    no_recipe_name='annet',
    servings_prefix='til',
    recipe_not_found_message='[Oppskrift ikke funnet.]',
    no_recipe='Ingen oppskrift'
)
