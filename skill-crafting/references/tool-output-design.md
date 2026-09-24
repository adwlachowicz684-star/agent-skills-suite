# 工具输出设计：输出就是推理的原材料

> ⭐ **工具输出 schema 不是 API 问题，是推理基底问题。**
> 每个字段名、每个可空边界、每个隐含假设，都会变成 agent 用来推理的材料。

## 目录

- [为什么输出设计独立于模型能力](#为什么输出设计独立于模型能力)
- [六条原则](#六条原则)
- [三种输出模式](#三种输出模式)
- [会翻车的地方](#会翻车的地方)
- [输出契约测试](#输出契约测试)
- [清单](#清单)

## 为什么输出设计独立于模型能力

agent 是**把工具输出当自然语言来推理**的。
当工具返回不透明标识符、面向机器的字段、或超大载荷时：

```
① 浪费上下文
② 让模型更难提取真正重要的东西
③ ⭐ 制造幻觉机会
```

> 一个设计糟糕的工具响应**不只是浪费 token——
> 它训练 agent 去做出"happy path 成立、边界情况失败"的推断。**

## 六条原则

**① 用语义等价物替换标识符**

```json
❌ {"id": "a3f4b2c1-...", "type": "application/vnd.openxmlformats-...wordprocessingml.document"}
✅ {"name": "Q3 Budget Review", "file_type": "Word document"}
```

> UUID 和 MIME 串是任意字节序列。
> ⭐ **把字母数字 ID 解析成语义化的名字，能显著降低检索任务中的幻觉**。

需要返回内部 ID 时，**同时带上实体名**：

```json
{"ticket_id": "T-4821", "title": "Payment timeout in checkout"}
```

这样 agent 不用再查一次就能推理。

**② 只返回与决策相关的字段**

返回 40 个字段而 agent 只需要 name 和 email：

```
→ 38 个字段是浪费
→ ⭐ 而且每个都是一次幻觉机会
   （agent 可能引用、编造或误读它没被要求处理的字段）
```

把扩展输出做成**可选模式**，而不是默认全给。

**③ 在工具层做分页与过滤**

```
✅ 接受过滤参数（status=open, created_after=...），返回前先应用
✅ 返回带 cursor 的一页，不是无界列表
✅ ⭐ 提供合理的默认值（limit=20）防止意外灌爆上下文
```

让 agent 自己去过滤 = 它要么幻觉出一个过滤条件，要么把整个数据集加载进上下文。

**④ 用 enum 表达响应粒度**

```json
{"response_format": "concise"}   // 仅摘要字段
{"response_format": "detailed"}  // 完整记录
```

让 agent 根据当前上下文预算自己选，而不是总是给全量或总是给最小集。

**⑤ 错误要可操作**

```json
❌ {"error": "400 Bad Request"}
✅ {"error": "Invalid date range: end_date must be after start_date.
             Received start=2024-03-01, end=2024-02-01."}
```

**"可操作的提示"模式**：
参数有歧义时，把合法选项直接写进错误消息——

```
Error: Invalid 'region' parameter.
       Supported regions: [us-east-1, us-west-2, eu-central-1].
```

agent 下一轮就能自我纠正，不需要人介入。

**⑥ 成功与失败不能混在一个形状里**

> ⭐ **绝不要用 HTTP 200 携带错误信息的 body。**

每一次调用必须**明确地**是成功或失败，
且**成功数据和错误信号不能出现在同一个响应形状里**。

## 三种输出模式

**摘要优先**——探索类工具（搜索、列目录）先给高层摘要 + top N：

```
Found 12 matching files. Top 3:
  index.js (Modified 2h ago)
  styles.css (Modified 1d ago)
  utils.js (Modified 5m ago)
Use 'read_file' for specific content.
```

**上下文窗口**——搜索/grep 时给匹配点周围几行，
让 agent 不用再调一次工具就能理解上下文：

```
File: auth.py
Line 42: # Validate session
Line 43: if session.is_expired():   <-- MATCH
Line 44:     return Redirect("/login")
```

**结构化优先**——agent 解析结构化数据比散文可靠。
避免 ASCII 边框表格、装饰性头部、以及"我找到了以下结果……"这类开场白。

## 会翻车的地方

**① 欠规格化**
为特定任务裁剪的 schema 漏掉了 agent 意外需要的字段
→ 它要么幻觉一个值，要么多跑一趟
→ **有时比一次性返回完整记录还贵**。

**② concise/detailed 选错**
agent 挑了错的模式，在**不知道自己数据不全**的情况下继续操作。
→ 缓解：**让 agent 在调用前先想清楚它需要什么数据**。

**③ schema 漂移**
"干净的默认值"被第一个用例塑形，新任务来了就不匹配了。
→ 必须**给 schema 版本化**，或把扩展放在 opt-in 后面。

**④ 开发者便利型输出**（反模式）

```
为调试方便而返回一切：
  原始数据库记录 · 完整对象图 · 内部标识符 · debug 字段
```

这是最常见的错误来源——**工具是为 agent 造的，不是为造工具的人**。

## 输出契约测试

大多数团队跳过的最后一步：

```
① Pydantic 模型作为输出 schema 的基线
   ——每次响应进 agent 循环前先验证
   捕获类型不匹配、必需字段缺失、文档与实际返回的形状漂移

② 在边界验证，而不是让它传播进推理
```

三级递进，对应越来越强的保证：

```
自然语言文档 → JSON Schema → ⭐ 带字段级诊断标注的 JSON Schema
```

**多数团队停在第一级，然后困惑为什么 agent 行为不一致。**

UC Berkeley 对 1600+ 条多 agent 执行轨迹的分析发现：
**schema 问题是最常见的根因之一**（参数格式错、类型不匹配、必需字段缺失）。

> ⭐ 这些表现为"agent 推理失败"，但**起源于 schema 设计**。
> **独立于 agent 测试 schema，能在 agent 之前抓到它们。**

## 清单

```
[ ] 默认返回精简摘要？
[ ] 潜在的大输出已分页或限流？
[ ] 错误明确且可操作（含合法选项）？
[ ] 输出是结构化的（JSON/YAML/key-value）？
[ ] 工具描述里含示例调用？
[ ] 装饰性格式（ASCII 艺术、ANSI 颜色码）已清除？
[ ] ⭐ 标识符已替换为语义等价物？
[ ] 每个字段都标注了 required / optional / nullable？
[ ] 字段描述解释语义而非重复类型？
[ ] ⭐ 每次响应都过了 schema 校验？
```

**字段描述那条值得展开**：
在 function calling 里，字段描述会进入模型上下文。

```
❌ "string"
✅ "订单下达的 ISO 8601 时间戳，UTC"
```

> schema 里的歧义会变成 agent 信念里的歧义。
