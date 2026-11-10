"""Forgot Password demo module (/forgot-password)."""
import re

from playwright.sync_api import Page, expect


class ForgotPasswordPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email")
        self.submit_button = page.locator("form button[type='submit']").first
        self.success_message = page.locator("#success-msg")

    def open(self):
        self.page.goto("/forgot-password")
        expect(self.email).to_be_visible()

    def request_reset(self, email: str):
        self.email.fill(email)
        self.submit_button.click()

    def expect_success(self, expected: str):
        """A valid e-mail adds ?forgot=true and shows the success banner."""
        expect(self.page).to_have_url(re.compile(r"forgot=true"))
        expect(self.success_message).to_be_visible()
        expect(self.success_message).to_contain_text(expected)

    def expect_validation_error(self, expected: str):
        """A malformed e-mail is stopped by the browser before it is sent."""
        message = self.email.evaluate("el => el.validationMessage")
        assert expected in message, f"expected {expected!r} in the browser message {message!r}"
        expect(self.page).not_to_have_url(re.compile(r"forgot=true"))
