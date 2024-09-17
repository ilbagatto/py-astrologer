# flake8: noqa F811

from dataclasses import dataclass
from enum import Enum, auto, unique
from math import degrees, radians
from typing import Iterable

from astropc.mathutils import diff_angle
from astropc.moon import apparent as apparent_moon
from astropc.moon import lunar_node
from astropc.planets import CelestialSphera, EclipticPosition, Planet
from astropc.sun import apparent as apparent_sun
from astropc.timeutils import djd_to_sidereal

from astrologer.aspects.utils import find_closest_aspect

from .aspects import AspectInfo, AspectType, ClassicWithAspectRatio, OrbsMethod
from .houses import (
    HousesSystem,
    equal_asc_cusps,
    equal_mc_cusps,
    in_house,
    morinus_cusps,
    quadrant_cusps,
    signcusp_cusps,
)
from .objects import PLANET_TO_OBJECT, ChartObjectInfo, ChartObjectType
from .points import SensitivePoints, ascendant, eastpoint, midheaven, vertex

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"


AspectsTable = dict[ChartObjectType, dict[ChartObjectType, AspectInfo]]
ObjectsDict = dict[ChartObjectType, ChartObjectInfo]


@unique
class ChartType(Enum):
    RADIX = auto()
    TRANSITS = auto()
    DIRECTIONS = auto()
    SOLAR_RETURN = auto()
    LUNAR_RETURN = auto()
    RELOCATION = auto()
    SYNASTRY = auto()
    COMPOSITE = auto()
    RELATIONSHIP = auto()


@dataclass
class Settings:
    houses: HousesSystem = HousesSystem.PLACIDUS
    orbs_method: OrbsMethod = ClassicWithAspectRatio()
    aspect_types = AspectType.MAJOR
    true_node: bool = True


class BaseChart:
    """Base class for charts."""

    def __init__(self, name: str, charttype: ChartType) -> None:
        self._name = name
        self._type = charttype

    @property
    def name(self) -> str:
        """
        Returns:
            str: chart name.
        """
        return self._name

    @property
    def charttype(self) -> ChartType:
        """
        Returns:
            ChartType: type of the chart.
        """
        return self._type

    def __str__(self) -> str:
        return self._name

    @property
    def objects(self) -> ObjectsDict:  # type: ignore[empty-body]
        """
        Returns:
            ObjectsDict: chart objects.
        """

    @property
    def aspects(self) -> AspectsTable:  # type: ignore[empty-body]
        """
        Returns:
            dict[ChartObjectType, dict[ChartObjectType, AspectInfo]]: aspects.
        """

    @property
    def houses(self) -> tuple[float, ...]:  # type: ignore[empty-body]
        """
        Returns:
            tuple[float, ...]: houses cusps, arc-degrees.
        """

    @property
    def settings(self) -> Settings:  # type: ignore[empty-body]
        """
        Returns:
            Settings: chart settings.
        """

    @property
    def points(self) -> SensitivePoints:  # type: ignore[empty-body]
        """Sensitive points.

        Returns:
            SensitivePoints: longitudes of sensitive points in degrees.
        """


@dataclass
class Place:
    name: str
    latitude: float
    longitude: float


