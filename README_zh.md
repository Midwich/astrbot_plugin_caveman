<p align="center">
  <a href="README_zh.md">中文</a> | <a href="README.md">English</a> | <a href="README_ru.md">Русский</a>
</p>

# 🪨 astrbot_plugin_caveman — LLM 输出压缩插件

**版本**: v0.0.1 | **作者**: Midwich | **许可证**: MIT

> *why use many token when few token do trick（为什么要用很多 token，少量 token 就能搞定）*

适用于 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的插件，让你的 AI 助手以极致简洁的方式回答 —— 节省 **~65% 的输出 token**，同时保持完整的技术准确性。

改编自 [**JuliusBrussee/caveman**](https://github.com/JuliusBrussee/caveman)（v1.8.1），这是流行起来的 Claude Code 技能生态系统。

---

## 功能特性

- **四级压缩强度**：lite → full → ultra → wenyan（文言文）
- **会话级状态**：每个聊天会话独立记忆自己的 caveman 模式
- **国际化支持**：用户界面文字自动适配 AstrBot 的 `bot_language` 设置
- **零依赖**：纯 AstrBot API，无需额外包
- **安全注入**：通过 `[CAVEMAN_MODE_ACTIVE]` 标记防止重复注入

---

## 快速开始

### 安装

1. 克隆到 AstrBot 插件目录：

```bash
cd /path/to/astrbot/data/plugins
git clone https://github.com/Midwich/astrbot_plugin_caveman.git
```

2. 重启 AstrBot 或通过 WebUI 重新加载插件。

### 环境要求

- AstrBot ≥ 3.0（使用 `filter.on_llm_request` 钩子）

### 配置

无需手动配置。插件自动读取 AstrBot 设置中的 `bot_language`。

支持语言：

| 语言 | 文件 | 状态 |
|------|------|------|
| **English** | `.astrbot-plugin/i18n/en-US.json` | ✅ 完整 |
| **Русский** | `.astrbot-plugin/i18n/ru-RU.json` | ✅ 完整 |
| **中文** | `.astrbot-plugin/i18n/zh-CN.json` | ✅ 完整（默认回退） |

---

## 命令

| 命令 | 操作 |
|------|------|
| `/caveman` 或 `/caveman help` | 显示帮助 |
| `/caveman on` 或 `/caveman full` | 启用 **完整** 模式（默认） |
| `/caveman lite` | 启用 **lite** —— 专业风格，去除废话 |
| `/caveman ultra` | 启用 **ultra** —— 电报风格，极限压缩 |
| `/caveman wenyan` | 启用 **文言文** —— 古典中文简洁风格 |
| `/caveman wenyan-lite` | 启用 **wenyan-lite** |
| `/caveman wenyan-ultra` | 启用 **wenyan-ultra** |
| `/caveman off` | 关闭 caveman，恢复正常模式 |
| `/caveman status` | 显示当前模式 |

### 示例

```
用户: /caveman full
机器人: 🪨 Caveman FULL 模式已开启。

用户: React 重渲染怎么修复？
机器人: 每次渲染新建对象引用。内联 prop = 新引用 = 重渲染。用 useMemo 包裹。
```

---

## 模式

| 模式 | 风格 | Token 节省 |
|------|------|-----------|
| **lite** | 专业简洁，无废话 | ~30% |
| **full** | 默认 caveman。碎片化，无冠词 | ~65% |
| **ultra** | 电报风格，全部缩写 | ~75% |
| **wenyan** | 古典中文简洁风格 | 视语言而定 |

---

## 国际化

插件自动跟随 AstrBot 的 `bot_language` 设置。

所有面向用户的字符串（帮助、状态、错误）均通过 `.astrbot-plugin/i18n/*.json` 本地化。LLM 压缩提示词保持英文，以确保模型兼容性最佳。

如需添加新语言，在 `.astrbot-plugin/i18n/` 创建 JSON 文件（如 `ja-JP.json`）并重新加载插件。缺失的键会自动回退到中文（`zh-CN`）。

---

## 更新日志

参见 [CHANGELOG.md](CHANGELOG.md)。

---

## 许可证与归属

本项目是基于 [Julius Brussee](https://github.com/JuliusBrussee) 的
[**caveman**](https://github.com/JuliusBrussee/caveman)
创作的衍生作品，原项目采用 [MIT 许可证](https://github.com/JuliusBrussee/caveman/blob/main/LICENSE)。

原始 caveman 是一个用于 Claude Code 的 LLM 输出压缩技能生态系统。
本仓库是 **非官方的独立移植版本**，移植至 AstrBot 平台，
**与原作者无关联，也未获得原作者的认可**。

原始作品与本移植版本均采用 MIT 许可证发布。
完整法律文本请参见 [LICENSE](./LICENSE) 文件。

由 **Midwich** 移植。
