import pytest

from latexplotlib import _config as cfg

GOLDEN_RATIO = (5**0.5 + 1) / 2
CONFIGFILE = "config.ini"
NAME = "latexplotlib"


def test_constants():
    assert cfg.DEFAULT_HEIGHT
    assert cfg.DEFAULT_WIDTH


class TestSize:
    @pytest.fixture
    def height(self):
        return 20

    @pytest.fixture
    def width(self):
        return 10

    @pytest.fixture
    def size(self, width, height):
        return cfg.Size(width=width, height=height)

    def test___init__(self, width, height):
        size = cfg.Size(width=width, height=height)

        assert size._width == width
        assert size._height == height

    def test_get(self, width, height, size):
        assert size.get() == (width, height)

    def test_context(self, size):
        assert size.get() == (10, 20)

        with size.context(44, 43):
            assert size.get() == (44, 43)

        assert size.get() == (10, 20)

    def test_str(self, size):
        str(size)

    def test_repr(self, size):
        repr(size)
