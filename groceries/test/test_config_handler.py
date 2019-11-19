from groceries.config.config_handler import config, default_settings
from groceries.config.config_types import Settings, Language, UnitDefinition, MenuFormat, Constants
from copy import deepcopy


def test_handler_defaults():
    for config_variant in [Settings, Language, UnitDefinition, MenuFormat, Constants]:
        assert isinstance(getattr(config, config_variant.name), config_variant)


def test_config_handler_set_new():
    test_config = deepcopy(config)
    old_setting = deepcopy(test_config.settings.small_fractions)
    # Flip the small fractions setting in settings:
    new_settings = deepcopy(default_settings)
    new_settings.small_fractions = not new_settings.small_fractions

    test_config.set_config(new_settings)

    assert test_config.settings.small_fractions != old_setting
