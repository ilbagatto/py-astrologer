"""Chart objects."""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"

from dataclasses import dataclass
from enum import Enum
from typing import Any

from astropc.planets import EclipticPosition, PlanetId

from .categories import Influence


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



@dataclass
class ChartObjectInfo:
    """Object position in chart."""

    type: ChartObjectType
    """Object type.
    """

    position: EclipticPosition
    """Ecliptical coordinates.
    """
    daily_motion: float = 0.0
    """Mean daily motion.
    """

    house: int = 0
    """House occupied by the object."""


PLANET_TO_OBJECT: dict[PlanetId, ChartObjectType] = {
    PlanetId.MERCURY: ChartObjectType.MERCURY,
    PlanetId.VENUS: ChartObjectType.VENUS,
    PlanetId.MARS: ChartObjectType.MARS,
    PlanetId.JUPITER: ChartObjectType.JUPITER,
    PlanetId.SATURN: ChartObjectType.SATURN,
    PlanetId.URANUS: ChartObjectType.URANUS,
    PlanetId.NEPTUNE: ChartObjectType.NEPTUNE,
    PlanetId.PLUTO: ChartObjectType.PLUTO
}