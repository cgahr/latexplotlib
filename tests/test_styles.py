# pylint: disable = import-error, missing-class-docstring, missing-function-docstring
# pylint: disable = missing-module-docstring, no-self-use, protected-access
# pylint: disable = redefined-outer-name, too-few-public-methods, too-many-arguments
# pylint: disable = unused-argument


from pathlib import Path

import matplotlib.pyplot as plt
import pytest

styles_folder = Path("styles/")


class TestStyles:
    @pytest.mark.parametrize("style", styles_folder.iterdir())
    def test_style(self, style, caplog):
        assert (
            style.suffix == ".mplstyle"
        ), f"The style '{style}' has an invalid suffix!"

        plt.style.use(style)
        if caplog.text != "":
            raise AssertionError(f"The style '{style}' is invalid: {caplog.text}")
