import pytest
from pathlib import Path
import re
from playwright.sync_api import sync_playwright



def highlight(element, page, color='orange'):
    # This function is for sync API; for async, use await page.evaluate(...)
    pass


def test_fish_icon_loads(headless_var, slow_mo_var, file_path="signatures/personal_signature.html", color_scheme="light", highlight_color="orange", my_browser_name="chromium"):
    abs_path = Path(file_path).resolve()
    with sync_playwright() as p:
        print(f"Testing {file_path}")
        browser_launcher = getattr(p, my_browser_name)
        browser = browser_launcher.launch(headless=headless_var, slow_mo=slow_mo_var)
        context = browser.new_context(color_scheme=color_scheme)
        page = context.new_page()
        page.goto(f"file://{abs_path}")
        fish_icon = page.query_selector('#fish-icon')
        assert fish_icon is not None, "Fish icon not found"
      
        assert fish_icon.is_visible(), "Fish icon is not visible"
        is_broken = page.evaluate('el => el.naturalWidth === 0 || el.naturalHeight === 0', fish_icon)
        assert not is_broken, "Fish icon image is broken (not loaded)"
        box = fish_icon.bounding_box()
        assert abs(box['height'] - 18) < 1, f"Fish icon height is not 18px, got {box['height']}"
        browser.close()

def test_gravatar_image_loads(headless_var, slow_mo_var, file_path="signatures/personal_signature.html", color_scheme="light", highlight_color="orange", my_browser_name="chromium"):
    abs_path = Path(file_path).resolve()
    with sync_playwright() as p:
        print(f"Testing {file_path}")
        browser_launcher = getattr(p, my_browser_name)
        browser = browser_launcher.launch(headless=headless_var, slow_mo=slow_mo_var)
        context = browser.new_context(color_scheme=color_scheme)
        page = context.new_page()
        page.goto(f"file://{abs_path}")
        gravatar = page.query_selector('#gravatar')
        assert gravatar is not None, "Gravatar not found"
        # Highlight the gravatar element
        # highlight(gravatar, page, color=highlight_color)
        assert gravatar.is_visible(), "Gravatar image is not visible"
        box = gravatar.bounding_box()
        assert box['width'] > 0, "Gravatar image has no width"
        assert box['height'] > 0, "Gravatar image has no height"
        browser.close()


@pytest.mark.parametrize("color_scheme,expected_color", [
    ("light", "#111111"),  # Dark gray text for light mode
    ("dark", "#FFFFFF") # White text for dark mode
])
def test_font_color_based_on_background(headless_var,slow_mo_var, color_scheme, expected_color, file_path="signatures/personal_signature.html", highlight_color="orange", my_browser_name="chromium"):
    abs_path = Path(file_path).resolve()
    with sync_playwright() as p:
        print(f"Testing {file_path} with {color_scheme} color scheme")
        browser_launcher = getattr(p, my_browser_name)
        browser = browser_launcher.launch(headless=headless_var)
        context = browser.new_context(color_scheme=color_scheme)
        page = context.new_page()
        page.goto(f"file://{abs_path}")
        # Try to select a main text element, fallback to <td> if .signature-text does not exist
        text_element = page.query_selector('.signature-text')
        if text_element is None:
            text_element = page.query_selector('td')
        assert text_element is not None, "Signature text element not found"
        actual_color = page.evaluate('el => window.getComputedStyle(el).color', text_element)
        # Convert RGB color to hex format for comparison
        actual_color_hex = page.evaluate('''(color) => {
            const rgb = color.match(/\d+/g);
            if (!rgb) return color;
            return '#' + rgb.map(x => {
                const hex = parseInt(x).toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }).join('');
        }''', actual_color)
        try:
            assert actual_color_hex.lower() == expected_color.lower(), f"Expected text color {expected_color}, got {actual_color_hex}"
        except AssertionError:
            page.pause()
            raise
        browser.close()
        