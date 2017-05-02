import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import regex # pip install regex


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_tittle_collor_and_font(driver):
    driver.get("http://localhost/litecart/")
    driver.find_element(By.XPATH, "//a[contains(., 'Campaign Products')]").click()
    tested_item_main_page = driver.find_element(By.CSS_SELECTOR, '#campaign-products .col-xs-halfs.col-sm-thirds.col-md-fourths.col-lg-fifths:first-child')

    # On the main page.
    item_name_on_the_main_page = tested_item_main_page.find_element(By.CSS_SELECTOR, '.info .name').text

    regular_price_on_the_main_page = tested_item_main_page.find_element(By.CSS_SELECTOR, '.regular-price')
    regular_price_text_on_the_main_page = regular_price_on_the_main_page.text

    regular_price_color_on_the_main_page = regular_price_on_the_main_page.value_of_css_property('color')
    regular_price_R_color_on_the_main_page = regex.search('(?<=\()\d+', regular_price_color_on_the_main_page).group()
    regular_price_G_color_on_the_main_page = regex.search('\(\d+\,\s\K\d+', regular_price_color_on_the_main_page).group()
    regular_price_B_color_on_the_main_page = regex.search('\(\d+\,\s\d+\,\s\K\d+', regular_price_color_on_the_main_page).group()
    assert regular_price_R_color_on_the_main_page == regular_price_G_color_on_the_main_page == regular_price_B_color_on_the_main_page  # Color is gray

    regular_price_decoration_on_the_main_page = regex.search('(blink|line-through|overline|underline|none|inherit)',
                                                             regular_price_on_the_main_page.value_of_css_property('text-decoration')).group()
    assert regular_price_decoration_on_the_main_page == 'line-through'  # text-decoration:line-through

    regular_price_size_on_the_main_page = regular_price_on_the_main_page.value_of_css_property('font-size')

    campaign_price_on_the_main_page = tested_item_main_page.find_element(By.CSS_SELECTOR, '.campaign-price')
    campaign_price_text_on_the_main_page = campaign_price_on_the_main_page.text

    campaign_price_color_on_the_main_page = campaign_price_on_the_main_page.value_of_css_property('color')
    campaign_price_G_color_on_the_main_page = regex.search('\(\d+\,\s\K\d+', campaign_price_color_on_the_main_page).group()
    campaign_price_B_color_on_the_main_page = regex.search('\(\d+\,\s\d+\,\s\K\d+', campaign_price_color_on_the_main_page).group()
    assert int(campaign_price_G_color_on_the_main_page) == int(campaign_price_B_color_on_the_main_page) == 0   # Color is red

    campaign_price_decoration_on_the_main_page = campaign_price_on_the_main_page.value_of_css_property('font-weight')
    try:
        assert campaign_price_decoration_on_the_main_page == 'bold'  # font-weight:bold . Chrome
    except AssertionError:
        try:
            assert campaign_price_decoration_on_the_main_page == '700'  # font-weight:700 . FF
        except AssertionError:
            assert False


    campaign_price_size_on_the_main_page = campaign_price_on_the_main_page.value_of_css_property('font-size')

    assert regular_price_size_on_the_main_page < campaign_price_size_on_the_main_page # The font size of the campaign price is larger than the regular price

    # On the item's page
    tested_item_main_page.click()
    item_name_on_the_item_page = driver.find_element(By.CSS_SELECTOR, 'h1').text
    assert item_name_on_the_main_page == item_name_on_the_item_page  # The same item name on the main and on the item pages

    regular_price_on_the_item_page = driver.find_element(By.CSS_SELECTOR, '.regular-price')
    assert regular_price_text_on_the_main_page == regular_price_on_the_item_page.text  # The same regular item's price on the main and on the item pages

    regular_price_color_on_the_item_page = regular_price_on_the_item_page.value_of_css_property('color')
    regular_price_R_color_on_the_item_page = regex.search('(?<=\()\d+', regular_price_color_on_the_item_page).group()
    regular_price_G_color_on_the_item_page = regex.search('\(\d+\,\s\K\d+', regular_price_color_on_the_item_page).group()
    regular_price_B_color_on_the_item_page = regex.search('\(\d+\,\s\d+\,\s\K\d+', regular_price_color_on_the_item_page).group()
    assert regular_price_R_color_on_the_item_page == regular_price_G_color_on_the_item_page == regular_price_B_color_on_the_item_page  # Color is gray

    regular_price_decoration_on_the_item_page = regex.search('(blink|line-through|overline|underline|none|inherit)',
                                                             regular_price_on_the_item_page.value_of_css_property('text-decoration')).group()
    assert regular_price_decoration_on_the_item_page == 'line-through'  # text-decoration:line-through

    regular_price_size_on_the_item_page = regular_price_on_the_item_page.value_of_css_property('font-size')

    campaign_price_on_the_item_page = driver.find_element(By.CSS_SELECTOR, '.campaign-price')
    assert campaign_price_text_on_the_main_page == campaign_price_on_the_item_page.text  # The same campaign item's price on the main and on the item pages

    campaign_price_color_on_the_item_page = campaign_price_on_the_item_page.value_of_css_property('color')
    campaign_price_G_color_on_the_item_page = regex.search('\(\d+\,\s\K\d+', campaign_price_color_on_the_item_page).group()
    campaign_price_B_color_on_the_item_page = regex.search('\(\d+\,\s\d+\,\s\K\d+', campaign_price_color_on_the_item_page).group()
    assert int(campaign_price_G_color_on_the_item_page) == int(campaign_price_B_color_on_the_item_page) == 0   # Color is red

    campaign_price_decoration_on_the_item_page = campaign_price_on_the_item_page.value_of_css_property('font-weight')
    try:
        assert campaign_price_decoration_on_the_item_page == 'bold'  # font-weight:bold . Chrome
    except AssertionError:
        try:
            assert campaign_price_decoration_on_the_item_page == '700'  # font-weight:700 . FF
        except AssertionError:
            assert False

    campaign_price_size_on_the_item_page = campaign_price_on_the_item_page.value_of_css_property('font-size')
    assert regular_price_size_on_the_item_page < campaign_price_size_on_the_item_page # The font size of the campaign price is larger than the regular price



