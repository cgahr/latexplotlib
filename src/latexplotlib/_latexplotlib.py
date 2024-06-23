import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import matplotlib.pyplot as plt

from ._config import size

if TYPE_CHECKING:
    from matplotlib.figure import Figure
else:
    Figure = Any


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
    aspect: Union[float, Literal["auto", "equal"]] = GOLDEN_RATIO,
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


def subplots(  # noqa: PLR0913
    nrows: int = 1,
    ncols: int = 1,
    *,
    scale: float = 1.0,
    ratio: Any = None,  # noqa: ANN401
    fraction: Any = None,  # noqa: ANN401
    aspect: Union[float, Literal["auto", "equal"]] = GOLDEN_RATIO,
    sharex: Union[bool, Literal["none", "all", "row", "col"]] = False,
    sharey: Union[bool, Literal["none", "all", "row", "col"]] = False,
    squeeze: bool = True,
    width_ratios: Optional[Sequence[float]] = None,
    height_ratios: Optional[Sequence[float]] = None,
    subplot_kw: Optional[Dict[str, Any]] = None,
    gridspec_kw: Optional[Dict[str, Any]] = None,
    **fig_kw: Any,  # noqa: ANN401
) -> Tuple[Figure, Any]:
    """
    Create a figure and a set of subplots.

    This utility wrapper makes it convenient to create common layouts of
    subplots, including the enclosing figure object, in a single call.

    Parameters
    ----------
    nrows, ncols : int, default: 1
        Number of rows/columns of the subplot grid.

    scale : float, optional
        The scale of of horizontal or vertical space to be used for the figure. For
        values larger then 1.0, the figure is to large to fit on the latex page without
        scaling it.

    aspect : float, optional
        The aspect of figure width to figure height for each individual axis element.
        Defaults to the golden aspect.

    sharex, sharey : bool or {'none', 'all', 'row', 'col'}, default: False
        Controls sharing of properties among x (*sharex*) or y (*sharey*)
        axes:

        - True or 'all': x- or y-axis will be shared among all subplots.
        - False or 'none': each subplot x- or y-axis will be independent.
        - 'row': each subplot row will share an x- or y-axis.
        - 'col': each subplot column will share an x- or y-axis.

        When subplots have a shared x-axis along a column, only the x tick
        labels of the bottom subplot are created. Similarly, when subplots
        have a shared y-axis along a row, only the y tick labels of the first
        column subplot are created. To later turn other subplots' ticklabels
        on, use `~matplotlib.axes.Axes.tick_params`.

        When subplots have a shared axis that has units, calling
        `~matplotlib.axis.Axis.set_units` will update each axis with the
        new units.

    squeeze : bool, default: True
        - If True, extra dimensions are squeezed out from the returned
          array of `~matplotlib.axes.Axes`:

          - if only one subplot is constructed (nrows=ncols=1), the
            resulting single Axes object is returned as a scalar.
          - for Nx1 or 1xM subplots, the returned object is a 1D numpy
            object array of Axes objects.
          - for NxM, subplots with N>1 and M>1 are returned as a 2D array.

        - If False, no squeezing at all is done: the returned Axes object is
          always a 2D array containing Axes instances, even if it ends up
          being 1x1.

    width_ratios : array-like of length *ncols*, optional
        Defines the relative widths of the columns. Each column gets a
        relative width of ``width_ratios[i] / sum(width_ratios)``.
        If not given, all columns will have the same width.  Equivalent
        to ``gridspec_kw={'width_ratios': [...]}``.

    height_ratios : array-like of length *nrows*, optional
        Defines the relative heights of the rows. Each row gets a
        relative height of ``height_ratios[i] / sum(height_ratios)``.
        If not given, all rows will have the same height. Convenience
        for ``gridspec_kw={'height_ratios': [...]}``.

    subplot_kw : dict, optional
        Dict with keywords passed to the
        `~matplotlib.figure.Figure.add_subplot` call used to create each
        subplot.

    gridspec_kw : dict, optional
        Dict with keywords passed to the `~matplotlib.gridspec.GridSpec`
        constructor used to create the grid the subplots are placed on.

    **fig_kw
        All additional keyword arguments are passed to the
        `.pyplot.figure` call.

    Returns
    -------
    fig : `.Figure`

    ax : `~matplotlib.axes.Axes` or array of Axes
        *ax* can be either a single `~.axes.Axes` object, or an array of Axes
        objects if more than one subplot was created.  The dimensions of the
        resulting array can be controlled with the squeeze keyword, see above.

        Typical idioms for handling the return value are::

            # using the variable ax for single a Axes
            fig, ax = plt.subplots()

            # using the variable axs for multiple Axes
            fig, axs = plt.subplots(2, 2)

            # using tuple unpacking for multiple Axes
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        The names ``ax`` and pluralized ``axs`` are preferred over ``axes``
        because for the latter it's not clear if it refers to a single
        `~.axes.Axes` instance or a collection of these.

    See Also
    --------
    .pyplot.figure
    .pyplot.subplot
    .pyplot.axes
    .Figure.subplots
    .Figure.add_subplot
    """
    if "figsize" in fig_kw:
        fig_kw.pop("figsize")
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

    gridspec_kw = fig_kw.get("gridspec_kw") or {}
    width_ratios = fig_kw.get("width_ratios") or gridspec_kw.get("width_ratios")
    height_ratios = fig_kw.get("height_ratios") or gridspec_kw.get("height_ratios")

    _figsize = figsize(
        nrows,
        ncols,
        scale=scale,
        aspect=aspect,
        width_ratios=width_ratios,
        height_ratios=height_ratios,
    )

    return plt.subplots(  # type: ignore[no-any-return]
        nrows=nrows,
        ncols=ncols,
        sharex=sharex,
        sharey=sharey,
        squeeze=squeeze,
        subplot_kw=subplot_kw,
        gridspec_kw=gridspec_kw,
        height_ratios=height_ratios,
        width_ratios=width_ratios,
        figsize=_figsize,
        **fig_kw,
    )
