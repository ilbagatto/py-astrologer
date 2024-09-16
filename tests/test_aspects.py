from astropc.planets import EclipticPosition
from pytest import fixture

from astrologer.aspects import Aspect, find_closest_aspect, iter_stelliums
from astrologer.objects import ChartObjectInfo, ChartObjectType


def test_find_closest_aspect():
    info = find_closest_aspect(
        ChartObjectInfo(
            type=ChartObjectType.MOON,
            position=EclipticPosition(lmbda=310.0),
        ),
        ChartObjectInfo(
            type=ChartObjectType.SUN,
            position=EclipticPosition(lmbda=312.0),
        ),
    )
    assert info.aspect == Aspect.CONJUNCTION


class TestStelliums:
    @fixture()
    def objects(self):
        return (
            ChartObjectInfo(
                type=ChartObjectType.MOON, position=EclipticPosition(lmbda=310.2111)
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN, position=EclipticPosition(lmbda=312.4308)
            ),
            ChartObjectInfo(
                type=ChartObjectType.MERCURY,
                position=EclipticPosition(lmbda=297.0784),
            ),
            ChartObjectInfo(
                type=ChartObjectType.VENUS,
                position=EclipticPosition(lmbda=295.2094),
            ),
            ChartObjectInfo(
                type=ChartObjectType.MARS, position=EclipticPosition(lmbda=177.9662)
            ),
            ChartObjectInfo(
                type=ChartObjectType.JUPITER,
                position=EclipticPosition(lmbda=46.9290),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SATURN,
                position=EclipticPosition(lmbda=334.602),
            ),
            ChartObjectInfo(
                type=ChartObjectType.URANUS,
                position=EclipticPosition(lmbda=164.032),
            ),
            ChartObjectInfo(
                type=ChartObjectType.NEPTUNE,
                position=EclipticPosition(lmbda=229.9224),
            ),
            ChartObjectInfo(
                type=ChartObjectType.PLUTO,
                position=EclipticPosition(lmbda=165.8254),
            ),
        )

    @fixture()
    def objects_around_zero(self):
        return (
            ChartObjectInfo(
                type=ChartObjectType.MOON, position=EclipticPosition(lmbda=310.2111)
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN, position=EclipticPosition(lmbda=312.4308)
            ),
            ChartObjectInfo(
                type=ChartObjectType.MERCURY,
                position=EclipticPosition(lmbda=297.0784),
            ),
            ChartObjectInfo(
                type=ChartObjectType.VENUS,
                position=EclipticPosition(lmbda=295.2094),
            ),
            ChartObjectInfo(
                type=ChartObjectType.MARS, position=EclipticPosition(lmbda=177.9662)
            ),
            ChartObjectInfo(
                type=ChartObjectType.JUPITER,
                position=EclipticPosition(lmbda=6.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SATURN,
                position=EclipticPosition(lmbda=358.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.URANUS,
                position=EclipticPosition(lmbda=164.032),
            ),
            ChartObjectInfo(
                type=ChartObjectType.NEPTUNE,
                position=EclipticPosition(lmbda=229.9224),
            ),
            ChartObjectInfo(
                type=ChartObjectType.PLUTO,
                position=EclipticPosition(lmbda=165.8254),
            ),
        )

    def test_stelliums_with_default_gap(self, objects):
        groups = list(iter_stelliums(objects))
        assert len(groups) == 7

    def test_stelliums_with_large_gap(self, objects):
        groups = list(iter_stelliums(objects, gap=15.0))
        assert len(groups) == 5

    def test_stelliums_with_zero_gap(self, objects):
        groups = list(iter_stelliums(objects, gap=0))
        assert len(groups) == len(objects)

    def test_stelliums_around_zero(self, objects_around_zero):
        groups = list(iter_stelliums(objects_around_zero))
        assert len(groups) == 6
