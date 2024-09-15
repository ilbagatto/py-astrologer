"""Chart objects."""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"

from dataclasses import dataclass

from .categories import ChartObjectType
from astropc.planets.planet import EclipticPosition


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
