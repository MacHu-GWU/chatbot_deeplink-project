# Claude -- Deep Link

## Claude Web (claude.ai)

```
https://claude.ai/new?q=<percent_encoded_utf8_prompt>
```

- ✅ **2026-07-23 由项目 owner 实测确认有效.** (此前网上有传言称该参数于 2025-10 被移除, 经实测为不实; 官方 desktop deep link 文档也仍在列 `claude://claude.ai/new?q=TEXT`.)
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

## Project 机制: 不支持带 prompt

> **项目决策 (2026-07-23): 本库不支持 project, 只做最简单的 prompt 预填.** 以下调研结论保留备查, 无需重新调研.

结论: **可以用 deep link 打开一个指定的 Project, 但不能同时预填 prompt.**

```
claude://claude.ai/project/{project_id}     # Desktop app scheme
https://claude.ai/project/{project_id}      # 等价的 universal link
```

- `project_id` 就是网页版 project URL 末尾的 UUID.
- Anthropic 官方 deep link 文档的参数表中, `q` 只在 **new chat / Code / Cowork** 这三类路由上受支持:
  - `claude://claude.ai/new?q=TEXT`
  - `claude://code/new?q=TEXT&folder=PATH` (`prompt` 是 `q` 的别名; 另有 `mode=plan|code`, `repo=owner/name`, `branch=`)
  - `claude://cowork/new?q=TEXT&folder=PATH&file=PATH`
- **`project/{id}` 路由不在 `q` 的支持列表里** -- 即没有 "在某个 project 内新建对话并预填 prompt" 的官方 URL 形式. 想要这个效果, 只能分两步: 先用 project deep link 打开 project, 再由用户手动新建对话.
- 对本库的设计含义: 不要提供 `project_id + prompt` 的组合参数, 那会产生一个静默丢弃 prompt 的 URL. 若将来要支持 project, 应做成独立的 "打开 project" 能力, 并明确它不接受 prompt.

## 示例

```python
from urllib.parse import quote

prompt = "请解释 Agent Harness."
encoded = quote(prompt, safe="")

claude_web_url = f"https://claude.ai/new?q={encoded}"
claude_code_url = f"claude-cli://open?q={encoded}"

# Project: 只能打开, 不能带 prompt
project_url = f"https://claude.ai/project/{project_id}"
```

## 参考

- https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link (Desktop, 含完整参数表)
- https://support.claude.com/en/articles/14898120-open-the-claude-mobile-app-with-a-link (Mobile; 只文档化了 `claude://code/...` 路由, 未提及 project)
- https://code.claude.com/docs/en/deep-links (Claude Code)
