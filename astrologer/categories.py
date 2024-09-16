"""Common types and constants.
"""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"

from dataclasses import dataclass
from enum import Enum, auto


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
