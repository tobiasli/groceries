"""Tests for the unit-components of the groceries package."""
import pytest
import numpy
from groceries.config.config_handler import config
from groceries import units

TEST_CASES_COMPONENTS = [
    ('mg', numpy.array([1000000, 1000000 * 4 / 3]), '1 - 1 1/3 kg'),
    ('gram', numpy.array([1250]), '1 1/4 kg'),
    ('kilometer', numpy.array([0.00003]), '3 cm'),
    ('teskje', numpy.array([4]), '0.20 dl'),
    ('dl', numpy.array([5]), '1/2 l'),
    ('cup', numpy.array([2]), '2 cups'),
    ('inch', numpy.array([0.5, 20]), '1/2 - 20 inches'),
    ('g', numpy.array([7000, 7500]), '7 - 7 1/2 kg'),
    ('l', numpy.array([0.5, 2]), '1/2 - 2 l'),
    ('pakke', numpy.array([0, 1]), '0 - 1 pakke'),
    ('hel', numpy.array([2]), '2 hele'),
    ('fedd', numpy.array([24]), '3 hele'),
    ('ounces', numpy.array([10]), '5/8 lb'),
    ('pint', numpy.array([2]), '4 cups'),
    ('kryddermål', numpy.array([20]), '0.20 dl'),
]


def test_unit_match():
    unit = units.Unit(dimension='mass', units=config.unit_definition.units['mass'])

    assert unit.match('2 kg')
    assert unit.match('kg')
    assert unit.match('1 liter') == (False, False, False)


def test_units_match():
    u = units.Units()

    assert u.match('kg')


@pytest.mark.parametrize('candidate_unit,candidate_amount,expected', TEST_CASES_COMPONENTS)
def test_units(candidate_unit, candidate_amount, expected):
    # This test uses large fractions as output (i.e 1/2) while test_groceries
    # uses small fractions (i.e. ½)
    units.SMALL_FRACTIONS = False

    UNITS = units.Units()

    unit, scale, text = UNITS.match(candidate_unit)
    original_amount = candidate_amount
    scaled_amount = original_amount * scale
    string = unit.amount_formatted(scaled_amount)

    assert unit
    assert candidate_unit == text
    assert string == expected

def test_match_non_unit():
    UNITS = units.Units()
    # Match None-unit:
    unit, scale, text = UNITS.match('nisse')
    assert unit.dimension == 'none'
    assert scale == 1
    assert text == ''
