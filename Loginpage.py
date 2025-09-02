
from playwright.sync_api import expect

class Loginpage:
    # Initialize the Loginpage object with playwright instance and define element locators for the page.
    def __init__(self,page):
        self.page=page

        # Locators for login page elements
        self.username_locator=page.locator("//input[@placeholder='Enter your mail']")
        self.password_locator=page.locator("//input[@placeholder='Enter your password ']")
        self.submit_button=page.locator("//button[@type='submit']")

        #  Locators for error message
        self.invalid_email_error = page.locator("//p[text()='*Incorrect email!']")
        self.invalid_password_error = page.get_by_text("Incorrect password!")
        self.blank_email_password_error = page.get_by_text("Email and password required!")
        self.blank_password_error = page.get_by_text("Password required!")


    # LOGIN PAGE ACTIONS

    def login(self,username,password):

        # Wait for username input before typing
        expect(self.username_locator).to_be_visible()
        self.username_locator.fill(username)

        # Wait for password input before typing
        expect(self.password_locator).to_be_visible()
        self.password_locator.fill(password)

        # Wait for button, then click
        expect(self.submit_button).to_be_enabled()
        self.submit_button.click()


    def get_error_message(self):
        """Return whichever error is visible"""
        errors = [
            self.invalid_email_error,
            self.invalid_password_error,
            self.blank_email_password_error,
            self.blank_password_error,
        ]

        for error in errors:
            try:
                # Explicit wait for visibility and fetch text content
                expect(error).to_be_visible(timeout=4000)
                text = error.text_content()
                # remove spaces and returns the error message
                if text:
                    return text.strip()
            except Exception:
                continue
        # if no error found returns none
        return None