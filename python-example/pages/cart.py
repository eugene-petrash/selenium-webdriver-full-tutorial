from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Cart:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.find_element(By.CSS_SELECTOR, '#cart a[href="http://localhost/litecart/en/checkout"]').click()

    @property
    def cart_items(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.items.table.table-striped.data-table tbody .item')))
        return self.driver.find_elements(By.CSS_SELECTOR, '.items.table.table-striped.data-table tbody .item')

    def remove_product_from_cart(self, i, total_products_count):
        self.check_cart_items_count(total_products_count, i)
        cart_items = self.cart_items
        self.check_total_price(cart_items, self.driver)
        cart_items[0].find_element(By.CSS_SELECTOR, 'button[title="Remove"]').click()
        self.wait.until(EC.staleness_of(cart_items[0]))
        if i < (total_products_count - 1):
            cart_items = self.cart_items
            self.check_total_price(cart_items, self.driver)
        elif i == (total_products_count - 1):
            assert len(self.driver.find_elements(By.XPATH, '//em[contains(., "There are no items in your cart")]')) == 1

    def check_total_price(self, cart_items, driver):
        subtotal = 0
        i = 0
        while i < len(cart_items):
            item_price = float((cart_items[i].find_element(By.XPATH, './/button[@title="Remove"]/../preceding-sibling::td[position()=1]').text)[1:])
            subtotal += item_price
            i += 1
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#box-checkout-shipping .price')))
        zone_based_shipping = float((driver.find_element(By.CSS_SELECTOR, '#box-checkout-shipping .price').text)[3:])
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#box-checkout-payment .price')))
        cash_on_delivery = float((driver.find_element(By.CSS_SELECTOR, '#box-checkout-payment .price').text)[3:])
        payment_due = subtotal + zone_based_shipping + cash_on_delivery
        assert len(driver.find_elements(By.XPATH, '//div[@id="box-checkout-summary"]//tfoot//strong[contains(., "$' + str(payment_due) + '")]')) == 1

    def check_cart_items_count(self, total_products_count, i):
        assert len(self.cart_items) == total_products_count - i

