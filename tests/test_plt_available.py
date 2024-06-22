import matplotlib.pyplot as plt
import pytest

import latexplotlib as lpl


def test_plt_functions_available():
    assert lpl.style == plt.style


@pytest.mark.parametrize("function", lpl._latexplotlib.__all__)
def test_lpl_functions_available(function: str):
    assert getattr(lpl, function) == getattr(lpl._latexplotlib, function)


@pytest.mark.parametrize("function", lpl._latexplotlib.__all__)
def test_lpl_doesnt_overwrite_existing_in_plt(function):
    if function == "subplots":
        assert True
    else:
        assert function not in dir(plt)


def test_non_existent_raises():
    with pytest.raises(AttributeError, match="matplotlib.pyplot"):
        lpl.doesnt_exist  # noqa: B018
