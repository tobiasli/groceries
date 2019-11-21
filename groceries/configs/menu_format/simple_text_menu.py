from groceries.configs.config_types import MenuFormat

menu_format = MenuFormat(
    scaling_number_format=r'\d+(?:[,\.]\d+)?',
    tag_identifier='.+',
    tag_separator=':',
    recipe_identifier='.*?'
)