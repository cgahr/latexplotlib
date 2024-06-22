import pytest

import latexplotlib._cleanup as cleanup


def test_styles():
    old_names = {
        "latex9pt-minimal.mplstyle",
        "latex9pt.mplstyle",
        "latex10pt-minimal.mplstyle",
        "latex10pt.mplstyle",
        "latex11pt-minimal.mplstyle",
        "latex11pt.mplstyle",
        "latex12pt-minimal.mplstyle",
        "latex12pt.mplstyle",
    }
    assert old_names == cleanup.STYLES


class TestPurgeOldStyles:
    @pytest.fixture()
    def purged_str(self, monkeypatch):
        s = "banana"
        monkeypatch.setattr(cleanup, "_PURGED_OLD", s)
        return s

    @pytest.fixture(autouse=True)
    def config(self, purged_str, monkeypatch):
        default = {purged_str: False}
        monkeypatch.setattr(cleanup, "config", default)

        def fun():
            assert default[purged_str] is True, "'is_purged'-flag is not set to True"

        self.assert_purged_true = fun
        return default

    @pytest.fixture()
    def styles_folder(self, monkeypatch):
        styles_folder = "new"
        monkeypatch.setattr(cleanup, "STYLES_FOLDER", styles_folder)
        return styles_folder

    @pytest.fixture()
    def new(self, tmp_path, styles_folder):
        path = tmp_path / styles_folder
        path.mkdir()
        return path

    @pytest.fixture()
    def stylelib(self, monkeypatch):
        stylelib = "old"
        monkeypatch.setattr(cleanup, "STYLELIB", stylelib)
        return stylelib

    @pytest.fixture()
    def old(self, tmp_path, stylelib):
        path = tmp_path / stylelib
        path.mkdir()
        return path

    @pytest.fixture(autouse=True)
    def mock_configdir(self, mocker, tmp_path):
        return mocker.patch(
            "latexplotlib._cleanup.get_configdir", return_value=tmp_path
        )

    def test_is_purged(self, config, purged_str, mock_configdir):
        config[purged_str] = True
        cleanup.purge_old_styles([])

        assert not mock_configdir.called
        self.assert_purged_true()

    def test_old_styledir_not_exists(self, mock_configdir, old):
        old.rmdir()

        cleanup.purge_old_styles([])
        mock_configdir.assert_called_once()

        self.assert_purged_true()

    def test_empty_dir(self, mock_configdir, new):
        cleanup.purge_old_styles([new.parent])
        mock_configdir.assert_called_once()

        self.assert_purged_true()

    @pytest.fixture(
        params=[
            "latex9pt-minimal.mplstyle",
            "latex9pt.mplstyle",
            "latex10pt-minimal.mplstyle",
            "latex10pt.mplstyle",
            "latex11pt-minimal.mplstyle",
            "latex11pt.mplstyle",
            "latex12pt-minimal.mplstyle",
            "latex12pt.mplstyle",
        ]
    )
    def mplstyle(self, request):
        return request.param

    def test_removes_file(self, new, old, mplstyle, mocker):
        cmp_spy = mocker.spy(cleanup.filecmp, "cmp")

        new_file = new / mplstyle
        old_file = old / mplstyle
        new_file.touch()
        old_file.touch()
        assert new_file.exists()
        assert old_file.exists()

        cleanup.purge_old_styles([new.parent])

        assert new_file.exists()
        assert not old_file.exists()
        cmp_spy.assert_called_once_with(new_file, old_file, shallow=False)

    def test_file_different(self, new, old, mplstyle, mocker):
        cmp_spy = mocker.spy(cleanup.filecmp, "cmp")

        new_file = new / mplstyle
        old_file = old / mplstyle
        new_file.touch()

        with old_file.open("w") as fh:
            fh.write("1\n")

        assert new_file.exists()
        assert old_file.exists()

        cleanup.purge_old_styles([new.parent])

        assert new_file.exists()
        assert old_file.exists()
        cmp_spy.assert_called_once_with(new_file, old_file, shallow=False)
