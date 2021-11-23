import json
import os
import sys
import warnings
from typing import Any, Callable, Tuple

import matplotlib.pyplot as plt
from appdirs import user_config_dir

GOLDEN_RATIO = (5 ** 0.5 + 1) / 2

HEIGHT = 630
WIDTH = 412

CONFIGFILE = "config.ini"

NAME = "latexplotlib"
CONFIGDIR = user_config_dir(NAME)


def export(fun: Callable):  # type: ignore
    mod = sys.modules[fun.__module__]
    if hasattr(mod, "__all__"):
        mod.__all__.append(fun.__name__)  # type: ignore
    else:
        mod.__all__ = [fun.__name__]  # type: ignore
    return fun


@export
def set_page_size(height: int, width: int):
    """Sets to size of the latex page in pts.

    You can find the size of the latex page under point 7 and 8 from

    \\usepackage{layout}
    \\layout*

    Parameters
    ----------
    height : int
        The height of the latex page in pts.
    width : int
        The width of the latex page in pts.
    """
    with open(CONFIGDIR + CONFIGFILE, "w", encoding="utf-8") as cfg:
        json.dump({"width": width, "height": height}, cfg, indent=4)


@export
def get_page_size() -> Tuple[int, int]:
    """The size of the latex page in pts.

    Returns
    -------
    int, int
        (height, width) of the page in pts.
    """
    try:
        with open(CONFIGDIR + CONFIGFILE, "r", encoding="utf-8") as cfg:
            config = json.load(cfg)
    except FileNotFoundError:
        warnings.warn("Page size not set, using defaults (see 'set_page_dimension').")
        return WIDTH, HEIGHT
    return config["height"], config["width"]


@export
def reset_page_size():
    if os.path.exists(CONFIGDIR + CONFIGFILE):
        os.remove(CONFIGDIR + CONFIGFILE)


@export
def convert_pt_to_in(pts: int) -> float:
    """Converts a length in pts to a length in inches.

    The length in inches is rounded down to two decimals after the comma.

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
    inch = 12.0 * 249.0 / 250.0 / 864.0 * pts
    return int(100 * inch) / 100


def _set_size(nrows, ncols, fraction: float = 1.0):
    height_pt, width_pt = get_page_size()

    width_in = convert_pt_to_in(width_pt) * fraction
    height_in = width_in / GOLDEN_RATIO * (nrows / ncols)

    max_height_in = convert_pt_to_in(height_pt) * fraction

    if height_in > max_height_in:
        width_in = width_in / max_height_in * height_in
        height_in = max_height_in

    return width_in, height_in


@export
def figsize(fraction: float = 1.0):
    height_pt, width_pt = get_page_size()

    width_in = convert_pt_to_in(width_pt) * fraction
    height_in = width_in / GOLDEN_RATIO

    max_height_in = convert_pt_to_in(height_pt) * fraction

    if height_in > max_height_in:
        width_in = width_in / max_height_in * height_in
        height_in = max_height_in

    return width_in, height_in


@export
def subplots(*args, fraction: float = 1.0, **kwargs) -> Tuple[Any, Any]:
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
        nrows, ncols, figsize=_set_size(nrows, ncols, fraction=fraction), **kwargs
    )
