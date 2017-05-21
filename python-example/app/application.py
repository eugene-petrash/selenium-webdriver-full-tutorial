from selenium import webdriver
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart import Cart
from selenium.webdriver.support.wait import WebDriverWait


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.wait = WebDriverWait(self.driver, 10)
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart = Cart(self.driver)

    def quit(self):
        self.driver.quit()
