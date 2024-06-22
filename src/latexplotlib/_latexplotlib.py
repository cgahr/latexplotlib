import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import matplotlib.pyplot as plt

from ._config import size

if TYPE_CHECKING:
    from typing import Literal

    Aspect = Union[float, Literal["auto", "equal"]]
else:
    Aspect = Union[float, str]


GOLDEN_RATIO: float = (5**0.5 + 1) / 2


__all__ = [
    "convert_inches_to_pt",
    "convert_pt_to_inches",
    "figsize",
    "subplots",
]


def _round(val: float) -> float:
    return int(10 * val) / 10


def convert_pt_to_inches(pts: float) -> float:
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


def figsize(  # noqa: PLR0913
    nrows: int = 1,
    ncols: int = 1,
    *,
    scale: float = 1.0,
    aspect: Aspect = GOLDEN_RATIO,
    height_ratios: Optional[Sequence[float]] = None,
    width_ratios: Optional[Sequence[float]] = None,
) -> Tuple[float, float]:
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
        msg = "'scale' must be positive"
        raise ValueError(msg)
    if isinstance(aspect, str) and aspect not in ["equal", "auto"]:
        msg = "'aspect' a float, 'equal' or 'auto'."
        raise ValueError(msg)

    if width_ratios is None:
        width_ratios = ncols * [1.0]

    if height_ratios is None:
        height_ratios = nrows * [1.0]

    max_width_pt, max_height_pt = size.get()

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
    *args: Any,  # noqa: ANN002
    scale: float = 1.0,
    aspect: Aspect = GOLDEN_RATIO,
    ratio: Any = None,  # noqa: ANN401
    fraction: Any = None,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN003
) -> Any:  # noqa: ANN401
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

    gridspec_kw = kwargs.get("gridspec_kw") or {}
    width_ratios = kwargs.get("width_ratios") or gridspec_kw.get("width_ratios")
    height_ratios = kwargs.get("height_ratios") or gridspec_kw.get("height_ratios")

    _figsize = figsize(
        nrows,
        ncols,
        scale=scale,
        aspect=aspect,
        width_ratios=width_ratios,
        height_ratios=height_ratios,
    )

    return plt.subplots(nrows, ncols, figsize=_figsize, **kwargs)
