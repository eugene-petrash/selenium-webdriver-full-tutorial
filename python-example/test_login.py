import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@name='login']")))
    driver.find_element(By.XPATH, "//button[@name='login']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Statistics')]")))
