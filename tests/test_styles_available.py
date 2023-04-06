from pathlib import Path

import matplotlib.pyplot as plt
import pytest

import latexplotlib as lpl  # noqa: F401


@pytest.mark.parametrize("style", Path("src/latexplotlib/styles/").iterdir())
def test_styles_are_usable(style):
    plt.style.use(style.stem)
