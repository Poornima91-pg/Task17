
from playwright.sync_api import expect

class Homepage:

    # Initialize the Homepage object with playwright instance and define element locators for the page.
    def __init__(self, page):
        self.page = page

        # Locators for logout functionality
        self.logout_dropdown = page.locator("id=profile-click-icon")
        self.logout_button = page.locator("//div[text()='Log out']")

        # Locator for popup alert close button (✕ icon)
        self.alert_button = page.locator("//button[text()='✕']")


    # LOGOUT ACTIONS

    def logout(self):

        # wait for alert button to be enabled and Handle alert button (✕)
        expect(self.alert_button).to_be_enabled(timeout=10000)
        self.alert_button.click()

        # wait for logout dropdown to be enabled and clicks on it
        expect(self.logout_dropdown).to_be_enabled(timeout=10000)
        self.logout_dropdown.click()

        # wait for logout button to be enabled and clicks on logout
        expect(self.logout_button).to_be_enabled(timeout=10000)
        self.logout_button.click()
