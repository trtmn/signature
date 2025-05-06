import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
import conftest
import re

def highlight(element, page, color='orange'):
    page.evaluate(f'el => {{ el.style.outline = "3px solid {color}"; el.style.background = "rgba(255,0,0,0.1)"; }}', element)


def test_fish_icon_loads(print_var,echo_var,file_path="html/personal_signature.html", color_scheme="light", highlight_color="orange", my_browser_name="chromium", headless_var=False):
    abs_path = Path(file_path).resolve()
    with sync_playwright() as p:
        print(f"Testing {file_path}")
        browser_launcher = getattr(p, my_browser_name)
        browser = browser_launcher.launch(headless=headless_var)
        context = browser.new_context(color_scheme=color_scheme)
        page = context.new_page()
        page.goto(f"file://{abs_path}")
        fish_icon = page.query_selector('#fish-icon')
        assert fish_icon is not None, "Fish icon not found"
        # Highlight the fish icon element
        highlight(fish_icon, page, color=highlight_color)
        # time.sleep(1)
        assert fish_icon.is_visible(), "Fish icon is not visible"
        is_broken = page.evaluate('el => el.naturalWidth === 0 || el.naturalHeight === 0', fish_icon)
        assert not is_broken, "Fish icon image is broken (not loaded)"
        box = fish_icon.bounding_box()
        assert abs(box['height'] - 18) < 1, f"Fish icon height is not 18px, got {box['height']}"
        browser.close()
