# Chatbot Deep Link 机制背景

## 是什么

多数 AI 聊天网页应用支持通过 URL 携带一个初始 prompt, 直接打开一个新对话, 这类 URL 俗称 "deep link". 最常见的形式:

```
https://<host>/<path>?q=<encoded_prompt>
```

## 编码规则

- Prompt 是 Unicode 字符串, 先转成 UTF-8 bytes, 再对 URL 中不安全的 byte 做 percent-encoding (`%XX`).
- **不是 Base64**. 除非某平台明确要求 Base64, 否则一律使用 percent-encoding.
- JavaScript: `encodeURIComponent(prompt)` (不要用 `encodeURI`, 它不转义 `&`, `?`, `#`, 会破坏 query string 的结构).
- Python: `urllib.parse.quote(prompt, safe="")` (`safe=""` 保证连 `/` 也编码, 避免 prompt 里嵌套 URL 造成歧义).

## 行为差异 (各家不保证一致, 且可能随版本变化)

- **自动发送**: 打开链接后直接把 prompt 当作已发送的消息处理 (例如 ChatGPT `?q=`).
- **仅预填**: 打开新对话, 把内容放进输入框, 用户需手动按 Enter 才会真正发送 (例如 Claude Web `/new?q=`).
- **App/CLI scheme**: 走自定义 URI scheme (例如 `claude-cli://open?q=`), 常有长度限制, 且可能需要用户滚动确认后才提交.

## 稳定性

这些机制都不是官方长期承诺的公开 API, 而是可观察到的网页/客户端行为. 做 deep link 库时应把每一种都视为 "尽力而为, 随时可能变化", 不要假设行为长期不变, 也不要在没有实测验证的前提下臆造某个 provider 的机制.

## 项目里的用法

参考同目录下按 provider 命名的文件 (如 `claude.md`, `chatgpt.md`), 记录每个已确认的 deep link 格式: host, path, query 参数名, 以及已知的行为差异. 尚未确认机制的 provider 不建立对应文件, 避免猜测性文档误导后续开发.

## 调研状态 (截至 2026-07-23)

| Provider | 状态 | 说明 |
|---|---|---|
| ChatGPT | ✅ 可用 | `chatgpt.com/?q=`, 见 `chatgpt.md` |
| Claude | ✅ 可用 | `claude.ai/new?q=` + `claude-cli://open?q=`, 见 `claude.md` |
| Google AI Mode | ✅ 实测可用 | `google.com/search?q=<p>&udm=50`, Gemini 驱动且自动提交, 见 `gemini.md` |
| Gemini 网页版 | ❓ 未能确认 | 旁证倾向原生不支持, 但缺决定性实测, 见 `gemini.md` |
| Doubao 豆包 | ✅ 可用 | `url-action?action={JSON}`, **不是 `?q=`**, 见 `doubao.md` |
| DeepSeek | ❓ 未能确认 | 见下 |
| Grok / Zai / Kimi / MiniMax | ⬜ 尚未调研 | -- |

**DeepSeek**: 没有任何公开文档描述 `chat.deepseek.com` 的 URL 参数, 汇总各家 URL 模板的社区帖子里也没有收录它. 实测 `https://chat.deepseek.com/?q=hello%20world` 在**未登录**状态下被重定向到登录页, 且该站有反自动化环境检测. **要确认只能由已登录的真人手动访问一次带 `?q=` 的 URL, 看输入框是否预填.**

> "查不到 ≠ 不支持". 在真人实测之前, 不要在库里凭猜测实现.

### 调研方法论教训 (2026-07-23)

1. **不要假设参数名是 `?q=`.** 豆包用的是 `url-action?action={"pluginId":"Send_Message","payload":{"text":...}}`, 和 `?q=` 毫无关系. 先搜索该产品实际怎么被接进"浏览器地址栏搜索引擎", 那个 URL 模板 (带 `%s` 的那种) 往往就是答案.
2. **浏览器工具的 tab 信息可能只显示 origin.** 曾据此误判 "query 被重定向丢弃", 实为显示截断. 判断真实 URL 必须执行 `location.href` 核对.
3. **未登录 / 被地区封禁的实测不能作为否定证据.** Gemini 需登录才渲染输入框, 豆包对境外 IP 直接 region-ban -- 这两种情况下什么都测不出来, 只能标 "未确认", 不能标 "不支持".
