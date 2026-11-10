"""Reads config/config.properties. Environment variables override a key:
BASE_URL -> url, BROWSER -> browser, HEADLESS -> headless (e.g. HEADLESS=true in CI)."""
import configparser
import os

_ENV_OVERRIDES = {"url": "BASE_URL", "browser": "BROWSER", "headless": "HEADLESS"}


class ConfigReader:
    _config = None
    path = os.path.join(os.path.dirname(__file__), "..", "config", "config.properties")

    @classmethod
    def _load(cls):
        if cls._config is None:
            cls._config = configparser.RawConfigParser()
            with open(os.path.abspath(cls.path), "r", encoding="utf-8") as f:
                # configparser needs a section header; the file is a plain .properties file
                cls._config.read_string("[DEFAULT]\n" + f.read())

    @classmethod
    def reset(cls):
        cls._config = None

    @classmethod
    def get(cls, key: str, default: str = "") -> str:
        env = _ENV_OVERRIDES.get(key)
        if env and os.environ.get(env, "").strip():
            return os.environ[env].strip()
        cls._load()
        return cls._config["DEFAULT"].get(key, default).strip()

    @classmethod
    def get_bool(cls, key: str) -> bool:
        return cls.get(key).lower() in ("true", "1", "yes", "on")

    @classmethod
    def get_int(cls, key: str, default: int = 0) -> int:
        value = cls.get(key)
        return int(value) if value.isdigit() else default
