import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
import conftest
import re

def highlight(element, page, color='orange'):
    page.evaluate(f'el => {{ el.style.outline = "3px solid {color}"; el.style.background = "rgba(255,0,0,0.1)"; }}', element)


def test_fish_icon_loads(print_var,echo_var,file_path="html/personal_signature.html", color_scheme="light", highlight_color="orange", my_browser_name="chromium", headless_var=True):
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

@pytest.mark.asyncio
async def test_google_search(setup_browser):
    page = setup_browser
    print("Testing google search...")
    # Wait for the element to be visible (async API)
    assert await page.get_by_label("Main Header Nav").get_by_role("link", name="Let's Chat").is_visible(), "Let's Chat link not visible"
    assert await page.get_by_role("link", name="Thoughts").is_visible(), "Thoughts link not visible"
    assert await page.get_by_role("link", name="Tools").is_visible(), "Tools link not visible"
    assert await page.locator("a").filter(has_text="Other Stuff").is_visible(), "Other Stuff link not visible"
    assert await page.get_by_role("banner").get_by_role("link", name="Fishy").is_visible(), "Fishy link not visible"
    assert await page.locator("#wp--skip-link--target").get_by_role("figure").filter(has_text=re.compile(r"^$")).locator("img").is_visible(), "Skip link image not visible"
    assert await page.get_by_role("heading", name="Hello.").is_visible(), "Hello heading not visible"
    assert await page.get_by_role("heading", name="I'm Fishy.").is_visible(), "I'm Fishy heading not visible"
    # Optionally pause for debugging
    # await page.pause()
