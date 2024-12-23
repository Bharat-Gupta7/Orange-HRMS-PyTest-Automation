from selenium.webdriver.common.by import By
from hrmshelper.selenium_helper import Selenium_Helper

class LoginPage(Selenium_Helper):

    username_webelement = (By.XPATH, "//input[@name='username']")
    password_webelement = (By.XPATH, "//input[@name='password']")
    login_webelement = (By.XPATH, "//button")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.webelement_enter(self.username_webelement, username)
        self.webelement_enter(self.password_webelement, password)
        self.webelement_click(self.login_webelement)
