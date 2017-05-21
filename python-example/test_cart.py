import pytest
from app.application import Application


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.quit)
    return fixture


def test_cart(app):
    app.main_page.open()
    app.product_page.open()
    total_products_count = 3
    i = 0
    while i < total_products_count:
        app.product_page.add_product_to_cart(i)
        i += 1
    app.cart.open()
    i = 0
    while i < total_products_count:
        app.cart.remove_product_from_cart(i, total_products_count)
        i += 1


