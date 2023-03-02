import matplotlib.pyplot as plt
import pytest


def pytest_addoption(parser):
    parser.addoption("--plot", action="store_true")


@pytest.fixture(autouse=True)
def close_plots():
    yield
    plt.close("all")


@pytest.fixture
def show(pytestconfig):
    yield
    if pytestconfig.getoption("plot"):
        plt.show(block=True)
