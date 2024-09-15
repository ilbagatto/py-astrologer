"""Astrological Houses.

Available house systems are:

1. Quadrant-based systems:
   * Placidus
   * Koch
   * Regiomontanus
   * Campanus
   * Topocentric
2. Morinus System.
3. Equal Systems.

"""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"

from enum import StrEnum
from math import acos, asin, atan2, cos, degrees, fabs, pi, sin, tan
from typing import Iterator

from astropc.mathutils import reduce_deg, reduce_rad, shortest_arc_rad

from astrologer.points import ascendant, midheaven

_HALF_SECOND = 0.5 / 3600
_R30 = 0.5235987755982988
_R60 = 1.0471975511965976
_R90 = 1.5707963267948966
_R120 = 2.0943951023931953
_R150 = 2.6179938779914944


_PLACIDUS_ARGS = ((10, 3.0, _R30), (11, 1.5, _R60), (1, 1.5, _R120), (2, 3.0, _R150))
_PLAC_DELTA = 1e-4
_TOPOCENTRIC_ARGS = ((-_R60, 1.0), (-_R30, 2.0), (_R30, 2), (_R60, 1.0))


class HousesSystem(StrEnum):
    PLACIDUS = "Placidus"
    KOCH = "Koch"
    REGIOMONTANUS = "Regio-Montanus"
    CAMPANUS = "Campanus"
    TOPOCENTRIC = "Topocentric"
    MORINUS = "Morinus"
    EQUAL_SIGNCUSP = "Equal (Sign-Cusp)"
    EQUAL_ASC = "Equal from Asc"
    EQUAL_MC = "Equal from MC"


def placidus_cusps(*, ramc: float, eps: float, theta: float) -> Iterator[float]:
    """Calculate house cusps using Placidus method.

    Args:
         ramc (float): Right ascension of the Meridian, radians.
         eps (float): Obliquity of the ecliptic in radians.
         theta (float): Geographic latitude in radians, positive northwards.
    Yields:
        Iterator[float]: longitude of the base cusps (11, 12, 2, 3) in radians
    """
    tt = tan(theta) * tan(eps)
    cs_eps = cos(eps)

    for i, f, x0 in _PLACIDUS_ARGS:
        k, r = (-1, ramc) if i in (10, 11) else (1, ramc + pi)
        last_x = x0 + ramc
        while True:
            x = r - k * (acos(k * sin(last_x) * tt)) / f
            if abs(shortest_arc_rad(x, last_x)) < _PLAC_DELTA:
                break
            last_x = x
        yield reduce_rad(atan2(sin(last_x), cs_eps * cos(last_x)))


def koch_cusps(*, ramc: float, eps: float, theta: float, mc: float) -> Iterator[float]:
    """Calculate house cusps using Koch method.

    Args:
        ramc (float): Right ascension of the Meridian, radians.
        eps (float): Obliquity of the ecliptic in radians.
        theta (float): Geographic latitude in radians, positive northwards.
        mc (float): MC in radians.

    Yields:
        Iterator[float]: longitude of the base cusps (11, 12, 2, 3) in radians
    """
    tn_theta = tan(theta)
    sn_eps = sin(eps)
    sn_mc = sin(mc)
    k = asin(tn_theta * tan(asin(sn_mc * sn_eps)))
    k1 = k / 3
    k2 = k1 * 2
    offsets = [-_R60 - k2, -_R30 - k1, _R30 + k1, _R60 + k2]
    for x in offsets:
        yield ascendant(ramc + x, eps, theta)


def regiomontanus_cusps(*, ramc: float, eps: float, theta: float) -> Iterator[float]:
    """Calculate house cusps using Regio-Montanus method.

    Args:
        ramc (float): Right ascension of the Meridian, radians.
        eps (float): Obliquity of the ecliptic in radians.
        theta (float): Geographic latitude in radians, positive northwards.

    Yields:
        Iterator[float]: longitude of the base cusps (11, 12, 2, 3) in radians
    """
    tn_theta = tan(theta)
    for h in (_R30, _R60, _R120, _R150):
        rh = ramc + h
        r = atan2(sin(h) * tn_theta, cos(rh))
        yield reduce_rad(atan2(cos(r) * tan(rh), cos(r + eps)))


def campanus_cusps(*, ramc: float, eps: float, theta: float) -> Iterator[float]:
    """Calculate house cusps using Campanus method.

    Args:
        ramc (float): Right ascension of the Meridian, radians.
        eps (float): Obliquity of the ecliptic in radians.
        theta (float): Geographic latitude in radians, positive northwards.
    Yields:
        Iterator[float]: longitude of the base cusps (11, 12, 2, 3) in radians
    """
    rm90 = ramc + _R90
    sn_the = sin(theta)
    cs_the = cos(theta)
    for h in (_R30, _R60, _R120, _R150):
        sn_h = sin(h)
        d = rm90 - atan2(cos(h), sn_h * cs_the)
        c = atan2(tan(asin(sn_the * sn_h)), cos(d))
        yield reduce_rad(atan2(tan(d) * cos(c), cos(c + eps)))


def topocentric_cusps(*, ramc: float, eps: float, theta: float) -> Iterator[float]:
    """Calculate house cusps using Topocentric method.

    Args:
        ramc (float): Right ascension of the Meridian, radians.
        eps (float): Obliquity of the ecliptic in radians.
        theta (float): Geographic latitude in radians, positive northwards.
    Yields:
        Iterator[float]: longitude of the base cusps (11, 12, 2, 3) in radians
    """
    tn_the = tan(theta)
    for x, n in _TOPOCENTRIC_ARGS:
        yield ascendant(ramc + x, eps, atan2(n * tn_the, 3))


