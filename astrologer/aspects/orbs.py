"""Aspect orbs.

There are different ways to determine, whether two planets are in
aspect.

"""

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"


from abc import ABC, abstractmethod
from math import fabs

from astrologer.categories import ChartObjectType
from astrologer.objects import ChartObjectInfo
from astropc.mathutils import shortest_arc_deg

from .aspects import Aspect, AspectInfo, AspectType


class OrbsMethod(ABC):
    """Base class for detecting an amount of leeway allowed in the measurement
    of a given aspect or angle.

    Subclasses implement `is_aspect` method, which detects aspect using specific rules.

    """

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    @abstractmethod
    def is_aspect(
        self,
        source: ChartObjectInfo,
        target: ChartObjectInfo,
        aspect: Aspect,
        arc: float | None = None,
    ) -> AspectInfo | None:
        """Check, if two objects are in aspect

        Args:
            source (ChartObjectInfo): source object
            target (ChartObjectInfo): target object
            aspect (Aspect): aspect to check
            arc (float, optional): arc between the objects. May be reused in repeating chects.
        Returns:
            AspectInfo | None: aspect details if there is an aspect, otherwise `None`.
        """


class Dariot(OrbsMethod):
    """Claude Dariot method, based on bodies in aspect.

    _Claude Dariot_ (1533-1594), introduced the so called _'moieties'_
    (mean-values) when calculating orbs. According to Dariot, Mercury and the
    Moon enter completion (application) of any aspect at a  distance of
    **9½°** — the total of their respective moieties:
    `(Mercury = 3½° + Moon = 6°)`.

    This method became the standard for European Renaissance astrologers.
    I does not take into account the nature of aspects.
    """

    moieties = {
        ChartObjectType.MOON: 12.0,
        ChartObjectType.SUN: 15.0,
        ChartObjectType.MERCURY: 7.0,
        ChartObjectType.VENUS: 7.0,
        ChartObjectType.MARS: 8.0,
        ChartObjectType.JUPITER: 9.0,
        ChartObjectType.SATURN: 9.0,
        ChartObjectType.URANUS: 6.0,
        ChartObjectType.NEPTUNE: 6.0,
        ChartObjectType.PLUTO: 5.0,
    }

    default_moiety = 4.0

    def __init__(self) -> None:
        super().__init__("Classic (Claude Dariot)")

    @classmethod
    def get_moiety(cls, obj: ChartObjectType) -> float:
        """Moiety for given object.

        Args:
            obj (ChartObjectType): object

        Returns:
            float: moiety in arc-degrees.
        """
        return cls.moieties.get(obj, cls.default_moiety)

    def calculate_orb(self, src: ChartObjectType, dst: ChartObjectType) -> float:
        """Calculate orb between two objects.

        Args:
            src (ChartObjectType): the first object.
            dst (ChartObjectType): the second object.

        Returns:
            float: orb in arc-degrees.
        """
        a = self.get_moiety(src)
        b = self.get_moiety(dst)
        return (a + b) / 2.0

    def check_aspect(self, aspect: Aspect, orb: float, arc: float) -> AspectInfo | None:
        """Check aspect using calculated orb.

        Args:
            aspect (Aspect): aspect to check
            orb (float): orb in arc-degrees.
            arc: (float): angular distance in arc-degrees

        Returns:
            AspectInfo | None: aspect details if there is an aspect, otherwise `None`.
        """
        delta = fabs(arc - aspect.val)
        if delta <= orb:
            return AspectInfo(aspect=aspect, arc=arc, delta=delta)
        return None

    def is_aspect(
        self,
        source: ChartObjectInfo,
        target: ChartObjectInfo,
        aspect: Aspect,
        arc: float | None = None,
    ) -> AspectInfo | None:
        """See `OrbsMethod.is_aspect`"""
        if arc is None:
            arc = shortest_arc_deg(source.position.lmbda, target.position.lmbda)
        orb = self.calculate_orb(source.type, target.type)
        return self.check_aspect(aspect, orb, arc)


class DeVore(OrbsMethod):
    """Orbs calculation is based on natures of the aspects.

    Some modern astrologers believe that orbs are based on aspects.
    The values are from _"Encyclopaedia of Astrology"_ by _Nicholas deVore_.
    """

    ranges = {
        Aspect.CONJUNCTION: (-10.0, 6.0),
        Aspect.VIGINTILE: (17.5, 18.5),
        Aspect.QUINDECILE: (23.5, 24.5),
        Aspect.SEMISEXTILE: (28.0, 31.0),
        Aspect.DECILE: (35.5, 36.5),
        Aspect.SEXTILE: (56, 63),
        Aspect.SEMISQUARE: (42.0, 49.0),
        Aspect.QUINTILE: (71.5, 72.5),
        Aspect.SQUARE: (84.0, 96.0),
        Aspect.TRIDECILE: (107.5, 108.5),
        Aspect.TRINE: (113.0, 125.0),
        Aspect.SESQUIQUADRATE: (132.0, 137.0),
        Aspect.BIQUINTILE: (143.5, 144.5),
        Aspect.QUINCUNX: (148.0, 151.0),
        Aspect.OPPOSITION: (174, 186),
    }

    def __init__(self) -> None:
        super().__init__("By Aspect (Nicholas deVore)")

    def is_aspect(
        self,
        source: ChartObjectInfo,
        target: ChartObjectInfo,
        aspect: Aspect,
        arc: float | None = None,
    ) -> AspectInfo | None:
        """See `OrbsMethod.is_aspect`"""
        if arc is None:
            arc = shortest_arc_deg(source.position.lmbda, target.position.lmbda)
        range = self.ranges[aspect]
        if range[0] <= arc and range[1] >= arc:
            return AspectInfo(aspect=aspect, arc=arc, delta=fabs(arc - aspect.val))
        return None


class ClassicWithAspectRatio(OrbsMethod):
    """Combined approach.

    For major aspects we use the classic Dariot orb.
    For minor and kepler aspects the classic orb is modified with a
    special coefficient: **0.6 (60%)** and **0.5 (50%)** respectively.
    These coefficients may be set in the initizlizer.
    """

    def __init__(self, minor_coeff: float = 0.6, kepler_coeff: float = 0.5) -> None:
        super().__init__("Classic with regard to Aspect type")
        self._minor_coeff = minor_coeff
        self._kepler_coeff = kepler_coeff
        self._classic = Dariot()

    def is_aspect(
        self,
        source: ChartObjectInfo,
        target: ChartObjectInfo,
        aspect: Aspect,
        arc: float | None = None,
    ) -> AspectInfo | None:
        """See `OrbsMethod.is_aspect`"""
        if arc is None:
            arc = shortest_arc_deg(source.position.lmbda, target.position.lmbda)
        orb = self._classic.calculate_orb(source.type, target.type)
        if aspect.type == AspectType.MINOR:
            orb *= self._minor_coeff
        elif aspect.type == AspectType.KEPLER:
            orb *= self._kepler_coeff
        return self._classic.check_aspect(aspect, orb, arc)
