"""A fresh browser, context and page for every scenario (started / closed in environment.py)."""
from playwright.sync_api import sync_playwright, Page

from utils.config_reader import ConfigReader


class BaseTest:
    _playwright = None
    _browser = None
    _context = None
    _page: Page = None

    @classmethod
    def init_browser(cls):
        cls._playwright = sync_playwright().start()
        name = ConfigReader.get("browser", "chromium").lower()
        name = {"chrome": "chromium", "edge": "chromium"}.get(name, name)
        launcher = getattr(cls._playwright, name)  # chromium | firefox | webkit
        cls._browser = launcher.launch(headless=ConfigReader.get_bool("headless"))
        cls._context = cls._browser.new_context(
            base_url=ConfigReader.get("url"),
            viewport={
                "width": ConfigReader.get_int("viewport_width", 1440),
                "height": ConfigReader.get_int("viewport_height", 900),
            },
        )
        cls._page = cls._context.new_page()
        cls._page.set_default_timeout(ConfigReader.get_int("timeout", 15000))
        cls._install_error_boundary_recovery(cls._page)
        cls._page.goto(ConfigReader.get("url"))

    # The live practice site sometimes renders its React error screen
    # ("Oops! Something went wrong! caught by error boundary") instead of the page.
    # Playwright runs this handler before any action / expect() that meets the screen:
    # it re-opens the same URL with a growing pause (up to 4 tries) and logs each
    # recovery, so the site's instability stays visible in the CI log.
    recoveries = []

    @classmethod
    def _install_error_boundary_recovery(cls, page: Page):
        cls.recoveries = []
        crash = page.get_by_text("caught by error boundary")

        def reopen(_locator=None):
            url = page.url
            for attempt in range(1, 5):
                cls.recoveries.append(url)
                print(f"⚠ site error boundary at {url}: re-opening (try {attempt}/4)")
                page.wait_for_timeout(1500 * attempt)
                page.goto(url, wait_until="load")
                page.wait_for_timeout(1000)
                if not crash.is_visible():
                    return

        page.add_locator_handler(crash, reopen, times=3)

    @classmethod
    def get_page(cls) -> Page:
        if cls._page is None:
            raise RuntimeError("Page is not ready: init_browser() runs in before_scenario")
        return cls._page

    @classmethod
    def quit_browser(cls):
        for closer in (cls._context, cls._browser):
            try:
                if closer:
                    closer.close()
            except Exception:
                pass
        if cls._playwright:
            cls._playwright.stop()
        cls._playwright = cls._browser = cls._context = cls._page = None
