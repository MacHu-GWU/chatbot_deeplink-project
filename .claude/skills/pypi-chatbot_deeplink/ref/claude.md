# Claude -- Deep Link

## Claude Web (claude.ai)

```
https://claude.ai/new?q=<percent_encoded_utf8_prompt>
```

- 打开一个新对话, 把 `q` 的内容放入输入框.
- **仅预填, 不自动发送** -- 用户需要自己按 Enter 或点击发送按钮才会真正提交. 这点和 ChatGPT 的 `?q=` (打开即可能自动发送) 不同, 在做 Launcher/Command 抽象时要单独标注这个差异.
- 编码规则见 `about.md`: UTF-8 + percent-encoding, 不是 Base64.

## Claude Code (CLI) Deep Link

```
claude-cli://open?q=<percent_encoded_utf8_prompt>
```

- Anthropic 官方文档记录的机制, 是 Claude Code/CLI 专属的 deep link, 与 `claude.ai/new?q=` 网页接口不是同一套, 不能混用.
- Query 长度上限约 **5,000 字符**.
- 对于较长的 prompt, Claude Code 会要求用户先滚动查看完整内容, 确认后才真正提交/执行.

## 示例

```python
from urllib.parse import quote

prompt = "请解释 Agent Harness."
encoded = quote(prompt, safe="")

claude_web_url = f"https://claude.ai/new?q={encoded}"
claude_code_url = f"claude-cli://open?q={encoded}"
```
