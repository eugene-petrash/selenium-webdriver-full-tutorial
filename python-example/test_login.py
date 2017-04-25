import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

@pytest.fixture
def driver(request):
    wd = webdriver.Firefox(capabilities={'marionette': True,
                                         'acceptSslCerts': False,
                                         'applicationCacheEnabled': False,
                                         'takesScreenshot': True,
                                         'version': '45.9.0',
                                         'raisesAccessibilityExceptions': False,
                                         'platform': 'LINUX',
                                         'platformName': 'Linux',
                                         'proxy': {},
                                         'platformVersion': '4.4.0-72-generic',
                                         'browserName': 'Firefox',
                                         'specificationLevel': '1',
                                         'XULappId': '{ec8030f7-c20a-464f-9b0e-13a3a9e97384}',
                                         'takesElementScreenshot': True,
                                         'browserVersion': '45.9.0',
                                         'device': 'desktop',
                                         'rotatable': False,
                                         'appBuildId': '20170411115307'
                                         },
                           firefox_binary=FirefoxBinary("/usr/local/bin/firefox_ESR_45/firefox"),
                           firefox_profile=FirefoxProfile(),
                           timeout=50,
                           proxy=None,
                           executable_path='geckodriver',
                           firefox_options=None, # More details here https://seleniumhq.github.io/selenium/docs/api/py/_modules/selenium/webdriver/firefox/options.html
                           log_path='geckodriver.log'
                           # More details here http://seleniumhq.github.io/selenium/docs/api/py/webdriver_firefox/selenium.webdriver.firefox.webdriver.html#module-selenium.webdriver.firefox.webdriver
                           )
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    pass
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@name='login']")))
    driver.find_element(By.XPATH, "//button[@name='login']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Statistics')]")))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//i[@class='fa fa-sign-out fa-lg']")))
    driver.find_element(By.XPATH, "//i[@class='fa fa-sign-out fa-lg']").click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@name='login']")))
