import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_new_window(driver):
    wait = WebDriverWait(driver, 10)
    admin_login(driver)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element(By.XPATH, '//a[contains(., " Add New Country")]').click()
    extra_links_list = driver.find_elements(By.CSS_SELECTOR, '.fa.fa-external-link')
    i = 0
    while i < len(extra_links_list):
        old_windows_list = driver.window_handles
        main_window = driver.current_window_handle
        extra_links_list[i].click()
        wait.until(EC.new_window_is_opened(old_windows_list))
        assert wait.until(EC.number_of_windows_to_be(2))
        test_windows_list = driver.window_handles
        for window in test_windows_list:
            if window not in old_windows_list:
                new_window = window
        driver.switch_to_window(new_window)
        print(driver.title)
        driver.close()
        driver.switch_to_window(main_window)
        assert wait.until(EC.number_of_windows_to_be(1))
        i += 1


def admin_login(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[@name='login']").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(.,'Statistics')]")))
    assert len(driver.find_elements(By.XPATH, "//h3[contains(.,'Statistics')]")) == 1