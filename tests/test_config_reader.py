"""Unit tests for the framework helpers (no browser, no network)."""
import re

import pytest

from pages.shop_page import PRICE
from utils.config_reader import ConfigReader


@pytest.fixture(autouse=True)
def fresh_config(monkeypatch):
    for var in ("BASE_URL", "BROWSER", "HEADLESS"):
        monkeypatch.delenv(var, raising=False)
    ConfigReader.reset()
    yield
    ConfigReader.reset()


def test_reads_properties_file():
    assert ConfigReader.get("url") == "https://practice.qabrains.com/"
    assert ConfigReader.get("valid_email") == "qa_testers@qabrains.com"
    assert ConfigReader.get_int("timeout") == 15000


def test_headless_defaults_to_false_locally():
    assert ConfigReader.get_bool("headless") is False


@pytest.mark.parametrize("value, expected", [("true", True), ("TRUE", True), ("1", True), ("false", False), ("no", False)])
def test_env_overrides_headless(monkeypatch, value, expected):
    monkeypatch.setenv("HEADLESS", value)
    assert ConfigReader.get_bool("headless") is expected


def test_env_overrides_browser_and_url(monkeypatch):
    monkeypatch.setenv("BROWSER", "firefox")
    monkeypatch.setenv("BASE_URL", "http://localhost:8080/")
    assert ConfigReader.get("browser") == "firefox"
    assert ConfigReader.get("url") == "http://localhost:8080/"


def test_blank_env_var_does_not_override(monkeypatch):
    monkeypatch.setenv("BROWSER", "   ")
    assert ConfigReader.get("browser") == "chromium"


def test_missing_key_and_bad_int_use_defaults():
    assert ConfigReader.get("no_such_key", "fallback") == "fallback"
    assert ConfigReader.get_int("valid_email", 7) == 7


@pytest.mark.parametrize("text, ok", [("Price $29.99", True), ("$1200.00", True), ("$29.9", False), ("29.99", False)])
def test_price_pattern(text, ok):
    assert bool(PRICE.search(text)) is ok


def test_every_scenario_is_tagged():
    """behave runs everything, but each scenario should still belong to @smoke or @regression."""
    import pathlib
    untagged = []
    for feature in pathlib.Path("features").glob("*.feature"):
        lines = feature.read_text().splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("Scenario"):
                tags = " ".join(l for l in lines[max(0, i - 2):i] if l.strip().startswith("@"))
                if not re.search(r"@(smoke|regression)\b", tags):
                    untagged.append(f"{feature.name}: {line.strip()}")
    assert untagged == []
