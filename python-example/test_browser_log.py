import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_selenium_grid(driver):
    admin_login(driver)
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    products = driver.find_elements(By.XPATH, '//a[contains(@href, "product_id=")]')
    i = 0
    while i < len(products):
        products = driver.find_elements(By.XPATH, '//a[contains(@href, "product_id=")]')
        products[i].click()
        assert len(driver.find_elements(By.XPATH, '//h1[contains(., "Edit Product")]')) == 1
        log_types_list = driver.log_types
        for log_type in log_types_list:
            assert len(driver.get_log(log_type)) == 0
        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        i += 1


def admin_login(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[@name='login']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Statistics')]")))
    assert len(driver.find_elements(By.XPATH, "//h3[contains(.,'Statistics')]")) == 1