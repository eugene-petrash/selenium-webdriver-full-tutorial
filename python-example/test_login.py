import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome(desired_capabilities={'chromeOptions': {'args': ['--start-fullscreen'],  # More here http://peter.sh/experiments/chromium-command-line-switches/
                                                                  'binary': '/usr/bin/google-chrome'},
                                                'databaseEnabled': False,
                                                'platform': 'Linux',
                                                'networkConnectionEnabled': False,
                                                'takesScreenshot': True,
                                                'javascriptEnabled': True,
                                                'browserName': 'chrome',
                                                'hasTouchScreen': False,
                                                'takesHeapSnapshot': True,
                                                'pageLoadStrategy': 'normal',
                                                'webStorageEnabled': True,
                                                'applicationCacheEnabled': False,
                                                'rotatable': False,
                                                'chrome': {'userDataDir': '/tmp/.org.chromium.Chromium.ayvBAD',
                                                           'chromedriverVersion': '2.29.461571 (8a88bbe0775e2a23afda0ceaf2ef7ee74e822cc5)'},
                                                'handlesAlerts': True,
                                                'mobileEmulationEnabled': False,
                                                'locationContextEnabled': True,
                                                'acceptSslCerts': True,
                                                'version': '57.0.2987.133',
                                                'browserConnectionEnabled': False,
                                                'unexpectedAlertBehaviour': 'ignore', # ignore/accept/dismiss
                                                'cssSelectorsEnabled': True,
                                                'nativeEvents': True
                                                })
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
