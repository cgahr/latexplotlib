from pathlib import Path

import latexplotlib  # noqa: F401
import matplotlib.pyplot as plt
import pytest


@pytest.mark.parametrize("style", Path("src/latexplotlib/styles/").iterdir())
def test_styles_are_usable(style):
    plt.style.use(style.stem)
