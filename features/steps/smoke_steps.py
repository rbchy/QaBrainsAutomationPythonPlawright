"""Home page and sidebar demo modules."""
import re

from behave import given, then, when
from playwright.sync_api import expect

from utils.base_test import BaseTest
from utils.config_reader import ConfigReader


@given("User launches the application")
def step_launch(context):
    BaseTest.get_page().goto("/")


@then("Home page should load successfully")
def step_home_loaded(context):
    page = BaseTest.get_page()
    expect(page).to_have_url(ConfigReader.get("url"))
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("form button[type='submit']", has_text="Login")).to_be_visible()


@when("User opens each demo module from the menu")
def step_open_modules(context):
    page = BaseTest.get_page()
    context.opened_modules = []
    # behave treats the first table row as the heading, so include it
    rows = [context.table.headings] + [r.cells for r in context.table.rows]
    context.expected_modules = [label for label, _ in rows]
    for label, expected_in_url in rows:
        page.goto("/")
        # menu items are rendered client-side; the locator waits for them
        item = (
            page.locator("[role='menuitem'], a")
            .filter(has_text=re.compile(rf"^\s*{re.escape(label)}\s*$"))
            .first
        )
        expect(item).to_be_visible()
        # keep the demo in this tab
        item.evaluate("el => { const a = el.tagName === 'A' ? el : el.querySelector('a'); if (a) a.removeAttribute('target'); }")
        item.click()
        expect(page).to_have_url(re.compile(re.escape(expected_in_url)))
        context.opened_modules.append(label)


@then("Each module page should open")
def step_modules_opened(context):
    expected = context.expected_modules
    assert context.opened_modules == expected, f"opened {context.opened_modules}, expected {expected}"
    expect(BaseTest.get_page().locator("body")).to_be_visible()
