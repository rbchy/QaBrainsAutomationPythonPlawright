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
        """A malformed e-mail is stopped by the browser before it is sent.
        The state (typeMismatch) is the same in every browser; the wording is
        Chromium's ("...is missing an '@'"), Firefox says "Please enter an email address."."""
        state = self.email.evaluate(
            "el => ({ typeMismatch: el.validity.typeMismatch, message: el.validationMessage })"
        )
        assert state["typeMismatch"] is True, f"browser should flag a type mismatch: {state}"
        if self.page.context.browser.browser_type.name == "chromium":
            assert expected in state["message"], f"expected {expected!r} in {state['message']!r}"
        else:
            assert state["message"], "browser gave no validation message"
        expect(self.page).not_to_have_url(re.compile(r"forgot=true"))
        expect(self.success_message).to_have_count(0)
