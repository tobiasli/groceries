# -------------------------------------------------------------------------------
# Name:        units
# Purpose:
#
# Author:      Tobias
#
# Created:     16.10.2015
# Copyright:   (c) Tobias 2015
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import math
import numpy
from re import sub
from typing import List, Tuple, Dict, Union

import tregex

from groceries.config.config_handler import config


class Unit(object):
    """Class for handling the units of groceries. Technically, a Unit object is
    not a unit, but rather a dimension containing several units that are
    normalized."""

    def __init__(self, dimension: str = 'none', units: dict = None, formatting: List[Dict] = None) -> None:
        """Construct Unit object.
        Args:
            dimension (str):    The name of the dimension being measured: length, weight, temperature, none, etc.
            units (dict):       The units defined within this dimension. Default is the "No-unit"-unit.
            formatting (list):  A list of formatting rules for the unit.

        Returns:
            None
        """

        # Object only needs original unit and mutable unit.
        # Everything else is fetched from the Quantity object from pint.
        self.dimension = dimension
        if not units:
            units = {'': config.unit_definition.constants.empty_unit}
        self.lookup_dict = self.construct_lookup_dict(units)

        self.pattern = r'(?:(?<=[\d\W])|(?<=^))(?P<unit>' + '|'.join(self.lookup_dict.keys()) + r')(?:(?=\W)|(?=$))'

        if not formatting:
            unit = list(self.lookup_dict.values())[0]['unit']
            formatting = [{'unit': unit, 'checks': [config.unit_definition.constants.AlwaysTrue()]}]

        self.formatting = formatting

    def __repr__(self) -> str:
        limit = 3
        variants = list(self.lookup_dict.keys())
        if len(variants) > limit:
            etc = ', ...'
        else:
            etc = ''
        return '<Unit: %s: %s>' % (self.dimension, '[' + ', '.join(variants[0:limit]) + etc + ']')

    def match(self, string: str) -> Tuple[object, Union[float, int], str]:
        """Match a candidate string with the unit, and return if match."""

        match = tregex.to_tuple(self.pattern, string)
        if match:
            scale = self.lookup_dict[match[0][0]]['scale']
            text = match[0][0]
            unit = self

            return unit, scale, text
        else:
            return False, False, False

    def scale_amount(self, normalized_amount: numpy.array) -> list:
        """
        Return a list of tuples containing the scaled components of the
        normalized amount,  according to this unit. The components consist
        of integer,  decimal,  numerator and denominator,  along with the
        unit_prefix corresponding to the scaling.
        """

        integer = 0
        decimal = 0
        numerator = 0
        denominator = 0
        unit = ''
        amounts = []

        normalized_amount.sort()

        for variant in self.formatting:
            if len(variant['checks']) == sum([check(normalized_amount[0]) for check in variant['checks']]):
                unit = variant['unit']
                break

        # If no formatting is found, select the unit with scale == 1:
        if not unit:
            for variant in self.lookup_dict:
                if self.lookup_dict[variant]['scale'] == 1:
                    unit = variant
                    break

        # If still no unit, select the unit with the lowest scale:
        if not unit:
            lowest = None
            for variant in self.lookup_dict:
                if not lowest or self.lookup_dict[variant]['scale'] < lowest:
                    unit = variant

        scale = self.lookup_dict[unit]['scale']

        for number in normalized_amount:
            number /= scale
            if number != 0:  # Only parse if nonzero.
                decimal, integer = math.modf(number)

                if decimal:
                    numerator, denominator = self.find_intuitive_fraction(decimal)

            amounts += [(integer, decimal, numerator, denominator, unit)]

        return amounts

    def amount_formatted(self, normalized_amount: numpy.array) -> str:
        """
        Return the amount and unit as a text string,  with logic for handling
        fractions,  scaling to reasonable unit prefixes and plurals.

        Input: Can be both list of numbers (converted to [0]-[1]-[2] etc)

        Assumes that the amount is normalized to the base unit of the current
        current Unit object.
        """

        unit = ''
        space = ''

        amount_strings = []

        if not isinstance(normalized_amount, numpy.ndarray):
            raise TypeError('amount_formatted input must be numpy.ndarray')

        if normalized_amount.size == 0:
            return unit

        less_than_zero = ''
        check = normalized_amount < 0
        if check.all():
            normalized_amount = abs(normalized_amount)
            less_than_zero = '-'

        amounts = self.scale_amount(normalized_amount)

        fraction = False
        for integer, decimal, numerator, denominator, unit in amounts:
            fraction = False
            if decimal:
                if numerator:
                    fraction = True
                    if integer:
                        amount = '%(integer)d %(numerator)d/%(denominator)d' % locals()
                    else:
                        amount = '%(numerator)d/%(denominator)d' % locals()
                else:
                    amount = '%0.2f' % (integer + decimal)  # Keep decimals if fraction is not found.
            else:
                amount = '%0.0f' % integer  # No decimal if no decimal.

            amount_strings += [less_than_zero + amount]

        amount_string = ' - '.join(amount_strings)

        if not normalized_amount.size == 0:
            if max(normalized_amount) != 1 and not fraction:
                unit = self.lookup_dict[unit]['plural']
            else:
                unit = self.lookup_dict[unit]['unit']

        if amount_string and unit:
            space = ' '

        formatted = '%(amount_string)s%(space)s%(unit)s' % locals()

        # Swap big fractions (1/2) with small fractions (½):
        if config.settings.small_fractions:
            for fraction in config.constants.fractions_inverse:
                formatted = sub(fraction, config.constants.fractions_inverse[fraction], formatted)

        return formatted

    @staticmethod
    def find_intuitive_fraction(number: Union[float, int]) -> Union[
        Tuple[None, None], Tuple[Union[float, int], Union[float, int]]]:
        # Return the numerator and denominantor if a number is found to be an
        # intuitive fraction < 1. Return None, None if nothing is found.

        precision = 4  # decimal places

        for i in config.constants.intuitive_denominators:
            rest = math.fmod(round(number, precision), round(1 / float(i), precision))  # Multiply by 100 so that
            if rest < 0.001:
                numerator = round((number - rest) * i)
                denominator = i
                return numerator, denominator
        return None, None

    @staticmethod
    def construct_lookup_dict(units: dict) -> dict:
        lookup = {}
        base_scale = 1
        for unit, properties in units.items():
            # TODO: It may be possible to drop the empty_unit defaults, and rather check if the key is present.
            properties.update({k: v for k, v in config.unit_definition.constants.empty_unit.items() if not k in properties.keys()})

            prefix_loop = ['']
            # Create lookup_dictionary:
            if properties['prefixes']:
                prefix_loop += list(properties['prefixes'].keys())
            if properties['plural']:
                plural_loop = [properties['plural']]
            else:
                plural_loop = []

            variants_loop = properties['variants'] + [unit] + plural_loop

            for prefix in prefix_loop:
                for variant in variants_loop:
                    if not prefix:
                        prefix_scale = base_scale
                    else:
                        prefix_scale = properties['prefixes'][prefix]

                    variant = prefix + variant
                    base_variant = prefix + unit
                    if properties['plural']:
                        plural = prefix + properties['plural']
                    else:
                        plural = base_variant
                    scale = prefix_scale * properties['scale']
                    lookup[variant] = {'scale': scale, 'unit': base_variant, 'plural': plural}
        return lookup