def quadrant_cusps(
    system: HousesSystem,
    *,
    ramc: float,
    eps: float,
    theta: float,
    asc: float | None = None,
    mc: float | None = None,
) -> tuple[float, ...]:
    """Calculate cusps using one of quadrant-based system.

    Quadrant systems are:
       * Placidus
       * Koch
       * Regiomontanus
       * Campanus
       * Topocentric

    Args:
        system (HousesSystem): a system
        ramc (float): Right ascension of the Meridian, radians.
        eps (float): Obliquity of the ecliptic in radians.
        theta (float): Geographic latitude in radians, positive northwards.
        asc (float | None, optional): Ascendant, radians
        mc (float | None, optional): Midheaven, radians

    Raises:
        ValueError: if the function is called for a high latitude where quadrant systems fail.
        ValueError: if given system is not a quadrant system (e.g. Morinus or Equal).

    Returns:
        tuple[float, ...]: longitudes of cusps 1-12 in arc-degrees.
    """

    if fabs(theta) > _R90 - fabs(eps):
        raise ValueError("Quadrant system fails at high latitudes")

    if mc is None:
        mc = midheaven(ramc, eps)
    if asc is None:
        asc = ascendant(ramc, eps, theta)

    match system:
        case HousesSystem.KOCH:
            iter = koch_cusps(ramc=ramc, eps=eps, theta=theta, mc=mc)
        case HousesSystem.PLACIDUS:
            iter = placidus_cusps(ramc=ramc, eps=eps, theta=theta)
        case HousesSystem.REGIOMONTANUS:
            iter = regiomontanus_cusps(ramc=ramc, eps=eps, theta=theta)
        case HousesSystem.CAMPANUS:
            iter = campanus_cusps(ramc=ramc, eps=eps, theta=theta)
        case HousesSystem.TOPOCENTRIC:
            iter = topocentric_cusps(ramc=ramc, eps=eps, theta=theta)
        case _:
            raise ValueError(f"{system} is not a topocentric system")
    base = list(iter)
    all_cusps = (
        asc,
        base[2],
        base[3],
        reduce_rad(mc + pi),
        reduce_rad(base[0] + pi),
        reduce_rad(base[1] + pi),
        reduce_rad(asc + pi),
        reduce_rad(base[2] + pi),
        reduce_rad(base[3] + pi),
        mc,
        base[0],
        base[1],
    )
    return tuple([degrees(x) for x in all_cusps])


def morinus_cusps(ramc: float, eps: float) -> tuple[float, ...]:
    """Calculate house cusps using Topocentric method.

    Args:
         ramc (float): Right ascension of the Meridian, radians.
         eps (float): Obliquity of the ecliptic in radians.

    Returns:
        tuple[float, ...]:  longitudes of cusps 1-12 in arc-degrees.
    """
    cs_eps = cos(eps)
    cusps = []
    for i in range(12):
        r = ramc + _R60 + _R30 * (i + 1)
        y = sin(r) * cs_eps
        x = cos(r)
        cusps.append(reduce_deg(degrees(atan2(y, x))))

    return tuple(cusps)


def equal_cusps(start_n: int = 0, start_x: float = 0.0) -> tuple[float, ...]:
    """Base routine for equal systems.

    Args:
        start_n (int, optional): index of the base cusp. Defaults to 0.
        start_x (float, optional): longitude of starting point. Defaults to 0.0.

    Returns:
        tuple[float, ...]: longitudes of cusps 1-12 in arc-degrees.
    """
    cusps = [0] * 12
    for i in range(12):
        n = (start_n + i) % 12
        cusps[n] = degrees(reduce_rad(start_x + _R30 * i))  # type: ignore
    return tuple(cusps)


def signcusp_cusps() -> tuple[float, ...]:
    """Calculate cusps using of Sign-Cusp system.

    Returns:
        tuple[float, ...]: longitudes of cusps 1-12 in arc-degrees.
    """
    return equal_cusps()


def equal_asc_cusps(asc: float) -> tuple[float, ...]:
    """Calculate cusps using of Equal from Ascendant system.

    Args:
        asc (float): Ascendant in radians.
    Returns:
        tuple[float, ...]: longitudes of cusps 1-12 in arc-degrees.
    """
    return equal_cusps(start_x=asc)


def equal_mc_cusps(mc: float) -> tuple[float, ...]:
    """Calculate cusps using of Equal from Midheaven system.

    Args:
        mc (float): Midheaven in radians.
    Returns:
        tuple[float, ...]: longitudes of cusps 1-12 in arc-degrees.

    If cusps tuple contains invaid data,the result is undefined.
    """
    return equal_cusps(start_x=mc, start_n=9)


def in_house(x: float, cusps: tuple[float, ...]) -> int:
    """Find in which house is a given point.

    Args:
        x (float): longitude in arc-degrees
        cusps (tuple[float, ...]): longitudes of 12 house cusps in arc-degrees

    Returns:
        int: index of a house
    """
    r = reduce_deg(x + _HALF_SECOND)
    result = 0
    ln = len(cusps)
    for i in range(ln):
        a = cusps[i]
        b = cusps[(i + 1) % ln]
        if ((a <= r) and (r < b)) or (a > b and (r >= a or r < b)):
            result = i
            break
    return result
