"""Registration demo module (/registration)."""
import re

from playwright.sync_api import Page, expect


class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page
        self.name = page.locator("#name")
        self.country = page.locator("#country")
        self.account = page.locator("#account")
        self.email = page.locator("#email")
        self.password = page.locator("#password")
        self.confirm_password = page.locator("#confirm_password")
        self.register_button = page.locator("form button[type='submit']")

    def open(self):
        # the menu item ids are generated per page load, so the module is opened by URL
        self.page.goto("/registration")
        expect(self.name).to_be_visible()

    def fill(self, name, country, account, email, password, confirm):
        self.name.fill(name)
        self.country.select_option(country)
        self.account.select_option(account)
        self.email.fill(email)
        self.password.fill(password)
        self.confirm_password.fill(confirm)

    def submit(self):
        self.register_button.click()

    def expect_registered(self):
        expect(self.page.get_by_text(re.compile("successfully", re.I)).first).to_be_visible()

    def expect_email_rejected(self):
        """The browser blocks the submit and reports why on the field itself."""
        state = self.email.evaluate("el => ({ valid: el.validity.valid, message: el.validationMessage })")
        assert state["valid"] is False, f"e-mail field should be invalid, got {state}"
        assert "@" in state["message"], f"validation message should mention '@': {state['message']!r}"
        expect(self.page.get_by_text(re.compile("successfully", re.I))).to_have_count(0)