class Units:
    """Units class, for matching and handling Unit objects. Definition of all units available to groceries.
        - A unit is identified by a combination of key, 'plural' and 'variants'.
        - The string representation of a unit is the key for quantity = 1 and 'plural' for quantity <> 1.
        - A unit with scale and base_unit can be normalized to the specified base unit if wanted.
        - "other" are dimentionless units of measurement with no normalization.
        - Unused dictionary keys do not need to be specified as they are covered by default values.
"""

    def __init__(self) -> None:

        self.units = self._define_units()
        self.no_unit = Unit()  # Empty unit with default, blank properties for those groceries without a unit.

    def reload_units(self) -> None:
        """Reload the units based on the config."""
        self.units = self._define_units()

    @staticmethod
    def _define_units() -> list:
        units = []
        for dimension in config.unit_definition.units:

            formatting = config.unit_definition.formatting

            if dimension in formatting:
                formatting = formatting[dimension]
            else:
                formatting = []

            if dimension == 'other':
                for unit, properties in config.unit_definition.units[dimension].items():
                    custom_dimension = dimension + '_' + unit
                    units += [Unit(custom_dimension, {unit: properties}, formatting)]
            else:
                units += [Unit(dimension, config.unit_definition.units[dimension], formatting)]
        return units

    def match(self, string: str) -> Tuple[Unit, Union[float, int], str]:
        for unit in self.units:
            unit, scale, text = unit.match(string)
            if unit:
                return unit, scale, text
        return self.no_unit, 1, ''

units = Units()
