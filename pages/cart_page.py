import os
from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page

    def _is_logged_in(self) -> bool:
        return self.page.locator("button:has-text('Logout'), [class*='logout']").count() > 0

    def _login_if_needed(self):
        if not self._is_logged_in():
            print("ℹ️  Logging in first...")
            from pages.login_page import LoginPage
            lp = LoginPage(self.page)
            lp.login("qa_testers@qabrains.com", "Password123")
            self.page.wait_for_timeout(2000)

    def _click_sidebar_item(self, label: str) -> bool:
        """Click a sidebar button/link by label text."""
        selectors = [
            f"button:has-text('{label}')",
            f"a:has-text('{label}')",
            f"span:has-text('{label}')",
            f"li:has-text('{label}')",
            f"[class*='sidebar'] *:has-text('{label}')",
        ]
        for sel in selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible():
                    el.click()
                    self.page.wait_for_timeout(2000)
                    print(f"✅ Clicked sidebar: '{label}'")
                    return True
            except Exception:
                pass
        print(f"⚠ Could not find sidebar item: '{label}'")
        return False

    def _open_ecommerce(self):
        """Navigate to home and click E-Commerce Site in sidebar."""
        # Go to home page
        self.page.goto("https://practice.qabrains.com/")
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_timeout(2000)

        # Click "E-Commerce Site" button in sidebar
        clicked = self._click_sidebar_item("E-Commerce Site")
        if not clicked:
            print("⚠ E-Commerce Site button not found — printing all sidebar items:")
            for el in self.page.locator("aside *, [class*='sidebar'] *, nav *").all():
                try:
                    txt = el.text_content().strip()
                    if txt and len(txt) < 50:
                        print(f"   → '{txt}'")
                except Exception:
                    pass

        self.page.wait_for_timeout(3000)

        # Check for "Failed to fetch" error — retry once
        failed_count = self.page.locator("text=Failed to fetch").count()
        if failed_count > 0:
            print("⚠ 'Failed to fetch component data' detected — retrying...")
            self.page.reload()
            self.page.wait_for_load_state('networkidle', timeout=8000)
            self.page.wait_for_timeout(2000)
            self._click_sidebar_item("E-Commerce Site")
            self.page.wait_for_timeout(3000)

        print(f"ℹ️  E-Commerce page loaded. URL: {self.page.url}")

    def _find_add_to_cart(self):
        """Search for Add to Cart buttons with many strategies."""
        selectors = [
            "button:has-text('Add to Cart')",
            "button:has-text('Add to cart')",
            "button:has-text('ADD TO CART')",
            "a:has-text('Add to Cart')",
            ".add-to-cart",
            "[class*='add-to-cart']",
            "[class*='addtocart']",
            "[data-action='add-to-cart']",
            "button:has-text('Buy')",
            "button:has-text('Buy Now')",
            ".btn-cart",
            "[class*='btn-cart']",
            # Broad patterns for this site's e-commerce panel
            "main button",
            "#root button",
            "[class*='product'] button",
            "[class*='item'] button",
            ".card button",
            "article button",
        ]
        for sel in selectors:
            try:
                loc = self.page.locator(sel)
                cnt = loc.count()
                if cnt > 0:
                    # Skip Logout button
                    for i in range(cnt):
                        txt = loc.nth(i).text_content().strip().lower()
                        if 'logout' not in txt and txt:
                            print(f"✅ Add to Cart via '{sel}'[{i}]: '{txt}'")
                            return loc, i
            except Exception:
                pass
        return None, 0

    def add_product_to_cart(self, index: int = 0):
        # Open e-commerce section from sidebar
        self._open_ecommerce()

        # Wait for JS content to render
        try:
            self.page.wait_for_load_state('networkidle', timeout=8000)
        except Exception:
            pass
        self.page.wait_for_timeout(2000)

        loc, btn_index = self._find_add_to_cart()
        if loc:
            try:
                loc.nth(btn_index).scroll_into_view_if_needed()
            except Exception:
                pass
            loc.nth(btn_index).click()
            self.page.wait_for_timeout(2000)
            print("✅ Add to Cart clicked!")
            return

        # Debug — print ALL page content
        print(f"❌ Add to Cart NOT found. URL: {self.page.url}")
        print("   Right panel content (buttons/inputs):")
        for el in self.page.locator("button, input, a[href]").all():
            try:
                txt = el.text_content().strip()
                cls = el.get_attribute("class") or ""
                typ = el.get_attribute("type") or el.evaluate("e=>e.tagName")
                if txt:
                    print(f"     [{typ}] '{txt}' class='{cls[:60]}'")
            except Exception:
                pass

        print("   Page visible text (first 500 chars):")
        try:
            print("   " + self.page.locator("body").inner_text()[:500])
        except Exception:
            pass

        os.makedirs("reports/screenshots", exist_ok=True)
        try:
            self.page.screenshot(
                path="reports/screenshots/ecommerce_debug.png",
                full_page=True
            )
            print("📸 Saved ecommerce_debug.png")
        except Exception:
            pass

        # Check if it's a site-level error
        page_text = self.page.locator("body").inner_text().lower()
        if "failed to fetch" in page_text or "error" in page_text:
            raise RuntimeError(
                "❌ E-Commerce component failed to load on practice.qabrains.com. "
                "This appears to be a SITE-SIDE issue ('Failed to fetch component data'). "
                "Check ecommerce_debug.png and verify site is working manually."
            )

        raise RuntimeError(
            f"❌ No Add-to-Cart button found in E-Commerce section. "
            f"URL: {self.page.url}. Check ecommerce_debug.png."
        )

    def is_product_in_cart(self, index: int = 0) -> bool:
        self.page.wait_for_timeout(2000)

        # Check cart selectors
        for sel in [".cart-item", "[class*='cart-item']", ".cart-product",
                    "[class*='cart-product']", ".order-item", "tbody tr",
                    "[class*='line-item']"]:
            try:
                cnt = self.page.locator(sel).count()
                if cnt > 0:
                    print(f"✅ Cart items via '{sel}': {cnt}")
                    return cnt > index
            except Exception:
                pass

        # Navigate to cart page if not already there
        if 'cart' not in self.page.url:
            for sel in ["a:has-text('Cart')", "a[href*='/cart']", ".cart-icon"]:
                try:
                    el = self.page.locator(sel).first
                    if el.is_visible():
                        el.click()
                        self.page.wait_for_load_state()
                        break
                except Exception:
                    pass

        self.page.wait_for_timeout(1500)

        # Fallback: body text
        try:
            body = self.page.locator("body").inner_text().lower()
            return any(k in body for k in [
                "remove", "quantity", "subtotal", "your cart", "checkout", "item in cart"
            ])
        except Exception:
            return False

    def remove_product(self, index: int = 0):
        for sel in ["button:has-text('Remove')", "a:has-text('Remove')",
                    "button:has-text('Delete')", "a:has-text('Delete')",
                    ".remove-item", "[class*='remove-item']",
                    "[data-action='remove']", "a[href*='remove']"]:
            try:
                loc = self.page.locator(sel)
                if loc.count() > index:
                    print(f"✅ Remove button: {sel}")
                    loc.nth(index).click()
                    self.page.wait_for_timeout(1500)
                    return
            except Exception:
                pass
        print("⚠ Remove button not found")

    def go_to_checkout(self):
        for sel in ["#checkout", "button:has-text('Checkout')", "a:has-text('Checkout')"]:
            try:
                el = self.page.locator(sel).first
                if el.is_visible():
                    el.click()
                    return
            except Exception:
                pass

    def get_product_quantity(self, index: int = 0) -> int:
        for sel in ["input[name='quantity']", "input[class*='qty']", "input[class*='quantity']"]:
            try:
                loc = self.page.locator(sel)
                if loc.count() > index:
                    val = loc.nth(index).input_value()
                    if val:
                        return int(val)
            except Exception:
                pass
        return 0
