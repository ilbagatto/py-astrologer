from pytest import approx, fixture, mark

from astrologer import objects
from astrologer.charts import Place, Radix


@fixture()
def place():
    return Place(name="Test Place", latitude=55.75, longitude=-37.58)


@fixture()
def djd():
    return 3772.990277


class TestRadix:
    delta = 1e-4

    @fixture
    def radix(self, djd, place):
        return Radix("Test Radix", djd=23772.990277, place=place)

    def test_objects_exist(self, radix):
        assert radix.objects is not None

    def test_objects_count(self, radix):
        assert len(radix.objects) == len(objects.ChartObjectType)

    @mark.parametrize(
        "index, expected",
        [
            (0, 110.1573),
            (1, 123.8636),
            (2, 140.6620),
            (3, 164.3171),
            (4, 201.3015),
            (5, 251.6059),
            (6, 290.1573),
            (7, 303.8636),
            (8, 320.6620),
            (9, 344.3171),
            (10, 21.3015),
            (11, 71.6059),
        ],
    )
    def test_houses(self, index, expected, radix):
        cusps = radix.houses
        assert approx(cusps[index], abs=self.delta) == expected

    @mark.parametrize(
        "key, expected",
        [
            ("asc", 110.15731188070275),
            ("mc", 344.3171486574102),
            ("vertex", 242.7037414020605),
            ("eastpoint", 76.70367696243846),
        ],
    )
    def test_points(self, key, expected, radix):
        got = getattr(radix.points, key)
        assert approx(got, abs=self.delta) == expected

    def test_sidereal_time(self, radix):
        assert approx(radix.sidereal_time, abs=self.delta) == 23.03702

    def test_aspects_objects(self, radix):
        aspects = radix.aspects
        assert len(aspects) == 10

    def test_aspects_symmetry(self, radix):
        aspects = radix.aspects
        assert (
            aspects[objects.ChartObjectType.MOON][objects.ChartObjectType.JUPITER]
            == aspects[objects.ChartObjectType.JUPITER][objects.ChartObjectType.MOON]
        )

    def test_no_aspects_to_self(self, radix):
        moon_aspects = radix.aspects[objects.ChartObjectType.MOON]
        assert moon_aspects.get(objects.ChartObjectType.MOON) is None
