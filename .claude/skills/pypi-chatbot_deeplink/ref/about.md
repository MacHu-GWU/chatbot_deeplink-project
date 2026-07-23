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
