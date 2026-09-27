# 示例与契约

## 目录

- [四个必备正文段落](#四个必备正文段落)
- [示例怎么写](#示例怎么写)
- [步骤原子性](#步骤原子性)
- [验收清单](#验收清单)
- [契约字段](#契约字段)
- [确定性 vs 概率性](#确定性-vs-概率性)

---

## 四个必备正文段落

一份完整的 SKILL.md 正文建议包含四段：

| 段落 | 作用 |
|---|---|
| **Instructions** | 编号步骤，祈使句，写明确切命令。**agent 会逐字遵循** |
| **Constraints** | 必须遵守的规则，防止常见错误、贯彻团队约定 |
| **Verification** | **agent 可用来自检自己输出的清单**，每项独立可验证 |
| **Examples** | 具体的输入/输出对 |

> **模糊的约束没有用**。"写干净的代码" ❌ → "函数不超过 50 行" ✅

---

## 示例怎么写

### 格式：输入 / 步骤 / 输出

```markdown
## Examples

### 提取文本

**Input**: "Extract text from report.pdf"

**Steps**:
1. Run: python scripts/extract_text.py report.pdf
2. Return the extracted text to the user

### 填写表单

**Input**: "Fill out form.pdf with name: John, date: 2024-01-15"

**Steps**:
1. Parse the field mappings
2. Run: python scripts/fill_form.py form.pdf --name "John" --date "2024-01-15"
```

### 一正一反对比最有效

```markdown
## 示例

**❌ 错误输出**（散文式，结论埋没）：
（一段长文……）

**✅ 正确输出**（结构化，结论前置）：
**结论**：通过 / 需修复
**关键问题**：file:line — 具体描述
```

> **Claude 模仿示例比遵循规则更可靠。** 要锁住输出格式，**示例是最好方式**。

### 数量与质量

> ⚠️ **一两个干净、典型、风格一致的范例，远胜过几十个杂乱的例子**
> ——后者反而会相互干扰、增加噪音。

### 边缘案例单独列

```markdown
## Edge Cases
- **加密 PDF**：先向用户要密码
- **扫描件**：提示可能需要 OCR
- **大文件**：分块处理避免内存问题
```

---

## 步骤原子性

> **每个步骤必须是可独立执行、可独立验证的原子操作。**

```
❌ 太粗——不可验证，模型不知从何下手
steps:
  - 审查代码
  - 给出反馈

✅ 正确粒度——每步有 input / output / verify
- id: step-1
  action: 解析 diff，提取变更文件列表与行范围
  input: unified diff 字符串
  output: [{file, added_lines, removed_lines}]
  verify: 列表非空；每项含 file 字段

- id: step-2
  action: 逐文件检查函数长度（>50 行标记 WARNING）
  input: step-1 的文件列表 + 原始代码
  output: [{file, line, type: "LONG_FUNCTION", message}]
  verify: 所有标记项都有 line 字段

- id: step-3
  action: 检查安全问题（正则匹配 SQL 拼接、eval()、硬编码密钥）
  input: 变更行文本
  output: [{file, line, type: "SECURITY", severity, message}]
  verify: severity 只能是 ERROR/WARNING/INFO
```

**三要素**：每步都要有 **action（做什么）· input（拿什么）· verify（怎么算对）**。

> `verify` 是关键——**没有验证点的步骤，等于没写**。

---

## 验收清单

> **如果你想让 AI 的表现达到你的要求，最好的方法就是把验收标准写成一个清单放进技能里。**
> **AI 每次做完就对着清单逐条打分；有一条不合格就重跑，直到全部合格才输出。**

```markdown
## Verification
- [ ] 组件能无错渲染
- [ ] Props interface 已导出
- [ ] 测试文件存在且至少有一个测试
- [ ] 无 TypeScript 错误
```

**写法要求**：

- 每项**独立可验证**（能跑命令就跑命令）
- 用**具体阈值**："函数 <50 行" 而不是 "代码简洁"
- **失败要重跑**，不允许带着不合格项交付

---

## 契约字段

部分实现支持在 frontmatter 声明输入/输出契约：

```yaml
---
name: security-scan
description: Scan for vulnerabilities
inputs:
  files:
    description: List of file paths to scan
    type: string
  severity:
    description: Minimum severity level
    type: enum
    options: [low, medium, high]
    default: medium
outputs:
  report:
    description: Scan report in markdown
    type: string
  passed:
    description: Whether scan passed
    type: boolean
---
```

| 属性 | 必填 | 说明 |
|---|---|---|
| `description` | 是 | 字段含义 |
| `type` | 是 | string / number / boolean / enum |
| `options` | enum 时 | 合法取值 |
| `default` | 否 | 默认值 |

> 这是**扩展字段**，不是开放标准的一部分。移植时可能被静默剥离——**不要依赖它做强制校验**。
> 想强制，用脚本。

---

## 确定性 vs 概率性

> **核心口诀：确定性的工作交给脚本，概率性的工作交给大模型。**

| 工作类型 | 交给 | 理由 |
|---|---|---|
| 批量计算、格式化、校验 | **scripts/** | 大模型算得慢、耗 token、**还可能算错** |
| 文字生成、推理、判断 | **模型** | 这是它擅长的 |

**典型反例**：让 AI 核算十几家店每个月的流水、毛利率、增长率
——**明显不合适**。写个脚本。

> 脚本执行**不占上下文**，且结果确定。**双赢。**

---

## 自查

```
□ 是否有 Instructions / Constraints / Verification / Examples 四段？
□ 示例是否是具体的输入→输出对？
□ 示例数量是否克制（1–2 组，风格一致）？
□ 是否有正反对比示例？
□ 每个步骤是否可独立验证（有 verify 点）？
□ 验收清单每项是否独立可验证、有具体阈值？
□ 是否有边缘案例章节？
□ 确定性计算是否都进了 scripts/？
```
