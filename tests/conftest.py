import pytest
from playwright.async_api import async_playwright

@pytest.fixture(scope="session")
def headless_var():
    return True

@pytest.fixture(scope="session")
def echo_var():
    print("echo_var")
    yield
    print("echo_var done")

@pytest.fixture(scope="session")
def print_var():
    print("print_var")
    yield
    print("print_var done")

@pytest.fixture(scope="session")
async def setup_browser(headless_var=True):
    print("Setting up browser...")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless_var, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://www.google.com")
        yield page
        print("Tearing down browser...")
        browser.close()


