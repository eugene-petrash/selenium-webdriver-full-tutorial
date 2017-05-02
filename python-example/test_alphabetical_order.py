import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import icu # pip install PyICU


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_check_countries_order(driver):
    admin_login(driver)
    driver.find_element(By.CSS_SELECTOR, "a[href='http://localhost/litecart/admin/?app=countries&doc=countries']").click()
    # a)
    countries_elements_list = driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table td a:not([title=Edit])')
    actual_countries_list = []
    for country_element in countries_elements_list:
        country = country_element.get_attribute("textContent")
        actual_countries_list.append(country)
    collator = icu.Collator.createInstance(icu.Locale('de_DE.UTF-8'))
    expected_countries_list = sorted(actual_countries_list, key=collator.getSortKey)
    assert actual_countries_list == expected_countries_list
    # b)
    countries_table_rows_len = len(driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table tbody tr'))
    i = 0
    while i < countries_table_rows_len:
        countries_table_rows = driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table tbody tr')
        zone_count = int(countries_table_rows[i].find_element(By.CSS_SELECTOR, '.text-center').text)
        if zone_count != 0:
            countries_table_rows[i].find_element(By.CSS_SELECTOR, 'a[title=Edit]').click()
            countries_zone_table_rows = driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table tbody tr')
            countries_zone_list = []
            for zone in countries_zone_table_rows:
                countries_zone_number_element = zone.find_element(By.CSS_SELECTOR, 'td:first-child')
                countries_zone_number_str = countries_zone_number_element.text
                countries_zone_name_element = zone.find_element(By.CSS_SELECTOR, "input[name='zones[" + countries_zone_number_str + "][name]']")
                countries_zone_name_str = countries_zone_name_element.get_attribute("value")
                countries_zone_list.append(countries_zone_name_str)
            assert countries_zone_list == sorted(countries_zone_list, key=collator.getSortKey)
            driver.find_element(By.CSS_SELECTOR, "a[href='http://localhost/litecart/admin/?app=countries&doc=countries']").click()
        i += 1
    admin_logout(driver)


def test_check_zones_order(driver):
    admin_login(driver)
    driver.find_element(By.CSS_SELECTOR, "a[href='http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones']").click()
    zones_table_rows_count = len(driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table tbody tr'))
    i = 0
    while i < zones_table_rows_count:
        zones_table_rows = driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table tbody tr')
        zones_table_rows[i].find_element(By.CSS_SELECTOR, 'a[title="Edit"]').click()
        zones_countries_zones_list_rows = driver.find_elements(By.CSS_SELECTOR, '.table.table-striped.data-table tbody tr')
        zones_countries_zone_list = []
        for zone in zones_countries_zones_list_rows:
            zones_countries_zone_number_element = zone.find_element(By.CSS_SELECTOR, 'td:first-child')
            zones_countries_zone_number_str = zones_countries_zone_number_element.text
            zones_countries_zone_name_element = zone.find_element(By.XPATH, "//input[@name='zones[" + zones_countries_zone_number_str + "][zone_code]']/..")
            zones_countries_zone_name_str = zones_countries_zone_name_element.text
            zones_countries_zone_list.append(zones_countries_zone_name_str)
        collator = icu.Collator.createInstance(icu.Locale('de_DE.UTF-8'))
        assert zones_countries_zone_list == sorted(zones_countries_zone_list, key=collator.getSortKey)
        driver.find_element(By.CSS_SELECTOR, "a[href='http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones']").click()
        i += 1
    admin_logout(driver)


def admin_login(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button[@name='login']").click()


def admin_logout(driver):
    driver.find_element(By.CSS_SELECTOR, '.fa.fa-sign-out.fa-lg').click()