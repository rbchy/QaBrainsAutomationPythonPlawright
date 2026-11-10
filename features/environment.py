"""Behave hooks: a clean browser per scenario; screenshot + page text when a scenario fails."""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from playwright.sync_api import expect  # noqa: E402

from utils.base_test import BaseTest  # noqa: E402
from utils.config_reader import ConfigReader  # noqa: E402


def before_all(context):
    os.makedirs("reports/screenshots", exist_ok=True)
    expect.set_options(timeout=ConfigReader.get_int("timeout", 15000))


def before_scenario(context, scenario):
    BaseTest.init_browser()
    context.page = BaseTest.get_page()


def after_scenario(context, scenario):
    if BaseTest.recoveries:
        print(f"⚠ {scenario.name}: site error screen recovered {len(BaseTest.recoveries)}x at {BaseTest.recoveries}")
    try:
        if scenario.status == "failed":
            page = BaseTest.get_page()
            name = re.sub(r"[^\w.-]+", "_", scenario.name)[:80]
            path = f"reports/screenshots/{name}.png"
            page.screenshot(path=path, full_page=True)
            body = page.locator("body").inner_text()[:1200]
            # printed so a CI failure can be read straight from the log
            print(f"\n---- FAILED: {scenario.name} @ {page.url}\n{body}\n---- screenshot: {path}")
    except Exception as exc:  # never hide the real failure
        print(f"Could not capture failure details: {exc}")
    finally:
        BaseTest.quit_browser()
