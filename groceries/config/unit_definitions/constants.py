# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# unit_definition_file_no.yaml
# Definition of all units available to groceries.py
#   - A unit is identified by a combination of key, 'plural' and 'variants'.
#   - The string representation of a unit is the key for quantity = 1 and
#     'plural' for quantity <> 1.
#   - A unit with scale and base_unit can be normalized to the specified base
#     unit if wanted.
#   - "other" are dimentionless units of measurement with no normalization.
#   - Unused dictionary keys do not need to be specified as they are covered by
#     default values.

import math

from groceries.config.constants.default import constants


# Wrapper for formatting check functions:
def less_than_or_equal_to(base):
    def le_base(candidate):
        return base >= candidate

    return le_base


def less_than(base):
    def lt_base(candidate):
        return base > candidate

    return lt_base


def greater_than_or_equal_to(base):
    def ge_base(candidate):
        return base <= candidate

    return ge_base


def greater_than(base):
    def gt_base(candidate):
        return base < candidate

    return gt_base


def equal_to(base):
    def eq_base(candidate):
        return base == candidate

    return eq_base


def fraction_of(base):
    def fraction_base(candidate):
        number = candidate / base
        for i in constants.intuitive_denominators:
            rest = math.fmod(number, 1 / float(i))
            if rest < 0.001:
                return True
        return False

    return fraction_base


def always_true(candidate):
    return True


metric_prefixes = {
    'k': 1000.0,
    'kilo': 1000.0,
    'h': 100.0,
    'hekto': 100.0,
    'de': 10.0,
    'da': 10.0,  # English shortform
    'deca': 10.0,
    'd': 0.1,
    'deci': 0.1,
    'c': 0.01,
    'centi': 0.01,
    'm': 0.001,
    'milli': 0.001
}

empty_unit = {
    'plural': '',
    'variants': [],
    'prefixes': {},
    'scale': 1
}