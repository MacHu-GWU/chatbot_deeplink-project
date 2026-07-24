# ChatGPT -- Deep Link

## ChatGPT Web (chatgpt.com)

```
https://chatgpt.com/?q=<percent_encoded_utf8_prompt>
```

- ✅ **2026-07-23 由项目 owner 确认可用.**
- 打开后, `q` 的内容作为新对话的输入被处理.
- 具体是 "打开即自动发送" 还是 "先显示再进入对话", 可能随网页版本和登录状态变化. 有社区汇总明确记录 "`q` 会被填成 prompt, 但实际仍需手动点击发送" -- 所以**不要把 ChatGPT 当成可靠的自动提交**, 保守起见按 "预填" 对待 -- OpenAI 官方确认浏览器地址栏搜索可以自动触发 ChatGPT 对话, 但没有发布一份稳定的 `?q=` deep link API 规范. 因此在做 Launcher 抽象时, 应把它当作 "可用的 web 行为", 而不是有长期兼容承诺的正式 API.
- 编码规则见 `about.md`: UTF-8 + percent-encoding, 不是 Base64.

## Project 机制: 不支持带 prompt

> **项目决策 (2026-07-23): 本库不支持 project, 只做最简单的 prompt 预填.** 以下调研结论保留备查, 无需重新调研.

结论: **Project 有自己的 URL, 但没有任何官方或已验证的方式在打开 project 时预填 prompt.**

```
https://chatgpt.com/g/g-p-<project_id>/project    # 打开 project 主页
```

- OpenAI 没有发布过 project 作用域的 URL 参数规范. `?q=` 只在**顶层** `chatgpt.com/?q=` 上被观察到有效, 落点是一个不属于任何 project 的普通新对话.
- 同源的 Custom GPT (`/g/g-<id>`) 也是一样的情况: 社区长期有 "希望 URL 能直接把 prompt 送进指定 GPT" 的 feature request, 到目前为止仍是**未实现的诉求**, 这反过来说明 `/g/...` 路由不接受 prompt 参数.
- 对本库的设计含义: 同 Claude -- 不要提供 `project_id + prompt` 的组合参数. 拼一个 `/g/g-p-<id>/project?q=...` 出来只会静默丢掉 prompt, 比报错更糟.

## 示例

```python
from urllib.parse import quote

prompt = "请解释 Agent Harness."
encoded = quote(prompt, safe="")
chatgpt_url = f"https://chatgpt.com/?q={encoded}"

# Project: 只能打开, 不能带 prompt
project_url = f"https://chatgpt.com/g/g-p-{project_id}/project"
```

## 参考

- https://community.openai.com/t/enable-direct-url-query-support-for-custom-gpts/1113619 (feature request, 未实现)
- https://community.openai.com/t/deep-linking-for-custom-gpts-with-url-parameters-launch-context/1370871
- https://github.com/combinatrix-ai/prompt-chatgpt-via-url-parameter (社区对 `?q=` / `?model=` 的观察记录)
