"""
Internationalization (i18n) backend for the caveman AstrBot plugin.

This module provides a lightweight translation layer inspired by the
livingmemory plugin pattern.  It implements a two-level lookup:

1. Fallback layer: ``core/i18n/en-US.json`` (English, hard-coded base).
2. Active layer:  ``.astrbot-plugin/i18n/<lang>.json`` (user-facing override).

At runtime the plugin calls ``init(language)`` once (usually inside
``CavemanPlugin.__init__``) and then uses ``t(key, **kwargs)`` anywhere a
user-facing string is emitted.  Missing keys gracefully degrade to the
fallback locale so the bot never crashes because of a missing translation.

Usage example::

    from core.i18n_backend import init, t
    init("ru-RU")
    print(t("messages.mode_on", level="FULL"))
    # → "🪨 Caveman режим FULL ВКЛЮЧЁН"
"""

import json
from pathlib import Path

# Directory that holds user-provided locale files (shipped with the plugin).
_locale_dir: Path = Path(__file__).resolve().parent.parent / ".astrbot-plugin" / "i18n"

# Directory that holds the built-in fallback locale (en-US).
_fallback_locale_dir: Path = Path(__file__).resolve().parent / "i18n"

# In-memory storage for the loaded translations.
_fallback: dict = {}       # zh-CN — always loaded, guarantees baseline strings.
_translations: dict = {}   # Active locale override (e.g. en-US, ru-RU).


def init(language: str = "en-US") -> None:
    """
    Load translation files into memory.

    The function is idempotent — calling it multiple times simply reloads
    the dictionaries, which is useful when the bot language setting changes
    at runtime.

    :param language: Target locale code, e.g. ``"en-US"``, ``"zh-CN"``,
        ``"ru-RU"``.  The corresponding file must exist under
        ``.astrbot-plugin/i18n/<language>.json``.  If it does not, only the
        fallback English strings will be available.
    """
    global _fallback, _translations

    # ------------------------------------------------------------------
    # 1. Load the fallback (English base).
    #    We try the built-in ``core/i18n/en-US.json`` first, and fall back
    #    to ``.astrbot-plugin/i18n/en-US.json`` if the former is absent.
    # ------------------------------------------------------------------
    fb_path: Path = _fallback_locale_dir / "en-US.json"
    for p in (fb_path, _locale_dir / "en-US.json"):
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                _fallback = json.load(f)
            break

    # ------------------------------------------------------------------
    # 2. Load the requested locale override.
    #    Search order:
    #      1. core/i18n/<language>.json              (built-in, full translations)
    #      2. .astrbot-plugin/i18n/<language>.json   (user overrides, WebUI-only)
    #
    #    NOTE: .astrbot-plugin/i18n/ files follow AstrBot's WebUI overlay
    #    convention (only "metadata" + "config" sections).  The backend
    #    needs full translations ("help" + "messages") which live in
    #    core/i18n/.  Therefore we check core/i18n/ FIRST.
    #
    #    If neither exists the caller still has the en-US fallback above.
    # ------------------------------------------------------------------
    _translations = {}
    target_paths = (
        _fallback_locale_dir / f"{language}.json",
        _locale_dir / f"{language}.json",
    )
    for p in target_paths:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                _translations = json.load(f)
            break


def _get(data: dict, key: str):
    """
    Retrieve a nested value from *data* using dot-notation.

    For example ``_get(d, "help.commands.on")`` is equivalent to
    ``d["help"]["commands"]["on"]`` but returns ``None`` safely when any
    intermediate key is missing.

    :param data: A nested dictionary loaded from a JSON translation file.
    :param key: Dot-separated key path, e.g. ``"messages.mode_on"``.
    :return: The stored value (usually a ``str`` or ``list``) or ``None``.
    """
    keys = key.split(".")
    for k in keys:
        if isinstance(data, dict) and k in data:
            data = data[k]
        else:
            return None
    return data


def t(key: str, **kwargs) -> str:
    """
    Translate a dot-notation key into a localized string.

    Resolution order:
        1. Active locale (set by the latest ``init()`` call).
        2. Fallback locale (zh-CN shipped with the plugin).
        3. Return the raw *key* itself so the developer sees immediately
           what string is missing.

    When *kwargs* are supplied the function attempts
    ``str.format(**kwargs)`` on the resolved template.  Format failures
    are silently ignored and the raw template is returned — this prevents
    a bot crash when a translation file is slightly out of sync with the
    code.

    :param key: Translation key, e.g. ``"messages.mode_on"``.
    :param kwargs: Named placeholders for template substitution.
    :return: Localized (and optionally formatted) string.
    """
    # Try the active locale first.
    result = _get(_translations, key)
    if result is None:
        # Fall back to the built-in Chinese strings.
        result = _get(_fallback, key)
    if result is None:
        # Last resort: return the key so the user sees the identifier.
        return key

    # Apply variable substitution if the caller provided placeholders.
    if kwargs:
        try:
            result = result.format(**kwargs)
        except (KeyError, ValueError):
            # Mismatch between template variables and kwargs — safe to ignore.
            pass
    return result


def t_list(key: str) -> list:
    """
    Translate a key that maps to a list of strings.

    This helper is useful when a translation file stores an array of
    suggestions, bullet points, or command variants.  If the resolved
    value is a plain string it is wrapped into a single-element list.

    :param key: Translation key pointing to a JSON array or string.
    :return: List of localized strings (empty list if nothing is found).
    """
    result = _get(_translations, key)
    if result is None:
        result = _get(_fallback, key)
    if isinstance(result, list):
        return result
    return [result] if isinstance(result, str) else []
