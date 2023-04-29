import filecmp
from pathlib import Path
from typing import List

from matplotlib import get_configdir

from ._config import _PURGED_OLD, config

STYLELIB = "stylelib"
STYLES = {
    "latex9pt-minimal.mplstyle",
    "latex9pt.mplstyle",
    "latex10pt-minimal.mplstyle",
    "latex10pt.mplstyle",
    "latex11pt-minimal.mplstyle",
    "latex11pt.mplstyle",
    "latex12pt-minimal.mplstyle",
    "latex12pt.mplstyle",
}
STYLES_FOLDER = "styles"


def purge_old_styles(path: List[str]) -> None:
    if config[_PURGED_OLD]:
        return

    old_styledir = Path(get_configdir()) / STYLELIB

    if not old_styledir.is_dir():
        config[_PURGED_OLD] = True
        return

    old_styles = {s.name for s in old_styledir.glob("latex*.mplstyle")}

    for style in STYLES & old_styles:
        if filecmp.cmp(
            Path(path[0]) / STYLES_FOLDER / style, old_styledir / style, shallow=False
        ):
            (old_styledir / style).unlink()

    config[_PURGED_OLD] = True
