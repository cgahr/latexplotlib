from collections.abc import Sequence
from pathlib import Path

from matplotlib.pyplot import style


def make_styles_available(path: Sequence[str]) -> None:
    lpl_styles = style.core.read_style_directory(Path(path[0]) / "styles")

    style.core.update_nested_dict(style.library, lpl_styles)
    style.core.available[:] = sorted(style.library.keys())
