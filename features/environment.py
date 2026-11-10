"""Behave hooks: a clean browser per scenario; screenshot + page text when a scenario fails."""
import functools
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


# Set by after_scenario: did the attempt that just finished meet the site's own
# "caught by error boundary" screen?
_SITE_ERROR = {"last": False}
RETRIED = []


def _run_with_site_error_retry(original_run, *args, **kwargs):
    """Re-run a failed scenario ONCE, and only when the failure came with the
    practice site's React error screen. Ordinary assertion failures are never retried."""
    failed = original_run(*args, **kwargs)
    if failed and _SITE_ERROR["last"]:
        print("↻ RETRY: the attempt met the site's error screen, running the scenario once more")
        failed = original_run(*args, **kwargs)
        RETRIED.append(("passed" if not failed else "failed"))
    return failed


def before_feature(context, feature):
    for scenario in feature.walk_scenarios():
        scenario.run = functools.partial(_run_with_site_error_retry, scenario.run)


def after_all(context):
    if RETRIED:
        print(f"↻ site-error retries: {len(RETRIED)} ({RETRIED.count('passed')} passed on retry)")


def before_scenario(context, scenario):
    BaseTest.init_browser()
    context.page = BaseTest.get_page()


def after_scenario(context, scenario):
    if BaseTest.recoveries:
        print(f"⚠ {scenario.name}: site error screen recovered {len(BaseTest.recoveries)}x at {BaseTest.recoveries}")
    _SITE_ERROR["last"] = False
    try:
        if scenario.status == "failed":
            page = BaseTest.get_page()
            _SITE_ERROR["last"] = bool(BaseTest.recoveries) or page.get_by_text("caught by error boundary").is_visible()
    except Exception:
        pass
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
