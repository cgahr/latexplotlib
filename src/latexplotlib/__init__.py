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
    "convert_inches_to_pt",
    "convert_pt_to_inches",
    "figsize",
    "size",
    "subplots",
    "__version__",
]

purge_old_styles(__path__)
make_styles_available(__path__)
