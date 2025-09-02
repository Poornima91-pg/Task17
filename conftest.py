# conftest.py

import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def setup():
    # Start Playwright
    with sync_playwright() as playwright:
        # Launch browser (headless=False → browser window is visible)
        browser = playwright.chromium.launch(headless=False)

        # Create a fresh context
        context = browser.new_context()

        # Open a new page (tab)
        page = context.new_page()

        # Provide the page object to the test
        yield page

        # Cleanup after test finishes
        context.close()
        browser.close()