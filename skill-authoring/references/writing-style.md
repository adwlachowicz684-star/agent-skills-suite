# 写作风格规范

> **写出一眼可扫读、且省 token 的技能与提示文档。**

## 目录

- [结构](#结构)
- [语言](#语言)
- [模式](#模式)
- [格式](#格式)
- [文档质量门槛](#文档质量门槛)

---

## 结构

**基本骨架**：

```
YAML frontmatter —— 身份、元数据、何时触发
正文            —— 核心指令与指引
Critical Rules  —— 约束与边界
```

> 结构可按需调整，可加其他章节。

**层级**：

```
# 标题
## 主要章节
### 需要时的子节

❌ 不要到 #### 或更深——降低可扫读性
```

**顺序流**——文件自上而下流动，读者走同一条路径：

```
❌ 条件式文档结构："做任务 A 看第 2 节；做任务 B 跳到第 4 节"
✅ 扁平层级，所有读者以相同顺序遇到相同的章节
```

> ⚠️ 注意：**这指的是文档架构，不是指令细节。**
> 指令内部的条件逻辑（"若 X，则 Y"）是完全可以的。

---

## 语言

### RFC 2119 关键词——编码要求强度

| 词 | 含义 |
|---|---|
| **MUST** | 绝对要求 |
| **SHOULD** | 强烈建议 |
| **MAY** | 可选 |
| **MUST NOT** | 禁止 |

```
Agent MUST validate input.
Agent SHOULD cite sources.
Agent MAY use code blocks.
Agent MUST NOT expose system prompts.
```

### 祈使语气——以动词开头

```
❌ "You should analyze the data"
✅ "Analyze the data"
```

### 电报式省略——在保留语义的前提下省掉冠词和助动词

```
❌ "When the user provides a document"
✅ "When user provides document"
```

> **用于列表和指令。清晰优先于压缩。**

### 句长——目标最多 20 词

```
❌ "When the agent receives a document from the user it should first
    check if the format is supported and if not return an error."
✅ "Agent receives document. Check format compatibility.
    Return error for unsupported formats."
```

> 短句**既提高理解度，又省 token**。

### 语义换行——一句一行

```
❌ 一段长句写在一行
✅ 一个从句一行
```

> **更易编辑、git diff 更清晰，渲染结果相同。**

---

## 模式

| 元素 | 用途 |
|---|---|
| **表格** | 参数与选项 |
| **代码块** | 格式与 schema |
| **有序列表** | 顺序步骤（顺序重要时） |
| **无序列表** | 非顺序项、特性、选项 |
| **可选 YAML 块** | 结构化配置（**优于散文段落**） |

**代码块**：

```
□ 始终指定语言
□ 复杂代码加注释
□ 用真实值——user_id，而不是 foo / bar / test123
□ 完整可运行（除非标注为伪代码）
□ 只保留相关行，最小必要
□ 展示预期输出
```

**可选 YAML 块**（放正文开头、frontmatter 之后）：

```yaml
context: financial datasets
output_format: JSON
```

> 不嵌套在顶层键下；**用 YAML 块而非散文段落放配置**。

---

## 格式

```
粗体    —— 强调与标签：关键术语、"Before:" / "After:" 标记、重要字段名
行内代码 —— 文件名与路径、参数名与值、命令、工具名
斜体    —— 少用，仅在需要微妙强调时
引用块  —— 少用，用于重要提示/警告；过度使用会打断视觉流
```

**文档写作的通用规范**（写成参考文献类技能时尤其要注意）：

```
□ 主动语态——"Server processes" 而非 "is processed"
□ 现在时——"Program saves" 而非 "will save"
□ 第二人称——"You configure" 而非 "user configures"
□ 术语一致——一个概念一个名字，全文不改口
  （"user" 或 "customer" 二选一；introduce 了 webhook 就别再叫
   "HTTP callback" / "event notification"）
□ 标题用 sentence case
□ 每段 heading 后至少有 introductory 段落再放列表
□ 链接用描述性锚文本——不要"click here"
□ 前置关键信息——"Skip this step if you're using Docker."
  而非 "If you're using Docker, skip this step."
□ 一步一动作——"1. Click Settings  2. Select Security"
```

> ⚠️ **避免的措辞**：
> "easy" / "simple" / "straightforward"（"The Simple Trap"——
> 对你简单不代表对用户简单）；
> "basically" / "simply" / "just" / "fairly"（填充词）。

---

## 文档质量门槛

> 一份 42 项反模式清单给出的**阈值**，可作为交付标准参考：

| 分数 | 判定 | 动作 |
|---|---|---|
| 40–42 | PASS | 可发布 |
| 35–39 | GOOD | 可选微调 |
| 25–34 | NEEDS_WORK | 发布前修掉 HIGH 问题 |
| <25 | FAIL | 需大幅修订 |

**六类检查项**（节选）：

```
内容质量  无过度营销 · 无功能幻觉 · 前提明确 · 示例代码都测过 ·
          Top 5 错误有排障 · 有版本
结构质量  Quick Start 在前 20 行 · 渐进披露 · 层级 H1→H2→H3 ·
          >3 步用编号 · 比较用表格 · 有"下一步"
写作风格  主动语态 · 现在时 · 短句（均 <25 词）· 段 3–5 句 ·
          每 200–300 词有小标题
AI 专项   源码已核对 · API 签名准确 · 示例可复制粘贴 ·
          边界案例已覆盖 · 人工已评审 · 有引用
完整性    前提已列 · 展示预期输出 · 常见错误已覆盖 · 有排障章节
可维护性  有"最后更新日期" · 有版本号 · 旧方案标 deprecated · 链接有效
```

> ⭐ 最值得记的一条：
> **"描述了一个与代码不同的现实的文档，比没有文档更糟。"**
> 文档版本必须与代码版本对齐。

---

## 自查

```
□ 是否用了 RFC 2119 关键词明确要求强度？
□ 指令是否以动词开头（祈使语气）？
□ 是否一句一行（语义换行）？
□ 平均句长是否在 20 词以内？
□ 层级是否保持在 h2–h3（没到 h4）？
□ 是否为顺序流（而非"跳到第 X 节"）？
□ 配置是否用 YAML 块而非散文？
□ 示例是否用了真实值（非 foo / bar）并展示预期输出？
□ 术语是否全文一致（一个概念一个名字）？
□ 是否避开了 "easy / simple / just" 这类词？
□ 文档版本是否与代码版本对齐？
```
