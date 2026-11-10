"""Cart and product checks on the e-commerce demo."""
from behave import given, then, when
from playwright.sync_api import expect

from pages.shop_page import PRICE, ShopPage
from utils.base_test import BaseTest


def _shop():
    return ShopPage(BaseTest.get_page())


@given("User is logged in to the e-commerce site")
def step_shop_login(context):
    _shop().login()


@given("The cart is empty")
def step_empty_cart(context):
    _shop().empty_cart()


@when("User adds {count:d} products to cart")
def step_add_products(context, count):
    for _ in range(count):
        _shop().add_one()


@when("User removes product from cart")
def step_remove_product(context):
    _shop().remove_one()


@then("{count:d} products should be in the cart")
def step_cart_count(context, count):
    expect(_shop().remove_buttons).to_have_count(count)


@then("The cart should still hold {count:d} products after reloading the shop")
def step_cart_after_reload(context, count):
    shop = _shop()
    shop.reload()
    expect(shop.remove_buttons).to_have_count(count)


@when("User opens the details of the first product")
def step_open_details(context):
    _shop().open_first_product_details()


@then("The product details page should show its name and price")
def step_details_name_price(context):
    page = BaseTest.get_page()
    expect(page.get_by_text(PRICE).first).to_be_visible()
    expect(page.get_by_text("Sample").first).to_be_visible()


@then('Every product card should show a name, a price and an "{button_text}" button')
def step_every_card(context, button_text):
    shop = _shop()
    products = shop.distinct_products()
    assert products > 0, "no products on the page"
    expect(shop.add_buttons).to_have_count(products)
    for text in shop.card_texts():
        assert PRICE.search(text), f"no price on card: {text!r}"
        assert "Name" in text, f"no product name on card: {text!r}"
        assert button_text.lower() in text.lower(), f"no {button_text!r} button on card: {text!r}"
