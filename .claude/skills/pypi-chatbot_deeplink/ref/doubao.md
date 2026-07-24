# Doubao 豆包 -- Deep Link

## 机制: `url-action` + JSON, 不是 `?q=`

豆包**有** deep link 机制, 但形式和其它家完全不同 -- 它不是简单的 `?q=<prompt>`, 而是往 `url-action` 端点传一个 **JSON 编码的 action 对象**:

```
https://www.doubao.com/chat/url-action?action={"pluginId":"Send_Message","payload":{"text":"<prompt>"}}
```

- `pluginId` 固定为 `Send_Message`.
- prompt 放在 `payload.text`.
- **整个 JSON 必须 percent-encode 后再作为 `action` 的值** -- 里面的 `{`, `}`, `"`, `:`, `,` 都是 URL 里的不安全/保留字符. 各处流传的模板为了给人肉眼看, 常常直接写未编码的 JSON (浏览器会自行容错), 但**程序生成时必须编码**.
- 据来源描述是 "从 app 逆向而来" 的写法, 用途是把豆包设为浏览器地址栏的自定义搜索引擎 (URL 模板里 `%s` 就是 `payload.text` 的位置).
- 行为: 来源称为 "即时响应", 倾向于**自动提交**而非仅预填. **未经实测确认.**

## 验证状态

✅ **2026-07-23 由项目 owner 实测确认可用**: 直接把**未经任何编码**的 URL (含未编码的 JSON 和中文 prompt) 粘进地址栏, 消息可以原样发出去.

❓ **仍待确认**: 标准 percent-encoding 后的等价 URL 是否同样被正确解析. 本库默认生成编码后的形式 (理由见下), 语义上等价, 但**尚未实测**.

⚠️ **地区封禁**: 从中国大陆以外访问会被重定向到 `https://www.doubao.com/security/doubao-region-ban?source=1`, 页面上连输入框都不存在. 这是库要考虑的现实约束 -- 生成的豆包链接对境外用户可能直接不可用, 也导致 AI 助手无法自行实测.

## 编码取舍: 库为什么仍然编码

豆包的前端对未编码的 JSON 和非 ASCII 文本足够容错, 手工粘贴时确实可以不编码. 但库不能依赖这一点:

- `{`, `}`, `"`, 空格在 URL 里是不安全字符. 未编码的 URL 一旦被放进 Markdown 链接、HTML `href`、shell 命令或 HTTP header 就会断裂.
- percent-encoding 后服务端 decode 回来是**完全相同的 JSON**, 两种形式语义等价.

因此 `chatbot_deeplink.doubao.Doubao` 默认输出编码形式. 若日后发现豆包对编码形式解析失败, 再改回原样输出即可 (改 `Doubao.encode_action` 一处).

## 示例

```python
import json
from urllib.parse import quote

prompt = "请解释 Agent Harness."
action = {"pluginId": "Send_Message", "payload": {"text": prompt}}
# separators 去掉多余空格, ensure_ascii=False 保留中文原文再交给 quote 做 UTF-8 编码
encoded = quote(json.dumps(action, ensure_ascii=False, separators=(",", ":")), safe="")

doubao_url = f"https://www.doubao.com/chat/url-action?action={encoded}"
```

## 对本库的设计含义

豆包打破了 "所有 provider 都是 `host + path + ?q=<encoded_prompt>`" 的假设. `BaseDeepLink` 的抽象必须允许子类**完全自定义 query 的构造方式** (这里是先 JSON 序列化再整体编码), 而不能把 "参数名 + 编码后的 prompt" 写死在基类里.

## 参考

- https://www.cnblogs.com/MaelDNM/p/19810485 (把豆包设置为浏览器默认搜索引擎)
- https://meta.appinn.net/t/topic/86299 (小众软件论坛: 各大 AI 平台快速搜索引擎链接汇总)
- https://blog.csdn.net/Tisfy/article/details/156224252 ("豆包聊天搜索" -- 直接在 Chrome 地址栏开启对话)
