import pytest
from datetime import datetime
from pathlib import Path
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define the base URL and login credentials
BaseUrl = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
Username = "Admin"
Password = "admin123"

@pytest.fixture(scope="class", autouse=True)
def browser_setup(request):
    """Fixture to set up the browser for tests."""
    options = Options()
    options.add_argument("--start-maximized")  # Open browser maximized
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)  # Initialize the WebDriver
    request.cls.driver = driver  # Assign driver to the test class
    yield driver
    driver.quit()  # Quit the browser after the test class is complete

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure pytest to generate HTML reports in a timestamped directory."""
    today = datetime.now()
    report_dir = Path("hrmsreports") / today.strftime("%Y%m%d")
    report_dir.mkdir(parents=True, exist_ok=True)  # Create the report directory if it doesn't exist
    report_path = report_dir / f"Report_{today.strftime('%Y%m%d%H%M%S')}.html"
    config.option.htmlpath = str(report_path)  # Specify the report path
    config.option.self_contained_html = True

def pytest_html_report_title(report):
    """Set the title for the HTML report."""
    report.title = "Orange HRMS Automation Test Report"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots for each test case."""
    # Capture the result of the test (whether it passed or failed)
    outcome = yield
    report = outcome.get_result()

    # Only capture a screenshot if the test has finished
    if report.when == "call":
        # Prepare the directory for screenshots inside hrmsreports/{today's directory}
        today = datetime.now().strftime("%Y%m%d")
        screenshot_dir = Path("hrmsreports") / today / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)  # Create the screenshots folder if it doesn't exist

        # Define the screenshot filename based on the test case name and result
        timestamp = time.strftime("%Y%m%d%H%M%S")
        test_name = item.nodeid.split("::")[-1]
        screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

        # Capture the screenshot
        if report.outcome == "failed" or report.outcome == "passed":
            # Save the screenshot
            item.cls.driver.save_screenshot(str(screenshot_path))
            print(f"Screenshot saved at: {screenshot_path}")

            # Add the screenshot to the report
            if "html" in item.config.option.plugins:
                extra = getattr(report, "extra", [])
                # Ensure that the screenshot is shown in the report
                screenshot_html_path = f"../screenshots/{test_name}_{timestamp}.png"  # Relative path for HTML report
                extra.append(pytest_html.extras.image(screenshot_html_path))  # Attach the screenshot to the HTML report
                report.extra = extra
