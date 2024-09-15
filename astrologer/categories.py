"""Common types and constants.
"""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class Influence(Enum):
    """Astrological influence."""

    NEUTRAL = auto()
    NEGATIVE = auto()
    POSITIVE = auto()


@dataclass
class IndexAndTitleMixin:
    index: int
    title: str


class Triplicity(IndexAndTitleMixin, Enum):
    """Triplicities."""

    FIRE = 0, "Fire"
    EARTH = 1, "Earth"
    AIR = 2, "Air"
    WATER = 3, "Water"


class Quadruplicity(IndexAndTitleMixin, Enum):
    """Quadruplicities."""

    CARDINAL = 0, "Cardinal"
    FIXED = 1, "Fixed"
    MUTABLE = 2, "Mutable"


@dataclass
class ZodiacSignMixin:
    index: int
    title: str
    triplicity: Triplicity
    quadruplicity: Quadruplicity


class ZodiacSign(ZodiacSignMixin, Enum):
    """Zodiac signs."""

    ARIES = 0, "Aries", Triplicity.FIRE, Quadruplicity.CARDINAL
    TAURUS = 1, "Taurus", Triplicity.EARTH, Quadruplicity.FIXED
    GEMINI = 2, "Gemini", Triplicity.AIR, Quadruplicity.MUTABLE
    CANCER = 3, "Cancer", Triplicity.WATER, Quadruplicity.CARDINAL
    LEO = 4, "Leo", Triplicity.FIRE, Quadruplicity.FIXED
    VIRGO = 5, "Virgo", Triplicity.EARTH, Quadruplicity.MUTABLE
    LIBRA = 6, "Libra", Triplicity.AIR, Quadruplicity.CARDINAL
    SCORPIO = 7, "Scorpio", Triplicity.WATER, Quadruplicity.FIXED
    SAGITTARIUS = 8, "Sagittarius", Triplicity.FIRE, Quadruplicity.MUTABLE
    CAPRICORNUS = 9, "Capricornus", Triplicity.EARTH, Quadruplicity.CARDINAL
    AQUARIUS = 10, "Aquarius", Triplicity.AIR, Quadruplicity.FIXED
    PISCES = 11, "Pisces", Triplicity.WATER, Quadruplicity.MUTABLE


@dataclass
class ChartObjectMixin:
    index: int
    title: str
    influence: Influence


class ChartObjectType(ChartObjectMixin, Enum):
    """Chart objects."""

    MOON = 0, "Moon", Influence.POSITIVE
    SUN = 1, "Sun", Influence.POSITIVE
    MERCURY = 2, "Mercury", Influence.NEUTRAL
    VENUS = 3, "Venus", Influence.POSITIVE
    MARS = 4, "Mars", Influence.NEGATIVE
    JUPITER = 5, "Jupiter", Influence.POSITIVE
    SATURN = 6, "Saturn", Influence.NEGATIVE
    URANUS = 7, "Uranus", Influence.NEGATIVE
    NEPTUNE = 8, "Neptune", Influence.NEUTRAL
    PLUTO = 9, "Pluto", Influence.NEUTRAL
    NODE = 10, "Lunar Node", Influence.NEUTRAL

    def __eq__(self, other: Any) -> Any:
        if not isinstance(other, ChartObjectType):
            return NotImplemented
        return self.title == other.title

    def __hash__(self) -> int:
        return hash(self.title)
