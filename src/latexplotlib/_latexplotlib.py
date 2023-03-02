import json
import os
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
from appdirs import user_config_dir

if TYPE_CHECKING:
    from typing import Literal

    Aspect = Union[float, Literal["auto", "equal"]]
else:
    Aspect = Union[float, str]


GOLDEN_RATIO: float = (5**0.5 + 1) / 2
NAME: str = "latexplotlib"

CONFIGFILE: str = "config.ini"
CONFIGDIR: Path = Path(user_config_dir(NAME))
CONFIGPATH: Path = CONFIGDIR.joinpath(CONFIGFILE)
DEFAULT_CONFIG: Dict[str, int] = {"width": 630, "height": 412}


__all__ = [
    "convert_inches_to_pt",
    "convert_pt_to_inches",
    "figsize",
    "size",
    "subplots",
]


def _round(val: float) -> float:
    return int(10 * val) / 10


class Config:
    @classmethod
    def _ensure_path_exists(cls, path: Path):
        if not path.parent.exists():
            path.parent.mkdir()

    def __init__(self, path: Path):
        self._ensure_path_exists(path)
        self.path = path

    def _config(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self.reset()

        with open(self.path, "r", encoding="utf-8") as fh:
            cfg: Dict[str, Any] = json.load(fh)
            return cfg

    def _write(self, cfg: Dict[str, Any]):
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


class Size:
    _width: int
    _height: int

    def __init__(self):
        self._width, self._height = config["width"], config["height"]

    def get(self) -> Tuple[int, int]:
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


def convert_pt_to_inches(pts: Union[int, float]) -> float:
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


def convert_inches_to_pt(inches: float) -> float:
    """Converts a length in inch to a length in pt.

    Parameters
    ----------
    inches : float
        A length in inches.

    Returns
    -------
    float
        A length in pts.

    References
    ----------
    - https://www.overleaf.com/learn/latex/Lengths_in_LaTeX
    """
    return inches * 864.0 * 250.0 / 249.0 / 12.0


def figsize(
    nrows: int = 1,
    ncols: int = 1,
    *,
    scale: float = 1.0,
    aspect: Aspect = GOLDEN_RATIO,
    gridspec_kw: Optional[Dict[str, Any]] = None,
):
    """Computes the optimal figsize.

    This function computes width and height (in inches) such that a figure using this
    figsize fits into a 'lpl.size' box (in pt) in a latex document.

    Parameters
    ----------
    nrows, ncols : int, default: 1
        Number of rows/columns of the subplot grid.
    scale : float, default: 1.0
        The scale of horizontal or vertical space to be used for the figure. For
        values larger then 1.0, the figure is to large to fit on the latex page without
        scaling it.
    aspect : Union[float, Literal["auto", "equal"]], default: 1.618033
        The aspect of figure width to figure height for each individual axis element.
        Defaults to the golden ratio.
    gridspec_kw : dict, optional
        Dict with keywords (normally) passed to the GridSpec constructor used to create
        the grid the subplots are placed on. Ignores everything but 'width_ratios' and
        'height_ratios'.

    Returns
    -------
    width, height : float
        width and height of the figure in inches.
    """
    if scale < 0:
        raise ValueError("'scale' must be positive")
    if isinstance(aspect, str) and aspect not in ["equal", "auto"]:
        raise ValueError("'aspect' a float, 'equal' or 'auto'.")

    width_ratios: Sequence[float] = ncols * [1.0]
    height_ratios: Sequence[float] = nrows * [1.0]

    if gridspec_kw is not None:
        if "width_ratios" in gridspec_kw:
            if len(gridspec_kw["width_ratios"]) != ncols:
                raise ValueError(
                    "Expected the given number of width ratios to match the number of "
                    "columns of the grid"
                )
            width_ratios = gridspec_kw["width_ratios"]

        if "height_ratios" in gridspec_kw:
            if len(gridspec_kw["height_ratios"]) != nrows:
                raise ValueError(
                    "Expected the given number of height ratios to match the number of "
                    "rows of the grid"
                )
            height_ratios = gridspec_kw["height_ratios"]

    max_width_pt, max_height_pt = size.get()

    scale = max(scale, 1)

    if aspect == "equal":
        aspect = 1.0

    if isinstance(aspect, str):
        width_pt, height_pt = scale * max_width_pt, scale * max_height_pt
    else:
        width_pt = max_width_pt * scale
        height_pt = width_pt / aspect * (sum(height_ratios) / sum(width_ratios))

        if height_pt > max_height_pt:
            width_pt = width_pt * max_height_pt / height_pt
            height_pt = max_height_pt

    return (
        _round(convert_pt_to_inches(width_pt)),
        _round(convert_pt_to_inches(height_pt)),
    )


def subplots(
    *args,
    scale: float = 1.0,
    aspect: Aspect = GOLDEN_RATIO,
    ratio: Any = None,
    fraction: Any = None,
    **kwargs,
) -> Tuple[Any, Any]:
    """A wrapper for matplotlib's 'plt.subplots' method

    This function wraps 'plt.subplots'

    Parameters
    ----------
    *args
        see help(plt.subplots)
    scale : float, optional
        The scale of of horizontal or vertical space to be used for the figure. For
        values larger then 1.0, the figure is to large to fit on the latex page without
        scaling it.
    aspect : float, optional
        The aspect of figure width to figure height for each individual axis element.
        Defaults to the golden aspect.
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
        warnings.warn(
            "keyword 'figsize' is ignored and its value discarded.", stacklevel=2
        )

    if ratio is not None:
        warnings.warn(
            "the keyword argument 'ratio' is deprecated and will removed in the "
            "future. Use 'aspect' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    if fraction is not None:
        warnings.warn(
            "the keyword argument 'fraction' is deprecated and will be removed in the "
            "future. Use 'scale' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    if "nrows" in kwargs:
        nrows = kwargs.pop("nrows")
        ncols = kwargs.pop("ncols")
    elif "ncols" in kwargs:
        nrows = args[0]
        ncols = kwargs.pop("ncols")
    else:
        nrows = args[0]
        ncols = args[1]

    gridspec_kw = kwargs.get("gridspec_kw")

    _figsize = figsize(
        nrows, ncols, scale=scale, aspect=aspect, gridspec_kw=gridspec_kw
    )

    return plt.subplots(nrows, ncols, figsize=_figsize, **kwargs)  # type: ignore
