import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import string


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_user_registration(driver):
    driver.get("http://localhost/litecart/")
    go_to_reg_user_page(driver)
    email, password = reg_user(driver)
    log_out(driver)
    log_in(driver, email, password)
    log_out(driver)


def reg_user(driver):
    reg_form = driver.find_element(By.CSS_SELECTOR, 'form[name="customer_form"]')
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="firstname"]').send_keys(random_string(10))
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="lastname"]').send_keys(random_string(10))
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="address1"]').send_keys(random_string(10))
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="postcode"]').send_keys(random_digits(5))
    reg_form.find_element(By.CSS_SELECTOR, 'select[name="country_code"]').click()
    reg_form.find_element(By.CSS_SELECTOR, 'select[name="country_code"] option[value="US"]').click()
    reg_form.find_element(By.CSS_SELECTOR, 'select[name="zone_code"]').click()
    reg_form.find_element(By.CSS_SELECTOR, 'select[name="zone_code"] option[value="CA"]').click()
    email = random_string(5) + '@' + random_string(4) + '.com'
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(email)
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="phone"]').clear()
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="phone"]').send_keys(random_digits(10))
    password = random_string(15)
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
    reg_form.find_element(By.CSS_SELECTOR, 'input[name="confirmed_password"]').send_keys(password)
    reg_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    check_success_message('Your customer account has been created', driver)
    return email, password


def go_to_reg_user_page(driver):
    driver.find_element(By.CSS_SELECTOR,
                        'form[name="login_form"] a[href="http://localhost/litecart/en/create_account"]').click()
    registration_h1 = driver.find_element(By.CSS_SELECTOR, "h1").get_attribute("textContent")
    assert registration_h1 == "Create Account"


def log_in(driver, email, password):
    login_form = driver.find_element(By.CSS_SELECTOR, '#box-account-login')
    login_form.find_element(By.CSS_SELECTOR, 'input[name="email"]').clear()
    login_form.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(email)
    login_form.find_element(By.CSS_SELECTOR, 'input[name="password"]').clear()
    login_form.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
    login_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    check_success_message('You are now logged in', driver)


def log_out(driver):
    driver.find_element(By.XPATH, '//a[contains(., "Logout")]').click()
    check_success_message('You are now logged out', driver)


def check_success_message(expected_message, driver):
    actual_message = driver.find_element(By.CSS_SELECTOR, 'div.alert.alert-success').get_attribute("textContent")
    assert expected_message in actual_message


def random_string(length):
    s = string.ascii_lowercase + string.digits
    return ''.join(random.sample(s,length))


def random_digits(length):
    d = string.digits
    return ''.join(random.sample(d,length))
