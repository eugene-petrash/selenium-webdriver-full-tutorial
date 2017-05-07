import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import os


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome(desired_capabilities={'chromeOptions': {'args': ['--start-fullscreen']}})
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_add_product(driver):
    admin_login(driver)
    go_to_catalog_page(driver)
    go_to_add_product_page(driver)
    fill_product_form(driver)


def admin_login(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[@name='login']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Statistics')]")))
    assert len(driver.find_elements(By.XPATH, "//h3[contains(.,'Statistics')]")) == 1


def go_to_catalog_page(driver):
    driver.find_element(By.XPATH, '//ul[@id="box-apps-menu"]//span[contains(., "Catalog")]').click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Catalog')]")))
    assert len(driver.find_elements(By.XPATH, "//h1[contains(.,'Catalog')]")) == 1


def go_to_add_product_page(driver):
    driver.find_element(By.XPATH, '//a[contains(., "Add New Product")]').click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Add New Product')]")))
    assert len(driver.find_elements(By.XPATH, "//h1[contains(.,'Add New Product')]")) == 1


def fill_product_form(driver):
    product_name = random_string(10)
    go_to_tab('General', driver)
    fill_general_tab_form(product_name, driver)
    go_to_tab('Information', driver)
    fill_information_tab_form(driver)
    go_to_tab('Prices', driver)
    fill_prices_tab_form(driver)
    save_data(driver)
    check_product_in_admin_catalog(product_name, driver)


def go_to_tab(name, driver):
    driver.find_element(By.XPATH, '//ul[@class="nav nav-tabs"]//a[contains(., "' + name + '")]').click()


def fill_input(name, text, driver, clear=None):
    form = driver.find_element(By.CSS_SELECTOR, '.tab-content')
    if clear == True:
        form.find_element(By.CSS_SELECTOR, 'input[name="' + name + '"]').clear()
    form.find_element(By.CSS_SELECTOR, 'input[name="' + name + '"]').send_keys(text)


def choose_select(name, value, driver):
    select = driver.find_element(By.CSS_SELECTOR, 'select[name="' + name + '"]')
    select.click()
    select.find_element(By.CSS_SELECTOR, 'option[value="' + value + '"]').click()


def select_checkbox(name, driver):
    checkbox = driver.find_element(By.XPATH, '//input[contains(@type, "checkbox")]/parent::label[contains(., "' + name + '")]')
    checkbox.click()


def attach_image(driver):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image.jpg")
    driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(path)


def fill_general_tab_form(product_name, driver):
    driver.find_element(By.XPATH, '//label[contains(., "Enabled")]').click()
    fill_input("code", random_digits(10), driver)
    select_category("Rubber Ducks", driver)
    fill_input("name[en]", product_name, driver)
    fill_input("sku", random_string(5), driver)
    fill_input("gtin", random_string(5), driver)
    fill_input("taric", random_string(5), driver)
    choose_select("quantity_unit_id", "1", driver)
    fill_input("quantity", random_digits(3), driver, True)
    choose_select("default_category_id", "0", driver)
    choose_select("weight_class", "g", driver)
    fill_input("weight", random_digits(3), driver, True)
    select_checkbox("Male", driver)
    choose_select("dim_class", "cm", driver)
    fill_input("dim_x", random_digits(3), driver, True)
    fill_input("dim_y", random_digits(3), driver, True)
    fill_input("dim_z", random_digits(2), driver, True)
    choose_select("delivery_status_id", "1", driver)
    choose_select("sold_out_status_id", "2", driver)
    fill_input("date_valid_from", '05/11/2017', driver)
    fill_input("date_valid_to", '05/12/2017', driver)
    attach_image(driver)


def select_category(name, driver):
    driver.find_element(By.CSS_SELECTOR, 'input[data-name="' + name + '"]').click()


def fill_information_tab_form(driver):
    choose_select("manufacturer_id", "1", driver)
    choose_select("supplier_id", "", driver)
    fill_input("keywords", random_string(5), driver)
    fill_input("short_description[en]", random_string(7), driver)
    driver.find_element(By.XPATH, '//textarea[@name="description[en]"]/preceding-sibling::div[@contenteditable="true"]')\
        .send_keys(random_sentence(5, 10))
    driver.find_element(By.XPATH, '//textarea[@name="attributes[en]"]').send_keys(random_sentence(7, 15))
    fill_input("head_title[en]", random_string(8), driver)
    fill_input("meta_description[en]", random_string(8), driver)


def fill_prices_tab_form(driver):
    choose_select("purchase_price_currency_code", "USD", driver)
    fill_input("purchase_price", random_digits(2), driver, True)
    choose_select("tax_class_id", "1", driver)
    fill_input("prices[USD]", random_digits(3), driver, True)
    fill_input("gross_prices[USD]", random_digits(3), driver, True)
    fill_input("prices[EUR]", random_digits(3), driver, True)
    fill_input("gross_prices[EUR]", random_digits(3), driver, True)


def save_data(driver):
    driver.find_element(By.CSS_SELECTOR, 'button[name="save"]').click()
    actual_message = driver.find_element(By.XPATH, '//div[contains(@class, "alert alert-success")]').get_attribute("textContent")
    assert "Changes were successfully saved" in actual_message


def check_product_in_admin_catalog(name, driver):
    assert len(driver.find_elements(By.XPATH, '//table[@class="table table-striped data-table"]//a[contains(., "' + name + '")]')) > 0


def random_string(length):
    s = string.ascii_lowercase + string.digits
    return ''.join(random.sample(s,length))


def random_digits(length):
    d = string.digits
    return ''.join(random.sample(d,length))


def random_sentence(word_len, sentence_len):
    i=0
    sentence = ""
    while i < sentence_len:
        sentence += random_string(word_len) + " "
        i += 1
    return sentence
