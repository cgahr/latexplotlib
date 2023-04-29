import json

import pytest
from latexplotlib import _config as cfg

GOLDEN_RATIO = (5**0.5 + 1) / 2


CONFIGFILE = "config.ini"

NAME = "latexplotlib"


def test_constants():
    assert cfg.CONFIGFILE
    assert cfg.NAME
    assert cfg.CONFIGDIR
    assert cfg.CONFIGPATH
    assert cfg.DEFAULT_CONFIG


class TestConfig:
    @pytest.fixture()
    def default(self, monkeypatch):
        default = {"apple": 10, "egg": 1, "skyscraper": "a"}
        monkeypatch.setattr(cfg, "DEFAULT_CONFIG", default)
        return default

    @pytest.fixture()
    def path(self, tmp_path, monkeypatch):
        path = tmp_path / "directory" / "dir2" / "tmp.ini"
        path.parent.mkdir(parents=True)
        return path

    @pytest.fixture()
    def config(self, default, path):
        with path.open("w", encoding="utf-8") as fh:
            json.dump(default, fh)

        return cfg.Config(path)

    @pytest.fixture()
    def mock_open(self, default, mocker):
        return mocker.patch("latexplotlib._config.Config._open", return_value=default)

    def test___init___path_exists(self, default, mock_open, mocker, path):
        path.touch()
        mocker.patch(
            "latexplotlib._config.Config.reset",
            side_effect=ValueError("Should not happen"),
        )

        config = cfg.Config(path)

        assert config.path == path
        assert config._config == default
        mock_open.assert_called_once_with(path)

    def test___init___path_not_exists(self, default, mock_open, mocker, path):
        reset = mocker.patch(
            "latexplotlib._config.Config.reset", side_effect=path.touch
        )

        config = cfg.Config(path)

        assert config.path == path
        assert config._config == default
        reset.assert_called_once()
        mock_open.assert_called_once_with(path)

    def test__open(self, config, default, path):
        config._config = None
        assert config._open(path) == default

    def test__write(self, config, default, path):
        config.path.unlink()
        config._write(default)

        cfg = config._open(path)
        assert cfg == default

    def test__write_no_parent(self, config, default, path):
        config.path.unlink()
        config.path.parent.rmdir()

        config._write(default)

        cfg = config._open(path)
        assert cfg == default

    def test__write_no_parents_2(self, config, default, path):
        config.path.unlink()
        config.path.parent.rmdir()
        config.path.parent.parent.rmdir()

        config._write(default)

        cfg = config._open(path)
        assert cfg == default

    def test_reset_path_exists(self, config, default, mocker):
        config._write(default)
        assert config.path.exists()

        mocker.patch.object(config, "_write")

        config.reset()

        assert not config.path.exists()
        config._write.assert_called_once_with(default)

    def test_reset_path_not_exists(self, config, default, mocker):
        config.path.unlink()
        assert not config.path.exists()
        mocker.patch.object(config, "_write")

        config.reset()

        assert not config.path.exists()
        config._write.assert_called_once_with(default)

    def test_reload(self, config, default, mock_open):
        config._config = None
        config.reload()

        assert config._config == default
        mock_open.assert_called_once()

    def test___getitem__(self, config, default):
        for key, item in default.items():
            assert config[key] == item

    def test___setitem__(self, config, default):
        assert config["skyscraper"] != "apple"
        config["skyscraper"] = "apple"
        assert config["skyscraper"] == "apple"


def test_config_path():
    assert cfg.config.path == cfg.CONFIGPATH


class TestSize:
    @pytest.fixture()
    def height(self):
        return 20

    @pytest.fixture()
    def width(self):
        return 10

    @pytest.fixture(autouse=True)
    def _patch_config(self, height, width, monkeypatch, mocker):
        d = {"width": width, "height": height}
        config = mocker.MagicMock(
            __getitem__=lambda _, v: d.__getitem__(v), reload=mocker.MagicMock()
        )
        monkeypatch.setattr(cfg, "config", config)

    @pytest.fixture()
    def size(self):
        return cfg.Size()

    def test___init__(self, width, height):
        size = cfg.Size()

        assert size._width == width
        assert size._height == height

    def test_get(self, width, height, size):
        assert size.get() == (width, height)

    def test_set(self, size):
        size.set(43, 44)
        assert size.get() == (43, 44)

    def test_reload(self, size):
        cur = size.get()

        size.set(0, 0)
        assert size.get() != cur

        size.reload()
        cfg.config.reload.assert_called_once()
        assert size.get() == cur

    def test_context(self, size):
        assert size.get() == (10, 20)

        with size.context(44, 43):
            assert size.get() == (44, 43)

        assert size.get() == (10, 20)

    def test_str(self, size):
        str(size)

    def test_repr(self, size):
        repr(size)
