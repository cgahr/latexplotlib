from ._latexplotlib import *
from ._version import __version__


def _make_styles_available() -> None:
    from pathlib import Path

    import matplotlib.pyplot as plt

    lpl_styles = plt.style.core.read_style_directory(
        Path(__path__[0]) / "styles"  # noqa: F405
    )

    plt.style.core.update_nested_dict(plt.style.library, lpl_styles)
    plt.style.core.available[:] = sorted(plt.style.library.keys())


_make_styles_available()
