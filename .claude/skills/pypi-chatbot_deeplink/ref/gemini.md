# Gemini -- Deep Link

## 结论速览 (2026-07-23 调研)

| 入口 | 状态 | URL |
|---|---|---|
| Google AI Mode (Gemini 驱动) | ✅ **实测可用, 自动提交** | `https://www.google.com/search?q=<encoded>&udm=50` |
| Gemini 网页版对话 | ❓ 未能确认, 旁证倾向不支持 | `https://gemini.google.com/app?q=...` |

## ✅ Google AI Mode -- 可用的 Gemini 系 deep link

```
https://www.google.com/search?q=<percent_encoded_utf8_prompt>&udm=50
```

- **2026-07-23 实测通过**: 未登录状态下直接打开, 页面呈现 "AI Mode Conversation: <prompt>" 并给出完整的 AI 回答.
- **自动提交** -- 不需要用户再按 Enter, 打开即出答案. 这点和 ChatGPT/Claude 的预填行为不同.
- `udm=50` 是 AI Mode 的开关参数 (`udm` 社区逆向解读为 "User Display Mode"). AI Mode 由 Gemini 驱动, 但它是 **Google 搜索里的 AI 对话**, 不等同于 `gemini.google.com` 上的 Gemini App 会话 -- 不共享对话历史, 界面和能力也不同. 在库里暴露时应明确命名 (如 `GoogleAIMode`), 不要伪装成 "Gemini".
- 有资料称 `udm=50&aep=11` 已被合并为 `aep=11`, 即 `aep=11` 也能进 AI Mode. 未实测, 当前以 `udm=50` 为准.
- 稳定性提示: `udm` 是未公开文档的搜索内部参数, 属于典型的 "可观察行为", Google 随时可能改.

## ❓ Gemini 网页版 (gemini.google.com)

`https://gemini.google.com/app?q=...` / `?prompt=...` **大概率原生不支持**, 但**本次未能取得决定性证据**.

旁证 (都指向不支持):

- 社区 Chrome 扩展 `gemini-url-prompt` 的 README 开宗明义: Gemini 不原生支持通过 URL 传 prompt, 扩展就是为填补这个空缺而存在, 靠注入脚本模拟 `input` / `textInput` 事件把文字塞进输入框.
- 网上 "`gemini.google.com/app?prompt=` 能自动填充并提交" 一类说法, **前提都是装了上述扩展**, 不是原生能力.
- Chrome 官方帮助文档说明 Gemini **不能**被设置为自定义搜索引擎; Chrome 里用 `@gemini` 唤起是浏览器内建功能, 走的不是 URL 参数.
- 小众软件论坛那份 "各大 AI 平台快速搜索引擎链接" 汇总里收录了豆包/ChatGPT/Perplexity 等, **唯独没有 Gemini 的可用模板**.
- HN 上有面向 Gemini 团队的公开请求帖, 陈述该参数至今不受支持.

为什么没有定论:

> ⚠️ 本文件早先版本写过 "实测 `?q=` 被重定向丢弃" -- **那是错误的**. 当时误把浏览器工具只显示 origin 的 tab 信息当成了真实 URL. 重新用 `location.href` 核对, `https://gemini.google.com/app?q=hello%20world` 的 query **完整保留**, 并没有被剥离.
>
> 真正的障碍是: Gemini 需要登录才会渲染输入框, 未登录态下无从判断 `q` 到底有没有被消费. **要下定论, 只能由已登录的真人打开一次该 URL, 看输入框是否预填.**

## 连带确认: Google AI Studio 不支持

`aistudio.google.com` 没有官方的 prompt URL 参数. 社区提过 `.../app/prompts/new_chat?model=...&prompt=<PROMPT>`, 但那只是一个 **feature request**, Google 方面仅回复 "已收到反馈", 从未确认实现. 不要把这个提案格式当作可用 URL.

## 示例

```python
from urllib.parse import quote

prompt = "请解释 Agent Harness."
encoded = quote(prompt, safe="")

# 可用: Google AI Mode (自动提交)
ai_mode_url = f"https://www.google.com/search?q={encoded}&udm=50"
```

## 参考

- https://en.wikipedia.org/wiki/Google_AI_Mode
- https://brightdata.com/blog/web-data/google-search-url-parameters (udm 参数汇总)
- https://github.com/elliot79313/gemini-url-prompt (扩展 README, 明说原生不支持)
- https://news.ycombinator.com/item?id=46761567 (HN: 请求 Gemini 增加 URL query parameter 支持)
- https://support.google.com/chrome/answer/95426 (Chrome: Gemini 不可设为自定义搜索引擎)
- https://discuss.ai.google.dev/t/set-prompt-to-aistudio-via-url-query-parameter/77309 (AI Studio feature request, 未实现)