class Radix(BaseChart):
    """Birth chart."""

    def __init__(
        self, name: str, djd: float, place: Place, settings: Settings | None = None
    ):
        super().__init__(name, ChartType.RADIX)

        if settings is None:
            settings = Settings()

        self._djd = djd
        self._place = place
        self._settings = settings
        self._objects = None
        self._aspects = None
        self._houses = None
        self._points = None
        self._sphera = None
        self._lst = None

    @property
    def djd(self) -> float:
        """Date and time of birth.

        Returns:
            float: number of Julian days since 1900 Jan. 0.5.
        """
        return self._djd

    @property
    def place(self) -> Place:
        """Birth place.

        Returns:
            `Place` instance.
        """
        return self._place

    @property
    def settings(self) -> Settings:
        """
        Returns:
            Settings: chart settings.
        """
        return self._settings

    def _calculate_houses(self) -> tuple[float, ...]:
        hsys = self._settings.houses
        match hsys:
            case (
                HousesSystem.PLACIDUS
                | HousesSystem.KOCH
                | HousesSystem.REGIOMONTANUS
                | HousesSystem.CAMPANUS
                | HousesSystem.TOPOCENTRIC
            ):
                return quadrant_cusps(
                    hsys,
                    ramc=radians(self.sidereal_time * 15),
                    eps=radians(self.sphera.obliquity),
                    theta=radians(
                        self.place.latitude,
                    ),
                    asc=radians(self.points.asc),
                    mc=radians(self.points.mc),
                )
            case HousesSystem.MORINUS:
                return morinus_cusps(
                    ramc=radians(self.sidereal_time * 15),
                    eps=radians(self.sphera.obliquity),
                )
            case HousesSystem.EQUAL_ASC:
                return equal_asc_cusps(radians(self.points.asc))
            case HousesSystem.EQUAL_MC:
                return equal_mc_cusps(radians(self.points.mc))
            case HousesSystem.EQUAL_SIGNCUSP:
                return signcusp_cusps()

    def _calculate_objects(self) -> Iterable[ChartObjectInfo]:
        next_djd = self._djd + 1
        sphera = self.sphera
        cusps = self.houses

        next_sphera = CelestialSphera.create(next_djd, apparent=True)

        moo = apparent_moon(self._djd)
        yield ChartObjectInfo(
            type=ChartObjectType.MOON,
            position=EclipticPosition(lmbda=moo.lmbda, beta=moo.beta, delta=moo.delta),
            daily_motion=moo.motion,
            house=in_house(moo.lmbda, cusps),
        )

        sun = apparent_sun(
            self._djd, dpsi=sphera.nutation.dpsi, ignore_light_travel=False
        )
        next_sun = apparent_sun(
            next_djd, dpsi=next_sphera.nutation.dpsi, ignore_light_travel=False
        )
        yield ChartObjectInfo(
            type=ChartObjectType.SUN,
            position=EclipticPosition(lmbda=sun.phi, delta=sun.rho),
            daily_motion=diff_angle(sun.phi, next_sun.phi),
            house=in_house(sun.phi, cusps),
        )

        for id, obj_type in PLANET_TO_OBJECT.items():
            pla = Planet.for_id(id)
            pos = pla.geocentric_position(sphera)
            next_pos = pla.geocentric_position(next_sphera)
            yield ChartObjectInfo(
                type=obj_type,
                position=pos,
                daily_motion=diff_angle(pos.lmbda, next_pos.lmbda),
                house=in_house(pos.lmbda, cusps),
            )

        node = lunar_node(self._djd, true_node=self.settings.true_node)
        next_node = lunar_node(next_djd, true_node=self.settings.true_node)
        yield ChartObjectInfo(
            type=ChartObjectType.NODE,
            position=EclipticPosition(lmbda=node),
            daily_motion=diff_angle(node, next_node),
            house=in_house(node, cusps),
        )

    def _calculate_aspects(
        self,
    ) -> dict[ChartObjectType, dict[ChartObjectType, AspectInfo]]:
        aspects: dict[ChartObjectType, dict[ChartObjectType, AspectInfo]] = {}
        method = self.settings.orbs_method
        flags = self.settings.aspect_types
        objs = self.objects
        keys = list(self.objects.keys())
        sz = len(keys)
        for i in range(0, sz - 1):
            src = objs[keys[i]]
            for j in range(i + 1, sz):
                dst = objs[keys[j]]
                asp = find_closest_aspect(
                    src, dst, orbs_method=method, type_flags=flags.value
                )
                if asp is not None:
                    aspects.setdefault(src.type, {})[dst.type] = asp
                    aspects.setdefault(dst.type, {})[src.type] = asp
        return aspects

    @property
    def sphera(self) -> CelestialSphera:
        if self._sphera is None:
            self._sphera = CelestialSphera.create(self._djd, apparent=True)
        return self._sphera

    @property
    def sidereal_time(self) -> float:
        if self._lst is None:
            self._lst = djd_to_sidereal(self._djd, lng=self.place.longitude)
        return self._lst  # type: ignore[return-value]

    @property
    def objects(self) -> ObjectsDict:
        """
        Returns:
            ObjectsDict: chart objects.
        """
        if self._objects is None:
            self._objects: ObjectsDict = {}  # type: ignore[no-redef, assignment]
            for obj in self._calculate_objects():
                self._objects[obj.type] = obj  # type: ignore[index]

        return self._objects  # type: ignore[return-value]

    @property
    def aspects(self) -> AspectsTable:
        """
        Returns:
            dict[ChartObjectType, dict[ChartObjectType, AspectInfo]]: aspects.
        """
        if self._aspects is None:
            self._aspects = self._calculate_aspects()  # type: ignore[assignment]
        return self._aspects  # type: ignore[return-value]

    @property
    def houses(self) -> tuple[float, ...]:
        """
        Returns:
            tuple[float, ...]: houses cusps, arc-degrees.
        """
        if self._houses is None:
            self._houses = self._calculate_houses()  # type: ignore[assignment]
        return self._houses  # type: ignore[return-value]

    @property  # type: ignore[no-redef]
    def settings(self) -> Settings:
        """
        Returns:
            Settings: chart settings.
        """
        return self._settings

    @property
    def points(self) -> SensitivePoints:
        """Sensitive points.

        Returns:
            SensitivePoints: longitudes of sensitive points in degrees.
        """
        if self._points is None:
            ramc = radians(self.sidereal_time * 15)
            eps = radians(self.sphera.obliquity)
            theta = radians(self.place.latitude)
            self._points = SensitivePoints(  # type: ignore[assignment]
                asc=degrees(ascendant(ramc, eps, theta)),
                mc=degrees(midheaven(ramc, eps)),
                vertex=degrees(vertex(ramc, eps, theta)),
                eastpoint=degrees(eastpoint(ramc, eps)),
            )
        return self._points  # type: ignore[return-value]
