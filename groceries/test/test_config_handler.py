from groceries.configs.config_handler import config, default_settings
from groceries.configs.config_types import Settings, Language, UnitDefinition, MenuFormat, Constants
from groceries import configs, units, Ingredient
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


def test_change_unit_formatting():
    old_config = deepcopy(config.unit_definition)
    try:
        assert str(Ingredient('2 lbs butter')) == '2 lb butter'

        config.set_config(configs.unit_definition.metric.unit_definition)
        units.units.reload_units()

        assert str(Ingredient('2 lb butter')) == '907.18 g butter'
    finally:
        config.set_config(old_config)