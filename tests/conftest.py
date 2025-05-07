import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

debug_var = True # Set to True to run in non-headless mode

@pytest.fixture(scope="session")
def headless_var():
    """Should run headless unless debug_var is True"""
    if debug_var:
        return False
    else:
        return True

@pytest.fixture(scope="session")
def slow_mo_var():
    """Should be set to 250ms unless debug_var is True, in which case it should be set to 1000ms"""
    if debug_var:
        return 1000
    else:
        return 250

@pytest.fixture(scope="session")
def print_var():
    print("print_var")
    yield
    print("print_var done")

@pytest.fixture(scope="session", autouse=True)
def echo_var(print_var):
    print("echo_var")
    yield
    print("echo_var done")