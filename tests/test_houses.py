from math import degrees, radians

from pytest import approx, fixture, mark, raises

from astrologer.houses import (
    HousesSystem,
    campanus_cusps,
    equal_asc_cusps,
    equal_mc_cusps,
    in_house,
    koch_cusps,
    morinus_cusps,
    placidus_cusps,
    quadrant_cusps,
    regiomontanus_cusps,
    signcusp_cusps,
    topocentric_cusps,
)

_DELTA = 1e-3


@fixture()
def ramc():
    return radians(45.0)


@fixture()
def mc():
    return radians(47.47)


@fixture()
def asc():
    return radians(144.92)


@fixture()
def theta():
    return radians(42.0)


@fixture()
def eps():
    return radians(23.4523)


@fixture
def cusps():
    return (
        110.1572788,
        123.8606431,
        140.6604438,
        164.3171029,
        201.3030337,
        251.6072499,
        290.1572788,
        303.8606431,
        320.6604438,
        344.3171029,
        21.3030337,
        71.6072499,
    )


@mark.parametrize(
    "cusp, expected",
    [(0, 87.50), (1, 117.46), (2, 172.43), (3, 200.09)],
)
def test_koch(cusp, expected, ramc, eps, theta, mc):
    got = list(koch_cusps(ramc=ramc, eps=eps, theta=theta, mc=mc))
    assert approx(degrees(got[cusp]), rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [(0, 83.21), (1, 116.42), (2, 167.08), (3, 194.39)],
)
def test_placidus(cusp, expected, ramc, eps, theta):
    got = list(placidus_cusps(ramc=ramc, eps=eps, theta=theta))
    assert approx(degrees(got[cusp]), rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [(0, 86.55), (1, 119.56), (2, 167.79), (3, 193.66)],
)
def test_regiomontanus(cusp, expected, ramc, eps, theta):
    got = list(regiomontanus_cusps(ramc=ramc, eps=eps, theta=theta))
    assert approx(degrees(got[cusp]), rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [(0, 77.90), (1, 111.82), (2, 174.04), (3, 200.48)],
)
def test_campanus(cusp, expected, ramc, eps, theta):
    got = list(campanus_cusps(ramc=ramc, eps=eps, theta=theta))
    assert approx(degrees(got[cusp]), rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [(0, 83.04), (1, 116.25), (2, 167.04), (3, 194.43)],
)
def test_topocentric(cusp, expected, ramc, eps, theta):
    got = list(topocentric_cusps(ramc=ramc, eps=eps, theta=theta))
    assert approx(degrees(got[cusp]), rel=_DELTA) == expected


@mark.parametrize(
    "system",
    [
        HousesSystem.PLACIDUS,
        HousesSystem.KOCH,
        HousesSystem.REGIOMONTANUS,
        HousesSystem.CAMPANUS,
        HousesSystem.TOPOCENTRIC,
    ],
)
def test_quadrant_systems(system, ramc, eps, theta, asc, mc):
    cusps = quadrant_cusps(system, ramc=ramc, eps=eps, theta=theta, asc=asc, mc=mc)
    assert len(cusps) == 12


def test_quadrant_cusps_with_invalid_system(ramc, eps, theta, asc, mc):
    with raises(ValueError):
        quadrant_cusps(HousesSystem.MORINUS, ramc=ramc, eps=eps, theta=theta)


def test_quadrant_cusps_with_invalid_latitude(ramc, eps):
    with raises(ValueError):
        quadrant_cusps(HousesSystem.MORINUS, ramc=ramc, eps=eps, theta=1.58)


@mark.parametrize(
    "cusp, expected",
    [
        (0, 74.321),
        (1, 106.882),
        (2, 138.021),
        (3, 166.707),
        (4, 194.330),
        (5, 223.092),
        (6, 254.321),
        (7, 286.882),
        (8, 318.022),
        (9, 346.707),
        (10, 14.330),
        (11, 43.092),
    ],
)
def test_morinus_cusps(cusp, expected):

    got = morinus_cusps(ramc=radians(345.559001), eps=radians(23.430827))
    assert approx(got[cusp], rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [
        (0, 0.0),
        (1, 30.0),
        (2, 60.0),
        (3, 90.0),
        (4, 120.0),
        (5, 150.0),
        (6, 180.0),
        (7, 210.0),
        (8, 240.0),
        (9, 270.0),
        (10, 300.0),
        (11, 330.0),
    ],
)
def test_signcusp_cusps(cusp, expected):

    got = signcusp_cusps()
    assert approx(got[cusp], rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [
        (0, 110.0),
        (1, 140.0),
        (2, 170.0),
        (3, 200.0),
        (4, 230.0),
        (5, 260.0),
        (6, 290.0),
        (7, 320.0),
        (8, 350.0),
        (9, 20.0),
        (10, 50.0),
        (11, 80.0),
    ],
)
def test_equalasc_cusps(cusp, expected):

    got = equal_asc_cusps(radians(110))
    assert approx(got[cusp], rel=_DELTA) == expected


@mark.parametrize(
    "cusp, expected",
    [
        (0, 110.0),
        (1, 140.0),
        (2, 170.0),
        (3, 200.0),
        (4, 230.0),
        (5, 260.0),
        (6, 290.0),
        (7, 320.0),
        (8, 350.0),
        (9, 20.0),
        (10, 50.0),
        (11, 80.0),
    ],
)
def test_equalmc_cusps(cusp, expected):

    got = equal_mc_cusps(radians(20))
    assert approx(got[cusp], rel=_DELTA) == expected


@mark.parametrize(
    "lng, house",
    [
        (312.4208864, 7),
        (310.2063276, 7),
        (297.0782202, 6),
        (295.2089981, 6),
        (177.9665740, 3),
        (46.9285345, 10),
        (334.6014315, 8),
        (164.0317672, 2),
        (229.9100725, 4),
        (165.8252621, 3),
    ],
)
def test_in_house_with_valid_cusps(lng, house, cusps):
    assert in_house(lng, cusps) == house
