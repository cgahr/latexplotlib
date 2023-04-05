"""Install latexplotlib.

This script (setup.py) will copy the matplotlib styles (*.mplstyle) into the
appropriate directory on your computer (OS dependent).

This code is based on SciencePlots:
https://github.com/garrettj403/SciencePlots/blob/master/setup.py

"""
import atexit
import logging
import shutil
from pathlib import Path

import matplotlib as mpl
from setuptools import setup
from setuptools.command.install import install

logger = logging.getLogger()


def install_styles() -> None:
    mpl_stylelib_dir = Path(mpl.get_configdir()) / "stylelib"
    if not mpl_stylelib_dir.exists():
        mpl_stylelib_dir.mkdir(parents=True)

    logger.info("Installing styles into {dir}", extra={"dir": mpl_stylelib_dir})
    for stylefile in Path("styles").glob("*.mplstyle"):
        logger.info("copying {style}", extra={"style": stylefile.name})
        shutil.copy(stylefile, mpl_stylelib_dir / stylefile.name)


class PostInstallMoveFile(install):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        atexit.register(install_styles)


setup(cmdclass={"install": PostInstallMoveFile})
