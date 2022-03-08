import json
import os
import sys
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional, Tuple

import deprecation
import matplotlib.pyplot as plt
from appdirs import user_config_dir

from ._version import __version__

GOLDEN_RATIO: float = (5**0.5 + 1) / 2
NAME: str = "latexplotlib"

CONFIGFILE: str = "config.ini"
CONFIGDIR: Path = Path(user_config_dir(NAME))
CONFIGPATH: Path = CONFIGDIR.joinpath(CONFIGFILE)
DEFAULT_CONFIG: dict[str, int] = {"width": 630, "height": 412}


# __all__ = [
#     "set_page_size",
#     "get_page_size",
#     "reset_page_size",
#     "config",
#     "size",
#     "convert_pt_to_in",
#     "figsize",
#     "subplots",
# ]


def export(sth: Any, name: Optional[str] = None):  # type: ignore
    mod = sys.modules[sth.__module__]
    name = name if name is not None else sth.__name__

    if hasattr(mod, "__all__"):
        mod.__all__.append(name)  # type: ignore
    else:
        mod.__all__ = [name]  # type: ignore
    return sth


def _round(val: float) -> float:
    return int(10 * val) / 10


@export
@deprecation.deprecated(
    deprecated_in="0.3",
    removed_in="0.4",
    current_version=__version__,
    details="Obsolete, use 'lpl.size.set' instead.",
)
def set_page_size(
    width: int,
    height: int,
):
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
    try:
        os.makedirs(CONFIGDIR)
    except FileExistsError:
        pass

    with open(CONFIGPATH, "w", encoding="utf-8") as cfg:
        json.dump({"width": width, "height": height}, cfg, indent=4)


@export
@deprecation.deprecated(
    deprecated_in="0.3",
    removed_in="0.4",
    current_version=__version__,
    details="Obsolete, use 'lpl.size.get' instead.",
)
def get_page_size() -> Tuple[int, int]:
    """The size of the latex page in pts.

    Returns
    -------
    int, int
        (width, height) of the page in pts.
    """
    try:
        with open(CONFIGPATH, "r", encoding="utf-8") as cfg:
            config = json.load(cfg)
    except FileNotFoundError:
        warnings.warn("Page size not set, using defaults (see 'set_page_dimension').")
        return 630, 412
    return (config["width"], config["height"])


@export
@deprecation.deprecated(
    deprecated_in="0.3",
    removed_in="0.4",
    current_version=__version__,
    details="Obsolete, use 'lpl.size.reset' instead.",
)
def reset_page_size():
    if os.path.exists(CONFIGPATH):
        os.remove(CONFIGPATH)


class Config:
    def __init__(self, path: Path):
        self.path = path

    def _config(self) -> dict[str, Any]:
        if not os.path.exists(self.path):
            self.reset()

        with open(self.path, "r", encoding="utf-8") as fh:
            cfg: dict[str, Any] = json.load(fh)
            return cfg

    def _write(self, cfg: dict[str, Any]):
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=4)

    def __getitem__(self, name: str) -> Any:
        return self._config()[name]

    def __setitem__(self, name: str, value: int):
        cfg = self._config()
        cfg[name] = value
        self._write(cfg)

    def reset(self):
        if os.path.exists(self.path):
            os.remove(self.path)

        self._write(DEFAULT_CONFIG)


config = Config(CONFIGPATH)
export(config, "config")


class Size:
    _width: int
    _height: int

    def __init__(self):
        self._width, self._height = config["width"], config["height"]

    def get(self) -> tuple[int, int]:
        """Returns the current size of the figure in pts.

        Returns
        -------
        int, int
            (width, height) of the page in pts.
        """
        return self._width, self._height

    def set(self, width: int, height: int):
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
    def context(self, width: int, height: int):
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

    def __str__(self):
        return str((self._width, self._height))

    def __repr__(self):
        return repr((self._width, self._height))


size = Size()
export(size, "size")


@export
def convert_pt_to_in(pts: int) -> float:
    """Converts a length in pts to a length in inches.

    Parameters
    ----------
    pts : int
        A length in pts.

    Returns
    -------
    float
        A length in inches.

    References
    ----------
    - https://www.overleaf.com/learn/latex/Lengths_in_LaTeX
    """
    return 12.0 * 249.0 / 250.0 / 864.0 * pts


def _set_size(nrows, ncols, fraction: float = 1.0, ratio: float = GOLDEN_RATIO):
    max_width_pt, max_height_pt = get_page_size()

    if fraction < 0:
        raise ValueError("fraction must be positive!")

    if fraction > 1:
        width_pt = max_width_pt
    else:
        width_pt = max_width_pt * fraction

    height_pt = width_pt / ratio * (nrows / ncols)

    if height_pt > max_height_pt:
        width_pt = width_pt * max_height_pt / height_pt
        height_pt = max_height_pt

    return _round(convert_pt_to_in(width_pt)), _round(convert_pt_to_in(height_pt))


@export
def figsize(fraction: float = 1.0, ratio: float = GOLDEN_RATIO):
    return _set_size(1, 1, fraction=fraction, ratio=ratio)


@export
def subplots(
    *args, fraction: float = 1.0, ratio=GOLDEN_RATIO, **kwargs
) -> Tuple[Any, Any]:
    """A wrapper for matplotlib's 'plt.subplots' method

    This function wraps 'plt.subplots'

    Parameters
    ----------
    *args
        see help(plt.subplots)
    fraction : float, optional
        The fraction of of horizontal or vertical space to be used for the figure. For
        values larger then 1.0, the figure is to large to fit on the latex page without
        scaling it.
    ratio : float, optional
        The ratio of figure width to figure height for each individual axis element.
        Defaults to the golden ratio.
    **kwargs
        see help(plt.subplots)

    Returns
    -------
    Tuple[Figure, axes.Axes or array of Axes]
        see help(plt.subplots)

    References
    ----------
    - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
    - https://jwalton.info/Embed-Publication-Matplotlib-Latex/
    """
    if "figsize" in kwargs:
        kwargs.pop("figsize")
        warnings.warn("keyword 'figsize' is ignored and its value discarded.")

    if "nrows" in kwargs:
        nrows = kwargs.pop("nrows")
        ncols = kwargs.pop("ncols")
    elif "ncols" in kwargs:
        nrows = args[0]
        ncols = kwargs.pop("ncols")
    else:
        nrows = args[0]
        ncols = args[1]

    return plt.subplots(  # type: ignore
        nrows,
        ncols,
        figsize=_set_size(nrows, ncols, fraction=fraction, ratio=ratio),
        **kwargs
    )
