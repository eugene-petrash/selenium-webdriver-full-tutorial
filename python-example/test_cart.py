import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome(desired_capabilities={'chromeOptions': {'args': ['--start-fullscreen']}})
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_cart(driver):
    wait = WebDriverWait(driver, 10) # seconds
    total_products_count = 3
    i = 0
    while i < total_products_count:
        add_product_to_cart(driver, wait, i)
        i += 1
    driver.find_element(By.CSS_SELECTOR, '#cart a[href="http://localhost/litecart/en/checkout"]').click()
    cart_items = driver.find_elements(By.CSS_SELECTOR, '.items.table.table-striped.data-table tbody .item')
    assert len(cart_items) == total_products_count
    i = 0
    while i < total_products_count:
        remove_product_from_cart(driver, wait, i, total_products_count)
        i += 1


def add_product_to_cart(driver, wait, i=None):
    driver.get("http://localhost/litecart/")
    products_list = driver.find_elements(By.CSS_SELECTOR, '#box-campaigns a')
    products_list[0].click()
    if is_element_present('#view-full-page a', driver):
        driver.find_element(By.CSS_SELECTOR, '#view-full-page a').click()
    options_size = driver.find_element(By.CSS_SELECTOR, 'select[name="options[Size]"]')
    options_size.click()
    sizes_list = options_size.find_elements(By.CSS_SELECTOR, 'option:not([selected="selected"])')
    sizes_list[i].click()
    counter_default_value = driver.find_element(By.XPATH, '//div[@id="cart"]//span[contains(@class, "quantity")]').text
    counter_new_value = str(int(counter_default_value) + 1)
    driver.find_element(By.CSS_SELECTOR, 'input[name="quantity"]').clear()
    driver.find_element(By.CSS_SELECTOR, 'input[name="quantity"]').send_keys('1')
    driver.find_element(By.CSS_SELECTOR, 'button[name="add_cart_product"]').click()
    wait.until(EC.presence_of_element_located((By.XPATH,
                                               '//div[@id="cart"]//span[contains(@class, "quantity") and contains(., "' + counter_new_value + '")]')))


def is_element_present(locator, driver):
    return len(driver.find_elements(By.CSS_SELECTOR, locator)) > 0


def remove_product_from_cart(driver, wait, i, total_products_count):
    cart_items = driver.find_elements(By.CSS_SELECTOR, '.items.table.table-striped.data-table tbody .item')
    check_total_price(cart_items, driver)
    cart_items[0].find_element(By.CSS_SELECTOR, 'button[title="Remove"]').click()
    wait.until(EC.staleness_of(cart_items[0]))
    cart_items = driver.find_elements(By.CSS_SELECTOR, '.items.table.table-striped.data-table tbody .item')
    if i < (total_products_count - 1):
        check_total_price(cart_items, driver)
        print('i=' + str(i))
    elif i == (total_products_count - 1):
        assert len(driver.find_elements(By.XPATH, '//em[contains(., "There are no items in your cart")]')) == 1
        print('i: ' + str(i))


def check_total_price(cart_items, driver):
    subtotal = 0
    i = 0
    while i < len(cart_items):
        item_price = float((cart_items[i].find_element(By.XPATH, './/button[@title="Remove"]/../preceding-sibling::td[position()=1]').text)[1:])
        subtotal += item_price
        i += 1
    zone_based_shipping = float((driver.find_element(By.CSS_SELECTOR, '#box-checkout-shipping .price').text)[3:])
    cash_on_delivery = float((driver.find_element(By.CSS_SELECTOR, '#box-checkout-payment .price').text)[3:])
    payment_due = subtotal + zone_based_shipping + cash_on_delivery
    assert len(driver.find_elements(By.XPATH, '//div[@id="box-checkout-summary"]//tfoot//strong[contains(., "$' + str(payment_due) + '")]')) == 1
