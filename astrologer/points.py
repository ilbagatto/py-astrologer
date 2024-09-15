"""Sensitive points.

Most of the calculations in this module are in radians.
"""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"

from enum import StrEnum
from math import atan2, cos, pi, sin, tan

from astropc.mathutils import reduce_rad


class SensitivePoint(StrEnum):
    ASCENDANT = "Ascendant"
    MIDHEAVEN = "Midheaven"
    EASTPOINT = "EastPoint"
    VERTEX = "Vertex"


_R90 = 1.5707963267948966  # 90 deg in radians


def midheaven(ramc: float, eps: float) -> float:
    """Midheaven, or The Medium Coeli, MC

    The highest point of intersection between the meridian and the ecliptic.

    Args:
        ramc (float): right ascension of the meridian, in radians.
        eps (float): Ecliptic obliquity, in radians.

    Returns:
        float: MC, in radians
    """
    x = atan2(tan(ramc), cos(eps))
    if x < 0:
        x += pi

    if sin(ramc) < 0:
        x += pi

    return reduce_rad(x)


def ascendant(ramc: float, eps: float, theta: float) -> float:
    """Ascendant.

    The point of the zodiac rising on the Eastern horizon.

    Args:
        ramc (float): right ascension of the meridian, in radians.
        eps (float): Ecliptic obliquity, in radians.
        theta (float): geographical latitude, in radians, positive northwards.

    Returns:
        float:  Ascendant, in radians.
    """
    return reduce_rad(atan2(cos(ramc), -sin(ramc) * cos(eps) - tan(theta) * sin(eps)))


def vertex(ramc: float, eps: float, theta: float) -> float:
    """Vertex.

    The westernmost point on the Ecliptic where it intersects the Prime Vertical.

    Args:
        ramc (float): right ascension of the meridian, in radians.
        eps (float): Ecliptic obliquity, in radians.
        theta (float): geographical latitude, in radians, positive northwards.

    Returns:
        float: Vertex longitude, in radians.
    """
    return ascendant(ramc + pi, eps, _R90 - theta)


def eastspoint(ramc: float, eps: float) -> float:
    """East Point.

    East Point (aka Equatorial Ascendant)  is the sign and degree rising over
    the Eastern Horizon at the Earth's equator at any given time.

    Args:
        ramc (float): right ascension of the meridian, in radians.
        eps (float): Ecliptic obliquity, in radians.

    Returns:
        float: East Point longitude, in radians.
    """
    return reduce_rad(atan2(cos(ramc), -sin(ramc) * cos(eps)))
