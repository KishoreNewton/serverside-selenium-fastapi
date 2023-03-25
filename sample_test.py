import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(params=["headless", "headful"])
def mode(request):
    return request.param

@pytest.fixture
def driver(mode):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if mode == "headful":
        chrome_options.add_argument("--start-maximized")

    if mode == "headless":
        chrome_options.add_argument("--headless")

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=chrome_options,
    )

    yield driver
    driver.quit()

def test_example(driver):
    driver.get("https://www.example.com")
    assert "Example Domain" in driver.title

def test_google(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title
