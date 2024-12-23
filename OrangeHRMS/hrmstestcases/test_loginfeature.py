import pytest
from conftest import *  # Importing shared configurations and fixtures
from hrmspages.LoginPage import LoginPage  # Importing the page object for the Login functionality

# Using the 'browser_setup' fixture defined in conftest.py for browser initialization and teardown
@pytest.mark.usefixtures("browser_setup")
class Test_login:

    @classmethod
    def setup_class(cls):
        """
        Setup method to initialize the web driver and navigate to the base URL.
        This is executed once before all tests in the class.
        """
        cls.driver.get(BaseUrl)  # Navigate to the application URL
        cls.login_page = LoginPage(cls.driver)  # Initialize the LoginPage object with the driver

    def test_valid_login(self):
        """
        Test case for verifying valid login functionality.
        It uses the login page object to enter credentials and submit the login form.
        """
        self.login_page.login(Username, Password)  # Perform login with valid credentials

    @classmethod
    def teardown_class(cls):
        """
        Teardown method to handle cleanup after all tests in the class.
        Since driver cleanup is managed by the fixture, this method is currently empty.
        """
        pass  # Driver teardown is handled in the 'browser_setup' fixture
