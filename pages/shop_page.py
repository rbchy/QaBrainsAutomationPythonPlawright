"""E-Commerce demo (/ecommerce). Each product card has one button that toggles
"Add to cart" / "Remove from cart", so the number of "Remove" buttons is the cart size."""
import re

from playwright.sync_api import Page, expect

from utils.config_reader import ConfigReader

PRICE = re.compile(r"\$\d+\.\d{2}")


class ShopPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_buttons = page.get_by_role("button", name=re.compile(r"^add to cart$", re.I))
        self.remove_buttons = page.get_by_role("button", name=re.compile(r"^remove from cart$", re.I))
        self.product_links = page.locator("a[href*='/ecommerce/product-details']")

    def login(self):
        self.page.goto("/ecommerce/login")
        self.page.locator("#email").fill(ConfigReader.get("shop_email"))
        self.page.locator("#password").fill(ConfigReader.get("shop_password"))
        self.page.locator("form button[type='submit']").first.click()
        expect(self.add_buttons.first).to_be_visible(timeout=20_000)

    def add_one(self):
        before = self.remove_buttons.count()
        self.add_buttons.first.click()
        expect(self.remove_buttons).to_have_count(before + 1)

    def remove_one(self):
        before = self.remove_buttons.count()
        self.remove_buttons.first.click()
        expect(self.remove_buttons).to_have_count(before - 1)

    def empty_cart(self):
        """Start from an empty cart, whatever an earlier run left behind."""
        while self.remove_buttons.count() > 0:
            self.remove_one()

    def reload(self):
        self.page.goto("/ecommerce")
        expect(self.add_buttons.or_(self.remove_buttons).first).to_be_visible(timeout=20_000)

    def open_first_product_details(self):
        href = self.product_links.first.get_attribute("href")
        assert href, "first product has no details link"
        self.page.goto(href)
        expect(self.page).to_have_url(re.compile(r"product-details\?id=\d+"))

    def card_texts(self):
        """Text of every product card: the closest ancestor of a cart button that also holds a product link."""
        return self.add_buttons.evaluate_all(
            """buttons => buttons.map(b => {
                 let el = b;
                 while (el && !el.querySelector("a[href*='product-details']")) el = el.parentElement;
                 return el ? el.innerText : "";
               })"""
        )

    def distinct_products(self) -> int:
        hrefs = self.product_links.evaluate_all("links => links.map(a => a.getAttribute('href'))")
        return len(set(hrefs))
