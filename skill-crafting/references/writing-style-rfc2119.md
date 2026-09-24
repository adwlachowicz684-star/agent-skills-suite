# 文风规范：RFC 2119、语义换行、句子长度

> 相关：《skill-crafting》的 `imperative-style.md` ·
> `write-reasons-not-rules.md` · `anti-patterns-catalog.md`
> 前置：`imperative-style.md` 讲祈使句 vs 第二人称，
> 这份讲⭐ **更细的可执行文风约束**——关键词、换行、句长、层级。

---

## 目录

- [1. ⭐ RFC 2119 关键词](#1--rfc-2119-关键词)
- [2. ⭐⭐ 语义换行](#2--语义换行)
- [3. ⭐ 祈使语气与电报式缩减](#3--祈使语气与电报式缩减)
- [4. ⭐ 句子长度 20 词上限](#4--句子长度-20-词上限)
- [5. 顺序流与层级](#5-顺序流与层级)
- [6. 排版元素怎么用](#6-排版元素怎么用)

---

## 1. ⭐ RFC 2119 关键词

> ⭐ **用它来编码"要求强度"**，而不是全靠语气词。

```
MUST        绝对要求
SHOULD      强烈建议
MAY         可选
MUST NOT    禁止
```

**对照**：

```
❌ 前：
   "确保 agent 总是在处理输入前验证用户输入，这很重要。
    agent 还应该在做事实性声明时尽量包含引用，
    因为这有助于用户验证信息。"

✅ 后：
   ## Constraints
   Agent MUST validate user input before processing.
   Agent SHOULD include citations for factual claims.
```

> ⭐ 好处是**强度可查**：你可以数一数 MUST 有多少条，
> 如果一屏好几个就该降级（与 `write-reasons-not-rules.md` 的三成原则呼应）。

**注意一个张力**：

```
RFC 2119 用 "Agent MUST ..."（第三人称主语）
《imperative-style》建议祈使句 "Validate input"（动词开头）

⭐ 两者不矛盾，是两种流派：
   祈使句更省 token、更直接
   RFC 2119 更精确、强度可分级
⭐ 建议：普通步骤用祈使句，⭐ 关键约束用 RFC 2119
```

---

## 2. ⭐⭐ 语义换行

> ⭐ **一个从句一行。** 渲染结果完全相同，但编辑和 diff 更好。

```
❌ 前：
   When the agent receives input validate it first and if validation
   fails respond with an error message.

✅ 后：
   When agent receives input validate it first.
   If validation fails respond with error message.
```

**三个具体好处**：

```
① 更容易编辑
② ⭐⭐ 更好的 git diff
   ——改一个从句只标一行，而不是整段
③ 渲染输出不变
```

> ⭐ 第 ② 条对团队协作特别值钱：
> `skill-ownership-changeflow.md` 说"git 历史是定位回归的第一工具"，
> 而语义换行让这个工具**精确到行**。

---

## 3. ⭐ 祈使语气与电报式缩减

**祈使语气**：以动词开头

```
❌ "You should analyze the data"
✅ "Analyze the data"
```

**电报式缩减**：保留语义的前提下丢掉冠词和助词

```
❌ "When the user provides a document"
✅ "When user provides document"
```

```
⭐ 用在列表和指令里
⭐ ⭐ 但"保留清晰优先于压缩"——读不懂的压缩是负收益
```

---

## 4. ⭐ 句子长度 20 词上限

```
⭐ 目标：≤20 词。
   更短的句子提升理解度，也减少 token。
```

**对照**：

```
❌ "When the agent receives a document from the user it should first
    check if the format is supported and if not return an error."
   （一个长句）

✅ "Agent receives document.
    Check format compatibility.
    Return error for unsupported formats."
   （拆成三个短句）
```

> ⭐ 与"语义换行"配合：不是硬砍，而是**把复合句拆成独立短句**。

---

## 5. 顺序流与层级

**顺序流**：文件自上而下，所有读者走同一条路径

```
❌ 条件式文档结构：
   "任务 A 看第 2 节；任务 B 直接跳到第 4 节"
```

> ⭐ 这个禁止很反直觉但理由充分：
> **条件式的文档结构会让不同的读者（不同轮次的模型）看到不同的内容，
> 行为就不一致了。**

**扁平层级**：

```
❌ 用 #### 或更深（降低可扫读性）
✅ ## 主要章节，必要时 ### 子章节
```

> ⭐ 注意区分：**文档结构要扁平，指令内部的条件逻辑没问题**
> （"If X, then Y" 完全可以）。这个原则约束的是**文档架构**，不是指令细节。

---

## 6. 排版元素怎么用

| 元素 | 用途 |
|---|---|
| **表格** | 参数与选项（⭐ 参考数据用表格而非散文） |
| **代码围栏** | 格式与 schema（BNF、YAML、JSON） |
| **粗体** | 强调与标签（关键术语、"Before:"/"After:"、重要字段名） |
| **行内代码** | 文件名与路径、参数名与值、命令、工具名 |
| *斜体* | ⭐ 少用 |
| > 引用块 | ⭐ 少用（重要警示才用，过度会打断视觉流） |

**配置优先用 YAML 块，而不是散文段落**：

```yaml
context: financial datasets
output_format: JSON
```

> ⭐ 不要嵌在顶层键下面；需要结构化配置时，
> ⭐ **优先 YAML 块而不是散文**。

---

## 速查

```
□ ⭐ 用 RFC 2119 编码强度：MUST / SHOULD / MAY / MUST NOT
□ ⭐ 普通步骤用祈使句，关键约束用 RFC 2119（两者可共存）
□ ⭐⭐ 语义换行：一个从句一行（渲染不变，git diff 精确到行）
□ ⭐ 祈使语气：动词开头
□ ⭐ 电报式缩减，但"保留清晰优先于压缩"
□ ⭐ 句子 ≤20 词，复合句拆成独立短句
□ ⭐ 顺序流：禁止"任务A看第2节、任务B跳第4节"式架构
□ ⭐ 层级停在 ## / ###，不用 ####
□ 参考数据用表格；格式/schema 用代码围栏
□ 配置用 YAML 块，不用散文
□ 斜体和引用块都要少用
□ ⭐ 可以数 MUST 的个数自检：一屏好几个就该降级
```

**一句话**：

> ⭐ **语义换行让 git diff 精确到行——
> 而"git 历史是定位回归的第一工具"。这两条是配套的。**
