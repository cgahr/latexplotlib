import json
from pathlib import Path

import numpy as np
import pytest
from appdirs import user_config_dir

from latexplotlib import _latexplotlib as lpl

GOLDEN_RATIO = (5 ** 0.5 + 1) / 2
HEIGHT = 630
WIDTH = 412

CONFIGFILE = "config.ini"

NAME = "latexplotlib"


def test_constants():
    assert lpl.GOLDEN_RATIO == GOLDEN_RATIO
    assert lpl.HEIGHT == HEIGHT
    assert lpl.WIDTH == WIDTH
    assert lpl.CONFIGFILE == CONFIGFILE
    assert lpl.NAME == NAME
    assert lpl.CONFIGDIR == Path(user_config_dir(NAME))
    assert lpl.CONFIGPATH == lpl.CONFIGDIR.joinpath(CONFIGFILE)


@pytest.mark.parametrize("value", [123.234, 23.4576585, 234])
def test__round(value):
    assert int(100 * value) / 100 == lpl._round(value)


class TestSetPageSize:
    def test_dir_exists(self, monkeypatch, tmp_path):
        configpath = tmp_path.joinpath("tmp.ini")
        monkeypatch.setattr(lpl, "CONFIGDIR", tmp_path)
        monkeypatch.setattr(lpl, "CONFIGPATH", configpath)

        lpl.set_page_size(WIDTH, HEIGHT)

        with open(configpath, "r", encoding="utf-8") as cfg:
            config = json.load(cfg)

        assert config["height"] == HEIGHT
        assert config["width"] == WIDTH

    def test_dir_not_exists(self, monkeypatch, tmp_path):
        configdir = tmp_path.joinpath("tmp")
        configpath = configdir.joinpath("tmp.ini")
        monkeypatch.setattr(lpl, "CONFIGDIR", configdir)
        monkeypatch.setattr(lpl, "CONFIGPATH", configpath)

        lpl.set_page_size(WIDTH, HEIGHT)

        with open(configpath, "r", encoding="utf-8") as cfg:
            config = json.load(cfg)

        assert config["height"] == HEIGHT
        assert config["width"] == WIDTH


class TestGetPageSize:
    def test_file_exists(self, monkeypatch, tmp_path):
        configpath = tmp_path.joinpath("tmp.ini")
        monkeypatch.setattr(lpl, "CONFIGDIR", tmp_path)
        monkeypatch.setattr(lpl, "CONFIGPATH", configpath)

        with open(configpath, "w", encoding="utf-8") as cfg:
            json.dump({"width": WIDTH, "height": HEIGHT}, cfg, indent=4)

        width, height = lpl.get_page_size()

        assert height == HEIGHT
        assert width == WIDTH

    def test_file_not_exists(self, monkeypatch, tmp_path):
        configpath = tmp_path.joinpath("tmp.ini")
        monkeypatch.setattr(lpl, "CONFIGDIR", tmp_path)
        monkeypatch.setattr(lpl, "CONFIGPATH", configpath)

        with pytest.warns(UserWarning):
            width, height = lpl.get_page_size()

        assert height == HEIGHT
        assert width == WIDTH


class TestResetPageSize:
    def test_exists(self, monkeypatch, tmp_path):
        configpath = tmp_path.joinpath("tmp.ini")
        monkeypatch.setattr(lpl, "CONFIGPATH", configpath)

        with open(configpath, "w", encoding="utf-8"):
            pass
        assert configpath.exists()

        lpl.reset_page_size()
        assert not configpath.exists()

    def test_not_exists(self, monkeypatch, tmp_path):
        configpath = tmp_path.joinpath("tmp.ini")
        monkeypatch.setattr(lpl, "CONFIGPATH", configpath)

        lpl.reset_page_size()
        assert not configpath.exists()


def test_convert_pt_to_in():
    val = 250 * 864
    ret = 12 * 249
    assert ret == lpl.convert_pt_to_in(val)


class TestSetSize:
    @pytest.mark.parametrize("nrows", [1, 2, 3])
    @pytest.mark.parametrize("ncols", [1, 2, 3])
    @pytest.mark.parametrize("fraction", [0.5, 1.0, 2.0])
    def test_nrows_ncols(self, monkeypatch, nrows, ncols, fraction):
        monkeypatch.setattr(lpl, "get_page_size", lambda: (WIDTH, HEIGHT))

        width = ncols * lpl._round(lpl.convert_pt_to_in(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_in(WIDTH / GOLDEN_RATIO))

        res_width, res_height = lpl._set_size(nrows, ncols, fraction=fraction)
        assert res_width <= width * max(fraction, 1)
        assert res_height <= height * max(fraction, 1)

    def test_negative_fraction(self):
        with pytest.raises(ValueError):
            lpl._set_size(1, 1, fraction=-1)


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
