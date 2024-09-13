import json
import sys
import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Union

from appdirs import user_config_dir

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

Number = Union[int, float]
ConfigData = Union[Number, bool]

GOLDEN_RATIO: float = (5**0.5 + 1) / 2
NAME: str = "latexplotlib"
CONFIGFILE: str = "config.ini"
CONFIGDIR: Path = Path(user_config_dir(NAME))
CONFIGPATH: Path = CONFIGDIR / CONFIGFILE
DEFAULT_WIDTH = 630
DEFAULT_HEIGHT = 412


def find_pyproject_toml() -> Path:
    pyproject = "pyproject.toml"
    path = Path().absolute()
    while path != Path("/"):
        if (path / pyproject).exists():
            return path / pyproject
        path = path.parent

    msg = "Could not find 'pyproject.toml'"
    raise FileNotFoundError(msg)


def find_config_ini() -> Path:
    msg = f"""
        Configuring latexplotlib via {CONFIGPATH} is being deprecated. Please use
        the [tool.latexplotlib] section of the 'pyproject.toml' file instead.

        To silence this warning, please delete the config file {CONFIGPATH}
    """
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

    if CONFIGPATH.exists():
        return CONFIGPATH

    msg = f"No such file: '{CONFIGPATH}'"
    raise FileNotFoundError(msg)


class Size:
    _width: Number
    _height: Number

    def __init__(self, *, width: Number, height: Number) -> None:
        self._width, self._height = width, height

    @classmethod
    def from_pyproject_toml(cls, path: Path) -> "Size":
        with path.open("rb") as fh:
            cfg = tomllib.load(fh)

        config = cfg.get("tool", {}).get("latexplotlib", {})

        return cls(
            width=config.get("width", DEFAULT_WIDTH),
            height=config.get("height", DEFAULT_HEIGHT),
        )

    @classmethod
    def from_config_ini(cls, path: Path) -> "Size":
        with path.open(encoding="utf-8") as fh:
            config: dict[str, Number] = json.load(fh)

        return cls(
            width=config.get("width", DEFAULT_WIDTH),
            height=config.get("height", DEFAULT_HEIGHT),
        )

    def get(self) -> tuple[Number, Number]:
        """Returns the current size of the figure in pts.

        Returns
        -------
        int, int
            (width, height) of the page in pts.
        """
        return self._width, self._height

    def set(self, width: Number, height: Number) -> None:
        """Sets the size of the latex page in pts.

        You can find the size of the latex page with the following commands:

        \\the\\textwidth
        \\the\\textheight

        Parameters
        ----------
        width : int
            The width of the latex page in pts.
        height : int
            The height of the latex page in pts.
        """
        self._width, self._height = width, height

    @contextmanager
    def context(self, width: Number, height: Number) -> Iterator[None]:
        """This context manager temporarily sets the size of the figure in pts.

        Parameters
        ----------
        width : int
            The width of the latex page in pts.
        height : int
            The height of the latex page in pts.
        """
        _width, _height = self._width, self._height
        self._width, self._height = width, height
        yield

        self._width, self._height = _width, _height

    def __repr__(self) -> str:
        return repr(f"{self._width}pt, {self._height}pt")

    def __str__(self) -> str:
        return str(f"{self._width}pt, {self._height}pt")


try:
    path = find_pyproject_toml()
    size = Size.from_pyproject_toml(path)
except FileNotFoundError:
    try:
        path = find_config_ini()

        size = Size.from_config_ini(path)
    except FileNotFoundError:
        size = Size(width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
