# Superscript numbers: ⁰¹²³⁴⁵⁶⁷⁸⁹ # In case i need them some day.

# Documentation for NUMBER_FORMAT:
# start:    Makes sure there are no leading numbers or forward slashes.
# stop:     Makes sure there are no trailing numbers or forward slashes.
# part1:    Matches integer or decimal numbers.
# part2:    Matches fractions.
# force_fail:   If neither integers/decimals/fractions are found,  negative look-
#               ahead assertion that matches anything but an empty string. As an
#               empty string is always a match,  the pattern automatically fails.

## INGREDIENTS
APROX_PREFIXES = [r'ca\.?', r'aprox\.?', r'aprx\.?', r'aproximately', r'omtrent', r'minst', r'circar']
NUMBER_FORMAT = r'(?:%(start)s%(part1)s%(stop)s)?(?:(?<=\d) +)?(?:%(start)s%(part2)s%(stop)s)?%(force_fail)s' % {
    r'start': r'(?:(?<=^)|(?<=[^\d/]))',
    r'part1': r'(?P<amount>\d+(?:[\., ]\d+)?)',
    r'part2': r'(?P<numerator>\d+)/(?P<denominator>\d+)',
    r'stop': r'(?:(?=$)|(?=[^\d/]))',
    r'force_fail': r'(?(amount)|(?(numerator)|(?!)))'}
INTUITIVE_FRACTIONS = [2, 3, 4,
                       8]
FRACTIONS = {  # Replace some special unicode characters with their plain text counterparts.
    '½': '1/2',
    '⅓': '1/3',
    '⅔': '2/3',
    '¼': '1/4',
    '¾': '3/4',
    '⅕': '1/5',
    '⅖': '2/5',
    '⅗': '3/5',
    '⅘': '4/5',
    '⅙': '1/6',
    '⅚': '5/6',
    '⅛': '1/8',
    '⅜': '3/8',
    '⅝': '5/8',
    '⅞': '7/8',
}
FRACTIONS_INVERSE = {v: k for k, v in FRACTIONS.items()}
NO_RECIPE_NAME = 'annet'
INGREDIENT_APROX_NAME_LIMIT = 80  # Perfect match = 100

## UNITS
# CUSTOM_DIMENSION_NAME = 'other'

## PLANNING
DEFAULT_NUMER_OF_PEOPLE = 2
MADE_FOR_VARIANT = 'til'  # 'made for'
WEEK_PLAN_COMMENT_START = '#'
RECIPE_NOT_FOUND_TAG = '<== Recipe not found'
NO_RECIPE = 'Ingen oppskrift'
