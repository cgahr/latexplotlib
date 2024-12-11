from typing import Any

from ._cleanup import purge_old_styles
from ._config import size
from ._latexplotlib import (
    convert_inches_to_pt,
    convert_pt_to_inches,
    figsize,
    subplots,
)
from ._styles import make_styles_available
from ._version import __version__

__all__ = [
    "__version__",
    "convert_inches_to_pt",
    "convert_pt_to_inches",
    "figsize",
    "size",
    "subplots",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    import matplotlib.pyplot as plt

    return getattr(plt, name)


purge_old_styles(__path__)
make_styles_available(__path__)
