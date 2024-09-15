"""Aspects."""

from dataclasses import dataclass
from enum import Enum, Flag, auto
from typing import Any

from astrologer.categories import Influence

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"


class AspectType(Flag):
    """Type of aspect.

    >>> classic_aspects = AspectType.MAJOR | AspectType.MINOR
    >>> AspectType.KEPLER in classic_aspects
    False

    """

    MAJOR = auto()
    MINOR = auto()
    KEPLER = auto()


@dataclass
class AspectDataMixin:
    """Additional properties of aspect."""

    title: str
    brief: str
    val: float
    influence: Influence
    type: AspectType


class Aspect(AspectDataMixin, Enum):
    """Aspect types."""

    CONJUNCTION = "Conjunction", "cnj", 0, Influence.NEUTRAL, AspectType.MAJOR
    VIGINTILE = "Vigintile", "vgt", 18, Influence.NEUTRAL, AspectType.KEPLER
    QUINDECILE = "Quindecile", "qdc", 24, Influence.NEUTRAL, AspectType.KEPLER
    SEMISEXTILE = "Semisextile", "ssx", 30, Influence.POSITIVE, AspectType.MINOR
    DECILE = "Decile", "dcl", 36, Influence.NEUTRAL, AspectType.KEPLER
    SEXTILE = "Sextile", "sxt", 60, Influence.POSITIVE, AspectType.MAJOR
    SEMISQUARE = "Semisquare", "ssq", 45, Influence.NEGATIVE, AspectType.MINOR
    QUINTILE = "Quintile", "qui", 72, Influence.NEUTRAL, AspectType.KEPLER
    SQUARE = "Square", "sqr", 90, Influence.NEGATIVE, AspectType.MAJOR
    TRIDECILE = "Tridecile", "tdc", 108, Influence.POSITIVE, AspectType.MINOR
    TRINE = "Trine", "tri", 120, Influence.POSITIVE, AspectType.MAJOR
    SESQUIQUADRATE = "Sesquiquadrate", "sqq", 135, Influence.NEGATIVE, AspectType.MINOR
    BIQUINTILE = "Biquintile", "bqu", 144, Influence.NEUTRAL, AspectType.KEPLER
    QUINCUNX = "Quincunx", "qcx", 150, Influence.NEGATIVE, AspectType.MINOR
    OPPOSITION = "Opposition", "opp", 180, Influence.NEGATIVE, AspectType.MAJOR

    def __eq__(self, other: Any) -> Any:
        if not isinstance(other, Aspect):
            return NotImplemented
        return self.title == other.title

    def __hash__(self) -> int:
        return hash(self.title)


@dataclass
class AspectInfo:
    """Aspect details."""

    aspect: Aspect
    """aspect type.
    """

    arc: float
    """angular distance between the bodies.
    """

    delta: float
    """difference between actual distance and exact aspect value (degrees).
    """
