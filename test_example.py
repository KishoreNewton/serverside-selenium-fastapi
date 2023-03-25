import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(params=["headless", "headful"])
def mode(request):
    return request.param

@pytest.fixture
def driver(mode):
    chrome_options = Options()

    if mode == "headless":
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=chrome_options,
        )
    else:
        driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()

def test_example(driver):
    driver.get("https://www.example.com")
    assert driver.title == "Example Domain"

def test_google(driver):
    driver.get("https://www.google.com")
    assert driver.title == "Google"
