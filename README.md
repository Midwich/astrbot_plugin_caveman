<p align="center">
  <a href="README_zh.md">中文</a> | <a href="README.md">English</a> | <a href="README_ru.md">Русский</a>
</p>

# 🪨 astrbot_plugin_caveman — LLM Output Compression Plugin

**Version**: v0.0.1 | **Author**: Midwich | **License**: MIT

> *why use many token when few token do trick*

An [AstrBot](https://github.com/AstrBotDevs/AstrBot) plugin that makes your AI assistant respond with extreme brevity — cutting **~65% of output tokens** while keeping full technical accuracy.

Adapted from [**JuliusBrussee/caveman**](https://github.com/JuliusBrussee/caveman) (v1.8.1), the viral Claude Code skill ecosystem.

---

## Features

- **Four compression levels**: lite → full → ultra → wenyan (classical Chinese)
- **Session-level state**: each chat session remembers its own caveman mode
- **i18n support**: user-facing text auto-adapts to AstrBot's `bot_language`
- **Zero dependencies**: pure AstrBot API, no extra packages
- **Safe injection**: duplicate-prompt guard via `[CAVEMAN_MODE_ACTIVE]` marker

---

## Quick Start

### Installation

1. Clone into AstrBot's plugin folder:

```bash
cd /path/to/astrbot/data/plugins
git clone https://github.com/Midwich/astrbot_plugin_caveman.git
```

2. Restart AstrBot or reload plugins via the WebUI.

### Requirements

- AstrBot ≥ 3.0 (uses `filter.on_llm_request` hook)

### Configuration

No manual configuration required. The plugin reads `bot_language` from AstrBot settings automatically.

Supported languages:

| Language | File | Status |
|----------|------|--------|
| **English** | `.astrbot-plugin/i18n/en-US.json` | ✅ Full |
| **Русский** | `.astrbot-plugin/i18n/ru-RU.json` | ✅ Full |
| **中文** | `.astrbot-plugin/i18n/zh-CN.json` | ✅ Full (fallback) |

---

## Commands

| Command | Description |
|---------|-------------|
| `/caveman` or `/caveman help` | Show help |
| `/caveman on` or `/caveman full` | Enable **full** mode (default) |
| `/caveman lite` | Enable **lite** — professional, no fluff |
| `/caveman ultra` | Enable **ultra** — telegraphic, max compression |
| `/caveman wenyan` | Enable **文言文** — classical Chinese terseness |
| `/caveman wenyan-lite` | Enable **wenyan-lite** |
| `/caveman wenyan-ultra` | Enable **wenyan-ultra** |
| `/caveman off` | Disable caveman, normal mode |
| `/caveman status` | Show current mode |

### Examples

```
You: /caveman full
Bot: 🪨 Caveman FULL mode ON.

You: How do I fix React re-render?
Bot: New object ref each render. useMemo wrap. Done.
```

---

## Modes

| Mode | Style | Token reduction |
|------|-------|-----------------|
| **lite** | Professional, drop filler | ~30% |
| **full** | Default caveman. Fragments, no articles | ~65% |
| **ultra** | Telegraphic, abbreviate everything | ~75% |
| **wenyan** | Classical Chinese terseness | varies |

---

## Internationalization

The plugin follows AstrBot's `bot_language` setting automatically.

All user-facing strings (help, status, errors) are localized via `.astrbot-plugin/i18n/*.json`. LLM compression prompts remain in English for maximum model compatibility.

To add a new language, create a new JSON file in `.astrbot-plugin/i18n/` (e.g. `ja-JP.json`) and reload the plugin. Missing keys fall back to Chinese (`zh-CN`).

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## License & Attribution

This project is a derivative work based on [**caveman**](https://github.com/JuliusBrussee/caveman)
by [Julius Brussee](https://github.com/JuliusBrussee), which is licensed under the
[MIT License](https://github.com/JuliusBrussee/caveman/blob/main/LICENSE).

The original caveman is a Claude Code skill ecosystem for LLM output compression.
This repository is an **unofficial, independent port** to the AstrBot platform and is
**not affiliated with or endorsed by the original author**.

Both the original work and this port are released under the MIT License.
See the [LICENSE](./LICENSE) file for the full legal text.

Ported by **Midwich**.
