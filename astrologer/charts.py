from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto, unique


from astrologer.points import SensitivePoint

from .aspects import AspectInfo, AspectType, ClassicWithAspectRatio, OrbsMethod
from .categories import ChartObjectType
from .objects import ChartObjectInfo

from .houses import HousesSystem

__author__ = "ilbagatto"
__license__ = "MIT"
__version__ = "0.0.1"


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
    aspect_types = AspectType.MAJOR | AspectType.MINOR
    true_node: bool = True


class BaseChart(ABC):
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

    @abstractmethod
    @property
    def objects(self) -> dict[ChartObjectType, ChartObjectInfo]:
        """
        Returns:
            dict[ChartObjectType, ChartObjectInfo]: chart objects.
        """

    @abstractmethod
    @property
    def aspects(self) -> dict[ChartObjectType, AspectInfo]:
        """
        Returns:
            dict[ChartObjectType, AspectInfo]: aspects.
        """

    @abstractmethod
    @property
    def houses(self) -> tuple[float, ...]:
        """
        Returns:
            tuple[float, ...]: houses cusps, arc-degrees.
        """

    @abstractmethod
    @property
    def settings(self) -> Settings:
        """
        Returns:
            Settings: chart settings.
        """

    @abstractmethod
    @property
    def points(self) -> dict[SensitivePoint, float]:
        """Sensitive points.

        Returns:
            dict[SensitivePoint, float]: longitudes of sensitive points in degrees.
        """


@dataclass
class Place:
    name: str
    latitude: float
    longitude: float


class Radix(BaseChart):
    """Birth chart."""

    def __init__(self, name: str, djd: float, place: Place, settings: Settings):
        super().__init__(name, ChartType.RADIX)
        self._djd = djd
        self._place = place
        self._settings = settings
        self._objects = None
        self._aspects = None
        self._houses = None
        self._points = None

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

    # @property
    # def objects(self) -> dict[ChartObjectType, ChartObjectInfo]:
    #     """
    #     Returns:
    #         dict[ChartObjectType, ChartObjectInfo]: chart objects.
    #     """
    #     # if self._objects is None:
    #     #     pass
    #     # return self._objects

    # @property
    # def aspects(self) -> dict[ChartObjectType, AspectInfo]:
    #     """
    #     Returns:
    #         dict[ChartObjectType, AspectInfo]: aspects.
    #     """

    # @property
    # def houses(self) -> tuple[float, ...]:
    #     """
    #     Returns:
    #         tuple[float, ...]: houses cusps, arc-degrees.
    #     """

    # @property
    # def settings(self) -> Settings:
    #     """
    #     Returns:
    #         Settings: chart settings.
    #     """

    # @property
    # def points(self) -> dict[SensitivePoint, float]:
    #     """Sensitive points.

    #     Returns:
    #         dict[SensitivePoint, float]: longitudes of sensitive points in degrees.
    #     """
