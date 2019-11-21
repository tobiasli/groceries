from groceries.configs.config_types import ConfigBase, Settings, Language, Constants, MenuFormat, UnitDefinition
from groceries.configs.constants.default import constants as default_constants
from groceries.configs.settings.metric_imperial import settings as default_settings
from groceries.configs.language.english import language as default_language
from groceries.configs.menu_format.simple_text_menu import menu_format as default_menu_format
from groceries.configs.unit_definition.metric_imperial import unit_definition as default_unit_definition


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
        """Use a specific configs instead of default. Can enter any configs, and it will work:
        I.e. the following will set configs.language to spanish for the entire module.

            from groceries.configs.language.spanish import language as spanish_lang
            from groceries.configs.config_handler import configs

            configs.set_config(spanish_lang)

        """
        setattr(self, config.name, config)


config = ConfigHandler()
