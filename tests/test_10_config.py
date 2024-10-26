import pytest

from latexplotlib import _config as cfg


def test_constants():
    assert cfg.DEFAULT_HEIGHT
    assert cfg.DEFAULT_WIDTH


class TestFindPyprojectToml:
    @pytest.fixture
    def path(self, tmp_path, mocker):
        path = tmp_path / "a" / "b" / "c"
        path.mkdir(parents=True)

        mocker.patch("latexplotlib._config.Path.absolute", return_value=path)
        return path

    def test_pyproject_exists(self, path):
        path = path.parent.parent / "pyproject.toml"
        path.touch()

        cfg.find_pyproject_toml()

    def test_pyproject_not_exists(self, path):
        assert cfg.find_pyproject_toml() is None


class TestFindConfigIni:
    @pytest.fixture
    def path(self, tmp_path, monkeypatch):
        path = tmp_path / "a"
        path.mkdir(parents=True)
        path /= "config.123"

        monkeypatch.setattr(cfg, "CONFIGPATH", path)
        return path

    def test_configini_exists(self, path):
        path.touch()

        with pytest.warns(DeprecationWarning):
            cfg.find_config_ini()

    def test_configini_not_exists(self, path):
        assert cfg.find_config_ini() is None


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

    def test_from_pyproject_toml_complete(self, tmp_path):
        width = 123
        height = 456
        path = tmp_path / "pyproject.toml"
        with path.open("w") as fh:
            fh.writelines(
                [
                    "[tool.latexplotlib]\n",
                    f"width = {width}\n",
                    f"height = {height}\n",
                ]
            )

        size = cfg.Size.from_pyproject_toml(path)
        assert size._width == width
        assert size._height == height

    def test_from_pyproject_toml_empty(self, tmp_path):
        path = tmp_path / "pyproject.toml"
        path.touch()

        size = cfg.Size.from_pyproject_toml(path)
        assert size._width == cfg.DEFAULT_WIDTH
        assert size._height == cfg.DEFAULT_HEIGHT

    def test_from_pyproject_toml_tool(self, tmp_path):
        path = tmp_path / "pyproject.toml"
        with path.open("w") as fh:
            fh.writelines(["[tool]\n"])

        size = cfg.Size.from_pyproject_toml(path)
        assert size._width == cfg.DEFAULT_WIDTH
        assert size._height == cfg.DEFAULT_HEIGHT

    def test_from_pyproject_toml_tool_latexplotlib(self, tmp_path):
        path = tmp_path / "pyproject.toml"
        with path.open("w") as fh:
            fh.writelines(["[tool.latexplotlib]\n"])

        size = cfg.Size.from_pyproject_toml(path)
        assert size._width == cfg.DEFAULT_WIDTH
        assert size._height == cfg.DEFAULT_HEIGHT


class TestGetSize:
    def test_todo(self):
        raise NotImplementedError
