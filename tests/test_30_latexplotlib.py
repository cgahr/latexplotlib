import matplotlib as mpl
import pytest

from latexplotlib import _latexplotlib as lpl

GOLDEN_RATIO = (5**0.5 + 1) / 2


def test_constants():
    assert lpl.GOLDEN_RATIO


@pytest.mark.parametrize("value", [123.234, 23.4576585, 234])
def test__round(value):
    assert int(10 * value) / 10 == lpl._round(value)


def test_convert_pt_to_inches():
    val = 250 * 864
    ret = 12 * 249
    assert ret == lpl.convert_pt_to_inches(val)


@pytest.mark.parametrize("val", [123, 346, 34])
def test_inches_to_pt_and_back(val):
    assert val == lpl.convert_inches_to_pt(lpl.convert_pt_to_inches(val))


class TestFigsize:
    @pytest.fixture(autouse=True)
    def _set_size(self, monkeypatch, mocker, width, height):
        size = mocker.MagicMock()
        size.get = mocker.MagicMock(return_value=(width, height))
        monkeypatch.setattr(lpl, "size", size)

    @pytest.fixture(params=(1, 2, 3))
    def nrows(self, request):
        return request.param

    @pytest.fixture(params=(1, 2, 3))
    def ncols(self, request):
        return request.param

    @pytest.fixture(params=(0.5, 1.0, 2.0))
    def scale(self, request):
        return request.param

    @pytest.fixture
    def width(self):
        return 400

    @pytest.fixture
    def height(self):
        return 300

    def test_nrows_ncols(self, nrows, ncols, width, scale):
        width_in = ncols * lpl._round(lpl.convert_pt_to_inches(width))
        height_in = nrows * lpl._round(lpl.convert_pt_to_inches(width / GOLDEN_RATIO))

        res_width, res_height = lpl.figsize(nrows, ncols, scale=scale)
        assert res_width <= width_in * max(scale, 1)
        assert res_height <= height_in * max(scale, 1)

    @pytest.mark.parametrize("aspect", [GOLDEN_RATIO, 1, 2])
    def test_nrows_ncols_with_ratio(self, nrows, ncols, scale, width, aspect):
        width_in = ncols * lpl._round(lpl.convert_pt_to_inches(width))
        height_in = nrows * lpl._round(lpl.convert_pt_to_inches(width / aspect))

        res_width, res_height = lpl.figsize(nrows, ncols, scale=scale, aspect=aspect)
        assert res_width <= width_in * max(scale, 1)
        assert res_height <= height_in * max(scale, 1)

    @pytest.mark.parametrize("aspect", ["equal", "auto"])
    def test_str_ratio(self, nrows, ncols, scale, width, aspect):
        width_in = ncols * lpl._round(lpl.convert_pt_to_inches(width))
        height_in = nrows * lpl._round(lpl.convert_pt_to_inches(width))

        res_width, res_height = lpl.figsize(nrows, ncols, scale=scale, aspect=aspect)
        assert res_width <= width_in * max(scale, 1)
        assert res_height <= height_in * max(scale, 1)

    @pytest.fixture
    def small_enough(self):
        return 0.07

    def test_width_height_ratios(self, nrows, ncols, small_enough):
        height_ratios = [0.5, 1.0, 0.1][:nrows]
        width_ratios = [0.7, 1.0, 0.3][:ncols]

        res_width, res_height = lpl.figsize(
            nrows,
            ncols,
            scale=1,
            aspect=1,
            height_ratios=height_ratios,
            width_ratios=width_ratios,
        )

        ratio_theory = sum(height_ratios) / sum(width_ratios)
        ratio_test = res_height / res_width

        assert abs(1 - ratio_theory / ratio_test) <= small_enough

    @pytest.mark.parametrize("aspect", ["test", "asd", "min"])
    def test_invalid_aspect(self, aspect):
        with pytest.raises(ValueError, match="'aspect' a float, 'equal' or 'auto'."):
            lpl.figsize(1, 1, aspect=aspect)

    def test_negative_scale(self):
        with pytest.raises(ValueError, match="'scale' must be positive"):
            lpl.figsize(1, 1, scale=-1)


class TestSubplots:
    @pytest.fixture
    def _set_size(self, monkeypatch, mocker):
        size = mocker.MagicMock()
        size.get = mocker.MagicMock(return_value=(400, 300))
        monkeypatch.setattr(lpl, "size", size)

    def test_args(self):
        lpl.subplots(1, 1)
        lpl.subplots(1, ncols=1)
        lpl.subplots(nrows=1, ncols=1)
        lpl.subplots(2, 3)

    def test_deprecates_ratio(self):
        with pytest.warns(DeprecationWarning):
            lpl.subplots(1, 1, ratio=1)

    def test_deprecates_fraction(self):
        with pytest.warns(DeprecationWarning):
            lpl.subplots(1, 1, fraction=1)

    def test_warns_if_figsize_used(self):
        with pytest.warns(UserWarning):
            lpl.subplots(1, 1, figsize=(3, 4))

    @pytest.mark.skipif(
        mpl.__version_info__ < (3, 6), reason="requires matplotlib 3.6.0 or higher"
    )
    def test_width_height_ratios(self):
        lpl.subplots(
            2,
            3,
            aspect="equal",
            height_ratios=[0.25, 1.0],
            width_ratios=[0.25, 1.0, 0.25],
        )

    @pytest.mark.skipif(
        mpl.__version_info__ < (3, 6), reason="requires matplotlib 3.6.0 or higher"
    )
    def test_both_width_ratios(self):
        msg = "must not be defined both as parameter and as key in 'gridspec_kw"
        with pytest.raises(ValueError, match=msg):
            lpl.subplots(
                2,
                3,
                aspect="equal",
                gridspec_kw={"width_ratios": []},
                width_ratios=[0.25, 1.0, 0.25],
            )

    @pytest.mark.skipif(
        mpl.__version_info__ < (3, 6), reason="requires matplotlib 3.6.0 or higher"
    )
    def test_both_height_ratios(self):
        msg = "must not be defined both as parameter and as key in 'gridspec_kw"
        with pytest.raises(ValueError, match=msg):
            lpl.subplots(
                2,
                3,
                aspect="equal",
                gridspec_kw={"height_ratios": []},
                height_ratios=[0.25, 1.0],
            )

    @pytest.mark.usefixtures("_set_size", "_show")
    def test_plot(self):
        height_ratios = [0.25, 1.0]
        width_ratios = [0.25, 1.0, 0.25]

        fig, axes = lpl.subplots(
            2,
            3,
            aspect="equal",
            gridspec_kw={
                "height_ratios": height_ratios,
                "width_ratios": width_ratios,
            },
        )

        axes[0, 0].axis("off")
        axes[0, 1].imshow([[1.5, 2.5, 3.5, 4.5]], vmin=0, vmax=6)
        axes[0, 2].axis("off")

        axes[1, 0].imshow([[1.5], [2.5], [3.5], [4.5]], vmin=0, vmax=6)
        axes[1, 1].imshow(
            [[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]], vmin=0, vmax=6
        )
        axes[1, 2].imshow([[1.5], [2.5], [3.5], [4.5]], vmin=0, vmax=6)

        fig.suptitle("test")

    @pytest.mark.usefixtures("_set_size", "_show")
    def test_plot2(self):
        fig, axes = lpl.subplots(
            1,
            2,
            aspect="equal",
            gridspec_kw={
                "height_ratios": [0.1],
                "width_ratios": [0.2, 1.0],
            },
        )
