import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_check_stickers(driver):
    driver.get("http://localhost/litecart/")
    driver.find_element(By.XPATH, "//div[@class='content']//a[contains(., 'Rubber Ducks')]").click()
    all_ducks = driver.find_elements(By.CSS_SELECTOR, '.col-xs-halfs.col-sm-thirds.col-md-fourths.col-lg-fifths')
    for duck in all_ducks:
        try:
            duck.find_element(By.CSS_SELECTOR, '.sticker.sale')
            assert len(duck.find_elements(By.CSS_SELECTOR, '.sticker:not(.sale)')) < 1
            print("Only one sticker 'sale' is detected =)\n")
        except NoSuchElementException:
            try:
                print("Sticker 'sale' is not displayed =( . But maybe 'new' sticker displayed? =/")
                duck.find_element(By.CSS_SELECTOR, '.sticker.new')
                assert len(duck.find_elements(By.CSS_SELECTOR, '.sticker:not(.new)')) < 1
                print("Yes! Only one sticker 'new' is detected =)\n")
            except NoSuchElementException:
                print("Stickers is not displayed\n")
                assert False
