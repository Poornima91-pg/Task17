
from playwright.sync_api import expect
from Task17.pages.Loginpage import Loginpage
from Task17.pages.Homepage import Homepage
from Task17 import config
import pytest
import time

def test_validate_login_elements(setup):
    """Validate Username, Password, and Submit button presence"""
    page = setup
    page.goto("https://v2.zenclass.in/login")
    login= Loginpage(page)

    try:
        # Check username field is visible and enabled
        expect(login.username_locator).to_be_visible()
        expect(login.username_locator).to_be_enabled()

        # Check password field is visible and enabled
        expect(login.password_locator).to_be_visible()
        expect(login.password_locator).to_be_enabled()

        # Check submit button is visible and enabled
        expect(login.submit_button).to_be_visible()
        expect(login.submit_button).to_be_enabled()

        # take screenshots
        page.screenshot(path="../validate_login_elements.png")

    except Exception as e:
        # if failed raise exception
        pytest.fail(f"Element validation failed: {e}")
        page.screenshot(path="validate_login_elements_error.png")




def test_successful_login_logout(setup):
    """Test successful login and logout"""
    page = setup
    login = Loginpage(page)
    logout = Homepage(page)

    try:
        # Open login page
        page.goto("https://v2.zenclass.in/login")

        # Perform login
        login.login(config.VALID_USERNAME, config.VALID_PASSWORD)

        # Validate login success by waiting for dashboard and take screenshots
        page.wait_for_url("**/dashboard", timeout=5000)
        expect(page).to_have_url("https://v2.zenclass.in/dashboard")
        # page.wait_for_timeout(3000)
        # page.wait_for_load_state()
        page.screenshot(path="../valid_login.png")

        # Perform logout
        logout.logout()

        # Validate logout success (login page should be opened)
        expect(login.username_locator).to_be_visible()

    except Exception as e:
        # if failed raise exception
        pytest.fail(f"Login/Logout failed: {e}")


@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("", "","*Incorrect email!"),   # Both empty
        ("", config.VALID_PASSWORD, "*Incorrect email!"),  # Empty email
        (config.VALID_USERNAME, "","Password required!"),            # Empty password
        (config.INVALID_USERNAME, config.VALID_PASSWORD, "*Incorrect email!"),  # Wrong email
        (config.VALID_USERNAME, config.INVALID_PASSWORD,"Incorrect password!") # Wrong password
    ]
)
def test_unsuccessful_login_scenarios(setup, username, password, expected_error):
    """Test multiple invalid login cases using parametrize"""
    page = setup
    login = Loginpage(page)

    try:
        # Go to login page
        page.goto("https://v2.zenclass.in/login")

        # Try to login with given credentials
        login.login(username, password)

        # Validate error message and take screenshots
        error_message = login.get_error_message()
        assert error_message == expected_error,(f"Expected error '{expected_error}' but got '{error_message}'")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        page.screenshot(path=f"invalid_login_{timestamp}.png")

        # Validate we are still on login page (not redirected to dashboard)
        expect(page).to_have_url("https://v2.zenclass.in/login")
        expect(page).not_to_have_url("https://v2.zenclass.in/dashboard")

    except AssertionError as e:
        # if failed raise exception

        pytest.fail(f"Assertion failed: {e}")
