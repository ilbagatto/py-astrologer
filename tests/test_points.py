from math import degrees, radians
from pytest import fixture, approx

from astrologer.points import ascendant, eastspoint, midheaven, vertex


@fixture()
def theta():
    return radians(55.75)


@fixture()
def eps():
    return radians(23.44425561111111)


@fixture()
def ramc():
    return radians(345.5553345833333)


def test_midheaven(ramc, eps):
    got = degrees(midheaven(ramc, eps))
    assert approx(got, abs=1e-3) == 344.3172222222222


def test_ascendant(ramc, eps, theta):
    got = degrees(ascendant(ramc, eps, theta))
    assert approx(got, abs=1e-4) == 110.15722222222222


def test_vertex(ramc, eps, theta):
    got = degrees(vertex(ramc, eps, theta))
    assert approx(got, abs=1e-4) == 242.70361111111112


def test_eastpoint(ramc, eps):
    got = degrees(eastspoint(ramc, eps))
    assert approx(got, abs=1e-4) == 76.70363
