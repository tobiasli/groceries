from groceries.config.config_types import Constants

constants = Constants(
    number_format=r'(?:%(start)s%(part1)s%(stop)s)?(?:(?<=\d) +)?(?:%(start)s%(part2)s%(stop)s)?%(force_fail)s' % {
        r'start': r'(?:(?<=^)|(?<=[^\d/]))',
        r'part1': r'(?P<amount>\d+(?:[\., ]\d+)?)',
        r'part2': r'(?P<numerator>\d+)/(?P<denominator>\d+)',
        r'stop': r'(?:(?=$)|(?=[^\d/]))',
        r'force_fail': r'(?(amount)|(?(numerator)|(?!)))'},

    # These intuitive_denominators are used for both parsing and formatting. Can be adjusted if needed.
    intuitive_denominators=[2, 3, 4, 8],

    # Rounding limit for chosing to use an intuitive fraction:
    fraction_rest_limit=0.001,

    fractions={  # Replace some special unicode characters with their plain text counterparts.
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
    },
    default_recipe_servings=2,
    ingredient_match_limit=0.9,
    week_plan_comment_prefix='#'
)
