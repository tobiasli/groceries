import math
import typing as ty
from abc import abstractmethod

from groceries.config.constants.default import constants

Number = ty.Union[int, float]


class FormattingRuleBase:
    """Base class for all unit formatting rules."""
    def __init__(self, limit: Number = None) -> None:
        """Construct the formatter given the value limit."""
        self.limit = limit

    @abstractmethod
    def method(self, candidate: Number) -> bool:
        """Actual test of parameters. Needs to be specifically implemented."""

    def __call__(self, candidate: Number) -> bool:
        """Perform the rule calculation for this specific formatting rule."""
        return self.method(candidate)

    def __str__(self) -> str:
        if self.limit is None:
            argument = ''
        else:
            argument = self.limit
        return f'{type(self).__name__}({argument})'

    def __repr__(self) -> str:
        return str(self)


class Constants:
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
    # Wrapper for formatting check functions:

    class LessThanOrEqualTo(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            return self.limit >= candidate

    class LessThan(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            return self.limit > candidate

    class GreaterThanOrEqualTo(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            return self.limit <= candidate

    class GreaterThan(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            return self.limit < candidate

    class EqualTo(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            return self.limit == candidate

    class FractionOf(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            number = candidate / self.limit
            for i in constants.intuitive_denominators:
                rest = math.fmod(number, 1 / float(i))
                if rest < constants.fraction_rest_limit:
                    return True
            return False

    class AlwaysTrue(FormattingRuleBase):
        def method(self, candidate: Number) -> bool:
            return True


unit_constants = Constants()
