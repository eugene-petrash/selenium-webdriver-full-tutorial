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
            sticker = duck.find_element(By.CSS_SELECTOR, '.sticker')
            sticker_type = sticker.get_attribute("textContent")
            print("Sticker '" + sticker_type + "' is detected")
            assert len(duck.find_elements(By.CSS_SELECTOR, '.sticker')) == 1
            print("This sticker is only one for this duck")
        except NoSuchElementException:
            print("I do not find any stickers. That's why test is fail.")
            assert False
