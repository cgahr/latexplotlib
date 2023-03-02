# pylint: disable = import-error, missing-class-docstring, missing-function-docstring
# pylint: disable = missing-module-docstring, no-self-use, protected-access
# pylint: disable = redefined-outer-name, too-few-public-methods, too-many-arguments
# pylint: disable = unused-argument


import json
import os

import pytest

from latexplotlib import _latexplotlib as lpl

GOLDEN_RATIO = (5**0.5 + 1) / 2
HEIGHT = 30000
WIDTH = 40000

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


def test_convert_pt_to_inches():
    val = 250 * 864
    ret = 12 * 249
    assert ret == lpl.convert_pt_to_inches(val)


class TestFigsize:
    def setup_function(self, monkeypatch, mocker):
        size = mocker.MagicMock()
        size.get = mocker.MagicMock(return_value=(WIDTH, HEIGHT))
        monkeypatch.setattr(lpl, "size", size)

    @pytest.fixture(params=(1, 2, 3))
    def nrows(self, request):
        return request.param

    @pytest.fixture(params=(1, 2, 3))
    def ncols(self, request):
        return request.param

    @pytest.fixture(params=(0.5, 1.0, 2.0))
    def scale(self, request):
        return request.param

    def test_nrows_ncols(self, nrows, ncols, scale):
        width = ncols * lpl._round(lpl.convert_pt_to_inches(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_inches(WIDTH / GOLDEN_RATIO))

        res_width, res_height = lpl.figsize(nrows, ncols, scale=scale)
        assert res_width <= width * max(scale, 1)
        assert res_height <= height * max(scale, 1)

    @pytest.mark.parametrize("aspect", [GOLDEN_RATIO, 1, 2])
    def test_nrows_ncols_with_ratio(self, nrows, ncols, scale, aspect):
        width = ncols * lpl._round(lpl.convert_pt_to_inches(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_inches(WIDTH / aspect))

        res_width, res_height = lpl.figsize(nrows, ncols, scale=scale, aspect=aspect)
        assert res_width <= width * max(scale, 1)
        assert res_height <= height * max(scale, 1)

    def test_negative_fraction(self):
        with pytest.raises(ValueError):
            lpl.figsize(1, 1, scale=-1)

    @pytest.mark.parametrize("aspect", ["equal", "auto"])
    def test_str_ratio(self, nrows, ncols, scale, aspect):
        width = ncols * lpl._round(lpl.convert_pt_to_inches(WIDTH))
        height = nrows * lpl._round(lpl.convert_pt_to_inches(WIDTH))

        res_width, res_height = lpl.figsize(nrows, ncols, scale=scale, aspect=aspect)
        assert res_width <= width * max(scale, 1)
        assert res_height <= height * max(scale, 1)

    def test_gridspec_kw(self, nrows, ncols):
        height_ratios = [0.5, 1.0, 0.1][:nrows]
        width_ratios = [0.7, 1.0, 0.3][:ncols]
        gridspec_kw = {"height_ratios": height_ratios, "width_ratios": width_ratios}

        res_width, res_height = lpl.figsize(
            nrows, ncols, scale=1, aspect=1, gridspec_kw=gridspec_kw
        )

        ratio_theory = sum(height_ratios) / sum(width_ratios)
        ratio_test = res_height / res_width

        assert abs(1 - ratio_theory / ratio_test) <= 0.07

    @pytest.mark.parametrize("aspect", ["test", "asd", "min"])
    def test_invalid_ratio(self, aspect):
        with pytest.raises(ValueError):
            lpl.figsize(1, 1, aspect=aspect)

    def test_invalid_scale(self):
        with pytest.raises(ValueError):
            lpl.figsize(1, 1, scale=-1)


class TestSubplots:
    def test_args(self):
        lpl.subplots(1, 1)
        lpl.subplots(1, ncols=1)
        lpl.subplots(nrows=1, ncols=1)
        lpl.subplots(2, 3)

    def test_deprecates_ratio(self):
        with pytest.warns(DeprecationWarning):
            lpl.subplots(1, 1, ratio=1)

    def test_deprecates_fraction(self):
        with pytest.warns(DeprecationWarning):
            lpl.subplots(1, 1, fraction=1)

    def test_warns_if_figsize_used(self):
        with pytest.warns(UserWarning):
            lpl.subplots(1, 1, figsize=(3, 4))

    def test_plot(self, show):
        fig, axes = lpl.subplots(
            2,
            3,
            aspect="equal",
            gridspec_kw={
                "height_ratios": [0.25, 1.0],
                "width_ratios": [0.25, 1.0, 0.25],
            },
        )

        axes[0, 0].axis("off")
        axes[0, 1].imshow([[1.5, 2.5, 3.5, 4.5]], vmin=0, vmax=6)
        axes[0, 2].axis("off")

        axes[1, 0].imshow([[1.5], [2.5], [3.5], [4.5]], vmin=0, vmax=6)
        axes[1, 1].imshow(
            [[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]], vmin=0, vmax=6
        )
        axes[1, 2].imshow([[1.5], [2.5], [3.5], [4.5]], vmin=0, vmax=6)

        fig.suptitle("test")

    def test_plot2(self, show):
        fig, axes = lpl.subplots(
            1,
            2,
            aspect="equal",
            gridspec_kw={
                "height_ratios": [0.1],
                "width_ratios": [0.2, 1.0],
            },
        )
