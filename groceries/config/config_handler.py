from groceries.config.config_types import ConfigBase, Settings, Language, Constants, MenuFormat, UnitDefinition
from groceries.config.constants.default import constants as default_constants
from groceries.config.settings.metric_imperial import settings as default_settings
from groceries.config.languages.english import language as default_language
from groceries.config.menu_format.simple_text_menu import menu_format as default_menu_format
from groceries.config.unit_definitions.metric_imperial import unit_definition as default_unit_definition


class ConfigHandler:
    """Class for handling default and non-default"""
    def __init__(self,
                 settings: Settings = None,
                 language: Language = None,
                 constants: Constants = None,
                 menu_format: MenuFormat = None,
                 unit_definition: UnitDefinition = None
                 ):

        self.settings = settings or default_settings
        self.language = language or default_language
        self.constants = constants or default_constants
        self.menu_format = menu_format or default_menu_format
        self.unit_definition = unit_definition or default_unit_definition

    def set_config(self, config: ConfigBase):
        """Use a specific config instead of default. Can enter any config, and it will work:
        I.e. the following will set config.language to spanish for the entire module.

            from groceries.config.language.spanish import language as spanish_lang
            from groceries.config.config_handler import config

            config.set_config(spanish_lang)

        """
        setattr(self, config.name, config)


config = ConfigHandler()
