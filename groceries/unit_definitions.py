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

from groceries.constants import *

# Wrapper for formatting check functions:
def less_than_or_equal_to(base):
    def le_base(candidate): return base>=candidate
    return le_base
def less_than(base):
    def lt_base(candidate): return base>candidate
    return lt_base
def greater_than_or_equal_to(base):
    def ge_base(candidate): return base<=candidate
    return ge_base
def greater_than(base):
    def gt_base(candidate): return base<candidate
    return gt_base
def equal_to(base):
    def eq_base(candidate): return base==candidate
    return eq_base
def fraction_of(base):
    def fraction_base(candidate):
        number = candidate/base
        for i in INTUITIVE_FRACTIONS:
            rest = math.fmod(number, 1 / float(i))
            if rest < 0.001:
                return True
        return False
    return fraction_base
def always_true(candidate):
    return True

metric_prefixes = {
    'k':      1000.0,
    'kilo':   1000.0,
    'h':      100.0,
    'hekto':  100.0,
    'de':     10.0,
    'da':     10.0, # English shortform
    'deca':   10.0,
    'd':      0.1,
    'deci':   0.1,
    'c':      0.01,
    'centi':  0.01,
    'm':      0.001,
    'milli':  0.001
    }

empty_unit = {
    'plural': '',
    'variants': [],
    'prefixes': {},
    'scale': 1
    }

dimensions = {
    'length': {
        'm': {
            'variants': ['meter', 'meters'],
            'prefixes': metric_prefixes
            },
        # Imperial
        'inch': {
            'plural': 'inches',
            'variants': ['tomme','tommer','inch','inches','in'],
            'scale': 0.0254,
            },
        'foot': {
            'variants': ['fot','ft'],
            'plural': 'feet',
            'scale': 0.3048
            }
        },
    'mass': {
        'g': {
            'variants': ['gram', 'grams'],
            'prefixes': metric_prefixes,
            },
        'tonn': {
            'scale': 1000000
            },
        # Imperial
        'oz': {
            'variants': ['ounce','ounces'],
            'scale': 28.349523125,
            },
        'lb': {
            'variants': ['pound','pounds'],
            'scale': 453.59237,
            }
        },
    'volume': {
        'l': {
            'variants': ['liter', 'litre', 'liters', 'litres'],
            'prefixes': metric_prefixes,
            },
        # Imperial
        'floz': {
            'variants': ['fluid ounce', 'fluid ounces'],
            'scale': 0.02957
            },
        'cup': {
            'plural': 'cups',
            'scale': 0.2366
            },
        'pint': {
            'plural': 'pints',
            'variants': ['pt'],
            'scale': 0.4732
            },
        # Norwegian
        'ss': {
            'variants': ['spiseskje', 'spiseskjeer', 'tablespoon', 'tbsp', 'tbs', 'tbl'],
            'scale': 0.015,
            },
        'ts': {
            'variants': ['teskje', 'teskjeer', 'teaspoon', 'tsp'],
            'scale': 0.005,
            },
        'kryddermål': {
            'variants': ['krm'],
            'scale': 0.001,
            },
        'dram': {
            'scale': 0.003697,
            }
        },
    'hvitløk': {
        'hel': {
            'plural': 'hele',
            'scale': 8
            },
        'fedd': {}
        },

    'other': {
        # Norwegian
        'pakke': {
            'plural': 'pakker'
            },
        'boks': {
            'plural': 'bokser'
            },
        'tube': {
            'plural': 'tuber'
            },
        'eske': {
            'plural': 'esker'
            },
        'glass': {},
        'pose': {
            'plural': 'poser'
            },
        'porsjon': {
            'plural': 'porsjoner'
            },
        }
    }
# The following specifies how a given unit is represented as a string.
# For each dimension, specify:
#   - The prioritized order of unit representation.
#   - The criteria for if the unit is chosen:
#       - lt: Less than
#       - le: Less or equal
#       - gt: Greater than
#       - ge: Greater or equal
#       - fraction: The amount is an intuitive fraction of the given unit.

