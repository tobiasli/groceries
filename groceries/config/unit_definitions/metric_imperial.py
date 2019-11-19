from groceries.config.config_types import UnitDefinition
from groceries.config.unit_definitions.constants import unit_constants as c

_units = {
    'length': {
        'm': {
            'variants': ['meter', 'meters'],
            'prefixes': c.metric_prefixes
        },
        # Imperial
        'inch': {
            'plural': 'inches',
            'variants': ['tomme', 'tommer', 'inch', 'inches', 'in'],
            'scale': 0.0254,
        },
        'foot': {
            'variants': ['fot', 'ft'],
            'plural': 'feet',
            'scale': 0.3048
        }
    },
    'mass': {
        'g': {
            'variants': ['gram', 'grams'],
            'prefixes': c.metric_prefixes,
        },
        'tonn': {
            'scale': 1000000
        },
        # Imperial
        'oz': {
            'variants': ['ounce', 'ounces'],
            'scale': 28.349523125,
        },
        'lb': {
            'variants': ['pound', 'pounds'],
            'scale': 453.59237,
        }
    },
    'volume': {
        'l': {
            'variants': ['liter', 'litre', 'liters', 'litres'],
            'prefixes': c.metric_prefixes,
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
_formatting = {
        'length': [
            {'unit': 'cm', 'checks': [c.equal_to(0)]},
            {'unit': 'inch', 'checks': [c.less_than(0.5), c.fraction_of(_units['length']['inch']['scale'])]},
            {'unit': 'mm', 'checks': [c.less_than(0.01)]},
            {'unit': 'cm', 'checks': [c.greater_than_or_equal_to(0.01), c.less_than(1)]},
            {'unit': 'm', 'checks': [c.always_true]},  # Last check is always true, so the unit defaults to 'm'.
        ],
        'mass': [
            {'unit': 'g', 'checks': [c.equal_to(0)]},
            {'unit': 'lb', 'checks': [c.less_than(2000), c.fraction_of(_units['mass']['lb']['scale'])]},
            {'unit': 'oz', 'checks': [c.less_than(1000), c.fraction_of(_units['mass']['oz']['scale'])]},
            {'unit': 'kg', 'checks': [c.greater_than_or_equal_to(1000)]},
            {'unit': 'g', 'checks': [c.less_than(1000), c.greater_than_or_equal_to(0.5), c.fraction_of(1)]},
            {'unit': 'mg', 'checks': [c.less_than(1)]},
        ],
        'volume': [
            {'unit': 'l', 'checks': [c.equal_to(0)]},
            {'unit': 'cup', 'checks': [c.fraction_of(_units['volume']['cup']['scale'])]},
            {'unit': 'l', 'checks': [c.greater_than_or_equal_to(1)]},
            {'unit': 'l', 'checks': [c.greater_than_or_equal_to(0.5), c.fraction_of(1)]},
            {'unit': 'dl', 'checks': [c.greater_than_or_equal_to(0.01), c.less_than(1)]},
            {'unit': 'ts', 'checks': [c.less_than(0.015), c.greater_than_or_equal_to(0.005 / 4),
                                      c.fraction_of(_units['volume']['ts']['scale'])]},
            {'unit': 'ss', 'checks': [c.less_than(0.01), c.greater_than_or_equal_to(0.015 / 4),
                                      c.fraction_of(_units['volume']['ss']['scale'])]},
            {'unit': 'ml', 'checks': [c.less_than(0.1)]},
        ],
        'hvitløk': [
            {'unit': 'hel', 'checks': [c.greater_than_or_equal_to(8)]}
        ]
    }
unit_definition = UnitDefinition(
    units=_units,
    formatting=_formatting,
    constants=c
)
