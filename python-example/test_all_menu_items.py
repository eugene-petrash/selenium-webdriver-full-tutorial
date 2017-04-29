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


def test_example(driver):
    pass
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit][ name=login]").click()
    menu_items = driver.find_elements(By.CSS_SELECTOR, "li#app-")
    menu_items_count = len(menu_items)
    i = 0
    while i < menu_items_count:
        menu_items = driver.find_elements(By.CSS_SELECTOR, "li#app-")
        menu_items[i].click()
        page_h1 = driver.find_element(By.CSS_SELECTOR, "h1")
        print("H1: " + page_h1.text)
        i += 1
        menu_subitems = driver.find_elements(By.CSS_SELECTOR, "li#app- .docs span.name")
        menu_subitems_count = len(menu_subitems)
        if menu_subitems_count > 0:
            s = 0
            while s < menu_subitems_count:
                menu_subitems = driver.find_elements(By.CSS_SELECTOR, "li#app- .docs span.name")
                menu_subitems[s].click()
                page_h1 = driver.find_element(By.CSS_SELECTOR, "h1")
                print("H1: " + page_h1.text)
                s += 1