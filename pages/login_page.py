"""Login demo on the practice-site home page."""
import re

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email")
        self.password = page.locator("#password")
        self.login_button = page.locator("form button[type='submit']", has_text="Login")
        self.success_message = page.locator("#success-msg")

    def open(self):
        self.page.goto("/")
        expect(self.email).to_be_visible()

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.login_button.click()

    def expect_logged_in(self):
        expect(self.page).to_have_url(re.compile(r"logged=true"))
        expect(self.success_message).to_be_visible()
        expect(self.success_message).not_to_have_text("")

    def expect_invalid_login_error(self, message: str):
        expect(self.page.get_by_text(message)).to_be_visible()
        expect(self.success_message).to_have_count(0)
        expect(self.page).not_to_have_url(re.compile(r"logged=true"))

    def logout(self):
        (
            self.page.locator("a, button")
            .filter(has_text=re.compile(r"^\s*log ?out\s*$", re.I))
            .filter(visible=True)
            .first.click()
        )

    def expect_logged_out(self):
        expect(self.page).not_to_have_url(re.compile(r"logged=true"))
        expect(self.login_button).to_be_visible()
        expect(self.success_message).to_have_count(0)
