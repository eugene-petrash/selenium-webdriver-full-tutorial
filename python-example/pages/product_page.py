from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, number=0):
        products_list = self.driver.find_elements(By.CSS_SELECTOR, '#box-campaigns a')
        products_list[number].click()

    def add_product_to_cart(self, i=0):
        self.full_page_helper()
        counter_new_value = self.fill_product_parameters(i)
        self.submit_product_adding(counter_new_value)

    def submit_product_adding(self, counter_new_value):
        self.driver.find_element(By.CSS_SELECTOR, 'button[name="add_cart_product"]').click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                        '//div[@id="cart"]//span[contains(@class, "quantity") and contains(., "' + counter_new_value + '")]')))

    def fill_product_parameters(self, i):
        options_size = self.driver.find_element(By.CSS_SELECTOR, 'select[name="options[Size]"]')
        options_size.click()
        sizes_list = options_size.find_elements(By.CSS_SELECTOR, 'option:not([selected="selected"])')
        sizes_list[i].click()
        counter_default_value = self.driver.find_element(By.XPATH,
                                                         '//div[@id="cart"]//span[contains(@class, "quantity")]').text
        counter_new_value = str(int(counter_default_value) + 1)
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="quantity"]').clear()
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="quantity"]').send_keys('1')
        return counter_new_value

    def full_page_helper(self):
        if self.is_element_present('#view-full-page a'):
            self.driver.find_element(By.CSS_SELECTOR, '#view-full-page a').click()

    def is_element_present(self, locator):
        return len(self.driver.find_elements(By.CSS_SELECTOR, locator)) > 0
