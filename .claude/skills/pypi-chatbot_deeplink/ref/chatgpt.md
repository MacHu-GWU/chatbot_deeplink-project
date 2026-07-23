# ChatGPT -- Deep Link

## ChatGPT Web (chatgpt.com)

```
https://chatgpt.com/?q=<percent_encoded_utf8_prompt>
```

- 打开后, `q` 的内容作为新对话的输入被处理.
- 具体是 "打开即自动发送" 还是 "先显示再进入对话", 可能随网页版本和登录状态变化 -- OpenAI 官方确认浏览器地址栏搜索可以自动触发 ChatGPT 对话, 但没有发布一份稳定的 `?q=` deep link API 规范. 因此在做 Launcher 抽象时, 应把它当作 "可用的 web 行为", 而不是有长期兼容承诺的正式 API.
- 编码规则见 `about.md`: UTF-8 + percent-encoding, 不是 Base64.

## 示例

```python
from urllib.parse import quote

prompt = "请解释 Agent Harness."
encoded = quote(prompt, safe="")
chatgpt_url = f"https://chatgpt.com/?q={encoded}"
```
