# 技能依赖注入：委托 / 链式 / 配置 / 共享服务

> 相关：《skill-orchestration》的 `composition-patterns-types.md` ·
> `skill-chaining-composition.md` · `collision-arbitration.md` ·
> 《skill-patterns》的 `five-design-patterns.md`
> 前置：那些讲"组合的类型与冲突怎么解"，
> 这份讲⭐ **组合的四种具体写法**，每种都给一个可直接照抄的正文骨架。

---

## 目录

- [1. ⭐ 依赖注入在技能里是什么意思](#1--依赖注入在技能里是什么意思)
- [2. ⭐⭐ 模式一：委托](#2--模式一委托)
- [3. ⭐ 模式二：链式](#3--模式二链式)
- [4. ⭐⭐ 模式三：配置注入](#4--模式三配置注入)
- [5. ⭐⭐ 模式四：共享服务技能](#5--模式四共享服务技能)
- [6. ⭐⭐ 三种写法的正反对照](#6--三种写法的正反对照)

---

## 1. ⭐ 依赖注入在技能里是什么意思

```
传统软件：把依赖传进函数，而不是让函数自己创建
技能：⭐⭐ 设计一个技能，让它⭐ 调用另一个技能来完成某个子任务，
     而不是自己处理一切
```

**对照**（同一个需求，两种写法）：

```
需求：从 PDF 抽取数据 → 转成表格 → 做分析

❌ 无依赖注入：一个巨型技能试图处理全部三步
✅ ⭐ 依赖注入：三个聚焦的技能
   pdf   负责抽取
   xlsx  负责表格操作
   第三个技能编排整条流水线
```

> ⭐ 这与 `composable-patterns.md` 的"一职责一技能"一致，
> 但这份给的是⭐ **接口层面的写法**——即"怎么在正文里调用另一个技能"。

---

## 2. ⭐⭐ 模式一：委托

> ⭐⭐ **一个技能调用另一个技能处理特定子任务，然后继续处理结果。**

**骨架**（可直接照抄）：

```markdown
You process incoming invoices and extract line items.
When given an invoice PDF:
1. First invoke /pdf extract text and tables from {filename}
2. Parse the extracted content to identify: vendor name,
   invoice number, date, line items
3. Format the extracted data as structured JSON
4. Return the structured result with confidence scores
```

> ⭐⭐ 这个例子的精妙之处在于**双向无知**：
>
> ```
> ⭐ pdf 技能不需要知道"发票"是什么——它只负责抽取内容
> ⭐ invoice-processor 不需要理解 PDF 内部——它只接收抽取好的文本
> ```
>
> ⭐⭐⭐ **双向无知正是解耦的证据**：
> 如果两个技能互相都需要知道对方的领域细节，那它们其实是一个技能。

---

## 3. ⭐ 模式二：链式

> ⭐ **多个技能顺序连接，每个技能的输出成为下一个的输入。**

**骨架**：

```markdown
You run contracts through a review pipeline.
1. /pdf extract all text from {contract_file}
2. /supermemory Are there similar contracts in the knowledge base?
3. Compare extracted clauses against known risky patterns
4. Generate a risk assessment summary

Output format:
- Risk level: LOW | MEDIUM | HIGH
- Key concerns: [list]
- Recommended actions: [list]
```

**流向**：

```
抽取 → 检索上下文 → 分析 → 总结
⭐ 每个技能处理一个领域
⭐⭐ 编排技能持有工作流逻辑，但⭐ 把实际工作委派给专门技能
```

> ⭐⭐ 与委托的区别：**链式是"输出接输入"，委托是"调用后拿回结果继续"**。
> 前者适合数据管道，后者适合"我需要一个能力来帮我完成这一步"。

**一个完整的三段式样例**（pdf → xlsx → docx）：

```
1. /pdf  extract tables from monthly-data.pdf
2. /xlsx create report.xlsx with: raw data sheet, summary sheet, charts
3. /docx create monthly-report.docx embedding ...
```

---

## 4. ⭐⭐ 模式三：配置注入

> ⭐⭐ **依赖注入在"技能之间传配置"时变得真正强大——
> 不硬编码行为，而是接受参数来控制依赖技能的行为。**

**骨架**：

```markdown
Parameters:
- source_file: path to the document
- schema: JSON object defining fields to extract
- confidence_threshold: minimum extraction confidence (default: 0.8)

Workflow:
1. /pdf extract all tables and key-value pairs from {source_file}
2. Map extracted content to the fields defined in {schema}
3. Filter out extractions with confidence below {confidence_threshold}
4. Return structured data matching the schema
```

**调用**：

```
/data-extractor source_file=report.pdf   schema={"fields": ["revenue", "expenses", "profit"]}
```

> ⭐⭐⭐ 关键在最后那段解释：
> **"通过指定要抽取什么来间接配置 pdf 技能，
> 而不是告诉 pdf 技能具体该怎么做。"**
>
> 这正是 `avoid-railroading`（别把 Claude 钉死）在组合场景下的应用：
> **你给的是意图（要哪些字段），不是实现（怎么解析 PDF）**。

> ⭐ 顺带印证了一条已有规则：**默认值要写出来**（`confidence_threshold (default: 0.8)`），
> 否则模型会自己猜一个，而每次猜的可能不一样。

---

## 5. ⭐⭐ 模式四：共享服务技能

> ⭐⭐ **创建"共享服务技能"——⭐ 专门设计给其他技能调用的实用技能，
> 而不是给用户直接调用的。**

**骨架**（json-formatter）：

```markdown
You format and validate JSON data. When invoked by another skill:
- Accept raw JSON or JSON strings as input
- Pretty-print with 2-space indentation
- Validate syntax and report any errors
- Optionally compact minified JSON
Always return valid JSON output or clear error messages.
```

**别的技能怎么用它**：

```
/tdd generate tests for auth.py, then /json-formatter format the test output
/supermemory store {result}, then /json-formatter validate the stored JSON
```

> ⭐⭐⭐ 这一类技能的设计要点与常规技能不同：
>
> ```
> ⭐ 它的用户是另一个 agent，不是人
> → ⭐ description 应该写"被其他技能调用时"，而不是"当用户想格式化 JSON 时"
> → ⭐ 输入输出必须是结构化的（文本会被上游解析）
> → ⭐⭐ 必须"总是返回有效 JSON 或明确的错误信息"
> ```
>
> ⭐⭐ 最后那条尤其关键：**共享服务技能不能有"偶尔什么都不输出"的情况**，
> 否则整条链会在中间断掉，而且很难定位。

---

## 6. ⭐⭐ 三种写法的正反对照

| | 写法 | 适用 |
|---|---|---|
| ❌ | 一个技能里写死全部三步 | 无（这是巨型技能） |
| ⭐ | **委托**：调用一个技能拿回结果，继续处理 | 我需要某个能力来完成这一步 |
| ⭐ | **链式**：A 的输出直接是 B 的输入 | 数据管道 |
| ⭐⭐ | **配置注入**：传参数间接控制依赖技能 | 同一个依赖、不同用法 |
| ⭐⭐ | **共享服务**：造一个专门给别人调用的技能 | 多处重复同一确定性操作 |

**一条贯穿的原则**（与 `solid-for-skills.md` 的依赖倒置对应）：

```
❌ "用这些 flag 调 qmd"
✅ ⭐ "搜索知识库"
   → ⭐ 说意图不说工具，依赖技能才能被替换
```

> ⭐ 组合起来的判断顺序：
> **先问"这一步是不是确定性的重复操作" → 是就造共享服务技能；
> 再问"是不是数据管道" → 是就链式；
> 否则用委托；需要参数化时加配置注入。**

---

## 速查

```
□ ⭐ 依赖注入 = ⭐ 让技能调用另一个技能，而不是自己处理一切
□ 巨型三步技能 → pdf + xlsx + 编排技能

□ ⭐⭐ 委托：调用后拿回结果继续
   ⭐⭐ 双向无知 = 解耦的证据
   （pdf 不知发票，invoice-processor 不知 PDF 内部）
□ ⭐ 链式：输出接输入，适合数据管道
□ ⭐⭐ 配置注入：⭐ 传意图不传实现
   （"要哪些字段" 而非 "怎么解析 PDF"）
   ⭐ 默认值必须写出来
□ ⭐⭐ 共享服务：⭐ 专门给别的技能调用
   ⭐ description 写"被其他技能调用时"
   ⭐⭐ 必须总是返回有效结构化输出（否则链在中间断掉且难定位）

□ ⭐ 选择顺序：确定性重复→共享服务；数据管道→链式；否则委托；需参数化→配置注入
□ ⭐ 说意图不说工具，依赖才能被替换
```

**一句话**：

> ⭐⭐ **双向无知是解耦的证据——pdf 技能不需要知道"发票"是什么，
> invoice-processor 也不需要理解 PDF 内部；如果互相都需要知道对方的领域细节，
> 那它们其实是一个技能。**
