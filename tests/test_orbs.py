from pytest import fixture, mark

from astrologer.aspects import Aspect, AspectInfo, ClassicWithAspectRatio, Dariot, DeVore
from astrologer.objects import ChartObjectInfo, ChartObjectType
from astropc.planets import EclipticPosition


@fixture()
def dariot():
    return Dariot()


@fixture()
def devore():
    return DeVore()


@fixture()
def classic_with_aspect_ratio():
    return ClassicWithAspectRatio()


@mark.parametrize(
    "source, target, aspect, result",
    [
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            Aspect.CONJUNCTION,
            AspectInfo(aspect=Aspect.CONJUNCTION, delta=2.0, arc=2.0),
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.MERCURY,
                position=EclipticPosition(lmbda=295.0),
            ),
            Aspect.CONJUNCTION,
            None,
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            Aspect.OPPOSITION,
            None,
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.JUPITER,
                position=EclipticPosition(lmbda=46.0),
            ),
            Aspect.SQUARE,
            AspectInfo(aspect=Aspect.SQUARE, delta=4.0, arc=94.0),
        ),
    ],
)
def test_dariot(
    source: ChartObjectInfo,
    target: ChartObjectInfo,
    aspect: Aspect,
    result: AspectInfo | None,
    dariot: Dariot,
):
    assert dariot.is_aspect(source, target, aspect) == result


@mark.parametrize(
    "source, target, aspect, result",
    [
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            Aspect.CONJUNCTION,
            AspectInfo(aspect=Aspect.CONJUNCTION, delta=2.0, arc=2.0),
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.MERCURY,
                position=EclipticPosition(lmbda=295.0),
            ),
            Aspect.CONJUNCTION,
            None,
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            Aspect.OPPOSITION,
            None,
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.JUPITER,
                position=EclipticPosition(lmbda=46.0),
            ),
            Aspect.SQUARE,
            AspectInfo(aspect=Aspect.SQUARE, delta=4.0, arc=94.0),
        ),
    ],
)
def test_devore(
    source: ChartObjectInfo,
    target: ChartObjectInfo,
    aspect: Aspect,
    result: AspectInfo | None,
    devore: DeVore,
):
    assert devore.is_aspect(source, target, aspect) == result


@mark.parametrize(
    "source, target, aspect, result",
    [
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            Aspect.CONJUNCTION,
            AspectInfo(aspect=Aspect.CONJUNCTION, delta=2.0, arc=2.0),
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.MERCURY,
                position=EclipticPosition(lmbda=295.0),
            ),
            Aspect.CONJUNCTION,
            None,
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.MOON,
                position=EclipticPosition(lmbda=310.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            Aspect.OPPOSITION,
            None,
        ),
        (
            ChartObjectInfo(
                type=ChartObjectType.SUN,
                position=EclipticPosition(lmbda=312.0),
            ),
            ChartObjectInfo(
                type=ChartObjectType.JUPITER,
                position=EclipticPosition(lmbda=46.0),
            ),
            Aspect.SQUARE,
            AspectInfo(aspect=Aspect.SQUARE, delta=4.0, arc=94.0),
        ),
    ],
)
def test_classic_with_aspect_ratio(
    source: ChartObjectInfo,
    target: ChartObjectInfo,
    aspect: Aspect,
    result: AspectInfo | None,
    classic_with_aspect_ratio,
):
    assert classic_with_aspect_ratio.is_aspect(source, target, aspect) == result
