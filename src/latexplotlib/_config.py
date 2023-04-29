import json
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Mapping, Tuple, Union

from appdirs import user_config_dir

GOLDEN_RATIO: float = (5**0.5 + 1) / 2
NAME: str = "latexplotlib"
_PURGED_OLD = "_purged_old_styles"

CONFIGFILE: str = "config.ini"
CONFIGDIR: Path = Path(user_config_dir(NAME))
CONFIGPATH: Path = CONFIGDIR / CONFIGFILE
DEFAULT_CONFIG: Dict[str, int] = {"width": 630, "height": 412, _PURGED_OLD: False}


ConfigData = Union[int, bool]


class Config:
    def __init__(self, path: Path) -> None:
        self.path = path

        if not self.path.exists():
            self.reset()

        self._config = self._open(path)

    def _open(self, path: Path) -> Dict[str, ConfigData]:
        with path.open(encoding="utf-8") as fh:
            config: Dict[str, ConfigData] = json.load(fh)
        return config

    def _write(self, cfg: Mapping[str, ConfigData]) -> None:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)

        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=4)

    def reset(self) -> None:
        if self.path.exists():
            self.path.unlink()

        self._write(DEFAULT_CONFIG)

    def reload(self) -> None:
        self._config = self._open(self.path)

    def __getitem__(self, name: str) -> ConfigData:
        return self._config.get(name, DEFAULT_CONFIG[name])

    def __setitem__(self, name: str, value: ConfigData) -> None:
        self._config[name] = value
        self._write(self._config)


config = Config(CONFIGPATH)


class Size:
    _width: int
    _height: int

    def __init__(self) -> None:
        self._width, self._height = config["width"], config["height"]

    def reload(self) -> None:
        config.reload()
        self._width, self._height = config["width"], config["height"]

    def get(self) -> Tuple[int, int]:
        """Returns the current size of the figure in pts.

        Returns
        -------
        int, int
            (width, height) of the page in pts.
        """
        return self._width, self._height

    def set(self, width: int, height: int) -> None:  # noqa: A003
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
        config["width"], config["height"] = width, height
        self._width, self._height = width, height

    @contextmanager
    def context(self, width: int, height: int) -> Iterator[None]:
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


size = Size()
