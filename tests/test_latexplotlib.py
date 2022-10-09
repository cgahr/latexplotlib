import json
import os

import pytest

from latexplotlib import _latexplotlib as lpl

GOLDEN_RATIO = (5**0.5 + 1) / 2
HEIGHT = 96978
WIDTH = 3453547

CONFIGFILE = "config.ini"

NAME = "latexplotlib"


def test_constants():
    assert lpl.GOLDEN_RATIO
    assert lpl.CONFIGFILE
    assert lpl.NAME
    assert lpl.CONFIGDIR
    assert lpl.CONFIGPATH
    assert lpl.DEFAULT_CONFIG


@pytest.mark.parametrize("value", [123.234, 23.4576585, 234])
def test__round(value):
    assert int(10 * value) / 10 == lpl._round(value)


class Test_Config:
    @pytest.fixture
    def default(self):
        return {"apple": 10, "egg": 1}

    @pytest.fixture
    def config(self, default, tmp_path, monkeypatch):
        monkeypatch.setattr(lpl, "DEFAULT_CONFIG", default)
        return lpl.Config(tmp_path.joinpath("directory", "tmp.ini"))

    def test__ensure_path_exists(self, tmp_path):
        lpl.Config._ensure_path_exists(tmp_path)

        assert tmp_path.exists()

    def test___init__(self, tmp_path):
        path = tmp_path.joinpath("tmp.ini")
        config = lpl.Config(path)

        assert config.path == path

    def test_write(self, config, default):
        config._write(default)

        assert os.path.exists(config.path)

        with open(config.path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
        assert cfg == default

    def test_reset(self, config, default, mocker):
        default = {"apple": 10, "egg": 1}
        config._write(default)
        assert os.path.exists(config.path)

        mocker.patch.object(config, "_write")

        config.reset()

        assert not os.path.exists(config.path)
        config._write.assert_called_once_with(default)

    def test__config_with_reset(self, config, default, mocker):
        mocker.spy(config, "reset")
        assert not os.path.exists(config.path)

        cfg = config._config()

        config.reset.assert_called_once_with()
        assert cfg == default

    def test__config_wo_reset(self, config, default, mocker):
        config._write(default)
        mocker.spy(config, "reset")
        assert os.path.exists(config.path)

        cfg = config._config()

        config.reset.assert_not_called()
        assert cfg == default

    def test___getitem__(self, config, default):
        config.reset()

        for key, item in default.items():
            assert config[key] == item

    def test___setitem__(self, config, default):
        config.reset()

        config["skyscraper"] = "apple"

        assert config["skyscraper"] == "apple"


class Test_Size:
    @pytest.fixture
    def config(self, monkeypatch):
        monkeypatch.setattr(lpl, "config", {"width": 10, "height": 20})

    @pytest.fixture
    def size(self):
        return lpl.Size()

    def test___init__(self, config):
        size = lpl.Size()

        assert size._width == 10
        assert size._height == 20

    def test_get(self, config, size):
        assert size.get() == (10, 20)

    def test_set(self, config, size):
        size.set(43, 44)
        assert size.get() == (43, 44)

    def test_context(self, config, size):
        assert size.get() == (10, 20)

        with size.context(44, 43):
            assert size.get() == (44, 43)

        assert size.get() == (10, 20)

    def test_str(self, size):
        str(size)

    def test_repr(self, size):
        repr(size)


def test_convert_pt_to_in():
    val = 250 * 864
    ret = 12 * 249
    assert ret == lpl.convert_pt_to_in(val)


class TestSetSize:
    def setup_function(self, monkeypatch, mocker):
        size = mocker.MagicMock()
        size.get = mocker.MagicMock(return_value=(WIDTH, HEIGHT))
        monkeypatch.setattr(lpl, "size", size)

    @pytest.mark.parametrize("nrows", [1, 2, 3])
    @pytest.mark.parametrize("ncols", [1, 2, 3])
    @pytest.mark.parametrize("fraction", [0.5, 1.0, 2.0])
    def test_nrows_ncols(self, nrows, ncols, fraction):
        width = ncols * lpl._round(lpl.convert_pt_to_in(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_in(WIDTH / GOLDEN_RATIO))

        res_width, res_height = lpl._set_size(nrows, ncols, fraction=fraction)
        assert res_width <= width * max(fraction, 1)
        assert res_height <= height * max(fraction, 1)

    @pytest.mark.parametrize("nrows", [1, 2])
    @pytest.mark.parametrize("ncols", [1, 2])
    @pytest.mark.parametrize("fraction", [0.5, 1.0, 2.0])
    @pytest.mark.parametrize("ratio", [GOLDEN_RATIO, 1, 2])
    def test_nrows_ncols_with_ratio(self, nrows, ncols, fraction, ratio):
        width = ncols * lpl._round(lpl.convert_pt_to_in(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_in(WIDTH / ratio))

        res_width, res_height = lpl._set_size(
            nrows, ncols, fraction=fraction, ratio=ratio
        )
        assert res_width <= width * max(fraction, 1)
        assert res_height <= height * max(fraction, 1)

    def test_negative_fraction(self):
        with pytest.raises(ValueError):
            lpl._set_size(1, 1, fraction=-1)

    @pytest.mark.parametrize("nrows", [1, 2])
    @pytest.mark.parametrize("ncols", [1, 2])
    @pytest.mark.parametrize("fraction", [0.5, 1.0, 2.0])
    @pytest.mark.parametrize("ratio", ["any", "max"])
    def test_str_ratio(self, nrows, ncols, fraction, ratio):
        width = ncols * lpl._round(lpl.convert_pt_to_in(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_in(WIDTH))

        res_width, res_height = lpl._set_size(
            nrows, ncols, fraction=fraction, ratio=ratio
        )
        assert res_width <= width * max(fraction, 1)
        assert res_height <= height * max(fraction, 1)

    @pytest.mark.parametrize("ratio", ["test", "asd", "min"])
    def test_invalid_ratio(self, ratio):
        with pytest.raises(ValueError):
            lpl._set_size(1, 1, ratio=ratio)


@pytest.mark.parametrize("fraction", [0.1, 0.5, 0.9, 1.0])
def test_figsize(fraction):
    assert lpl._set_size(1, 1, fraction=fraction) == lpl.figsize(fraction=fraction)


def test_subplots():
    lpl.subplots(1, 1)
    lpl.subplots(1, ncols=1)
    lpl.subplots(nrows=1, ncols=1)
    lpl.subplots(2, 3)

    with pytest.warns(UserWarning):
        lpl.subplots(1, 1, figsize=(3, 4))