# Preferred unit ranges for string representation.
metric_imperial_formatting = {
    'length': [
        {'unit': 'cm',    'checks': [equal_to(0)]},
        {'unit': 'inch',  'checks': [less_than(0.5), fraction_of(dimensions['length']['inch']['scale'])]},
        {'unit': 'cm',    'checks': [greater_than_or_equal_to(0.01), less_than(1)]},
        {'unit': 'mm',    'checks': [less_than(0.01)]},
        {'unit': 'm',     'checks': [always_true]}, # Last check is always true, so the unit defaults to 'm'.
        ],
    'mass': [
        {'unit': 'g',     'checks': [equal_to(0)]},
        {'unit': 'lb',    'checks': [less_than(2000),fraction_of(dimensions['mass']['lb']['scale'])]},
        {'unit': 'oz',    'checks': [less_than(1000),fraction_of(dimensions['mass']['oz']['scale'])]},
        {'unit': 'kg',    'checks': [greater_than_or_equal_to(1000)]},
        {'unit': 'g',     'checks': [less_than(1000),greater_than_or_equal_to(0.5),fraction_of(1)]},
        {'unit': 'mg',    'checks': [less_than(1)]},
        ],
    'volume': [
        {'unit': 'l',     'checks': [equal_to(0)]},
        {'unit': 'cup',   'checks': [fraction_of(dimensions['volume']['cup']['scale'])]},
        {'unit': 'l',     'checks': [greater_than_or_equal_to(1)]},
        {'unit': 'l',     'checks': [greater_than_or_equal_to(0.5),fraction_of(1)]},
        {'unit': 'dl',    'checks': [greater_than_or_equal_to(0.01), less_than(1)]},
        {'unit': 'ts',    'checks': [less_than(0.015), greater_than_or_equal_to(0.005/4), fraction_of(dimensions['volume']['ts']['scale'])]},
        {'unit': 'ss',    'checks': [less_than(0.01), greater_than_or_equal_to(0.015/4), fraction_of(dimensions['volume']['ss']['scale'])]},
        {'unit': 'ml',    'checks': [less_than(0.1)]},
        ],
    'hvitløk': [
        {'unit': 'hel',   'checks': [greater_than_or_equal_to(8)]      }
        ]
    }

metric_formatting = {
    'length': [
        {'unit': 'cm',    'checks': [equal_to(0)]},
        {'unit': 'cm',    'checks': [greater_than_or_equal_to(0.01), less_than(1)]},
        {'unit': 'mm',    'checks': [less_than(0.01)]},
        {'unit': 'm',     'checks': [always_true]}, # Last check is always true, so the unit defaults to 'm'.
        ],
    'mass': [
        {'unit': 'g',     'checks': [equal_to(0)]},
        {'unit': 'kg',    'checks': [greater_than_or_equal_to(1000)]},
        {'unit': 'g',     'checks': [less_than(1000),greater_than_or_equal_to(0.5),fraction_of(1)]},
        {'unit': 'mg',    'checks': [less_than(1)]},
        ],
    'volume': [
        {'unit': 'l',     'checks': [equal_to(0)]},
        {'unit': 'l',     'checks': [greater_than_or_equal_to(1)]},
        {'unit': 'l',     'checks': [greater_than_or_equal_to(0.5),fraction_of(1)]},
        {'unit': 'dl',    'checks': [greater_than_or_equal_to(0.01), less_than(1)]},
        {'unit': 'ts',    'checks': [less_than(0.015), greater_than_or_equal_to(0.005), fraction_of(dimensions['volume']['ts']['scale'])]},
        {'unit': 'ss',    'checks': [less_than(0.01), greater_than_or_equal_to(0.015), fraction_of(dimensions['volume']['ss']['scale'])]},
        {'unit': 'ml',    'checks': [less_than(0.1)]},
        ],
    'hvitløk': [
        {'unit': 'hel',   'checks': [greater_than_or_equal_to(8)]      }
        ]
    }







