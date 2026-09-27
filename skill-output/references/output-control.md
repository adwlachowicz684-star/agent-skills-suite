# 输出控制：模板、长度与机器可解析

> 相关：`skill-crafting` 的 `output-contract.md`（Schema-First）·
> `terminology.md` · `skill-domain-eng` 的 `api-doc-generation.md`

---

## 目录

- [1. 三个层次的控制手段](#1-三个层次的控制手段)
- [2. ⭐ system_prompt 是最强的定制工具](#2--system_prompt-是最强的定制工具)
- [3. 输出模板](#3-输出模板)
- [4. 控制响应长度](#4-控制响应长度)
- [5. 结构化思维格式](#5-结构化思维格式)
- [6. ⭐ 机器可解析输出](#6--机器可解析输出)

---

## 1. 三个层次的控制手段

```
提示词内指令      → 立即生效，不用改配置
技能里的模板      → 团队一致，与个人习惯无关
system_prompt     → ⭐ 最强，为技能激活期间的每次响应设定行为上下文
```

---

## 2. ⭐ system_prompt 是最强的定制工具

```yaml
name: api-doc-generator
description: "Generate structured API documentation from code"
system_prompt: |
  You are a technical writer generating API documentation.
  Always output documentation in the following structure:
  1. Endpoint summary (one sentence)
  2. Request format (TypeScript interface)
  3. Response format (TypeScript interface)
  4. Error codes table
  5. Curl example
  Never skip any section.
  Use British English spelling.
  Do not include implementation details or internal field names.
```

> ⭐ **它设定了技能激活期间每次响应的行为上下文，
> 不需要你在每条 prompt 里重复指令。**

---

## 3. 输出模板

在技能里定义响应模板，得到可预测的输出结构：

```markdown
- Endpoint: POST /users/register
- Method / Description
- Request (TypeScript interface)
- Response (TypeScript interface)
- Error Codes (table)
- Example Usage (curl)
```

> ⭐ **把模板定义在技能里 = 团队每个人生成的格式都一样，
> 与个人习惯或 prompt 措辞无关。**

---

## 4. 控制响应长度

Claude 会匹配你请求里隐含的详细程度。用固定模式控制：

| 想要 | 写法 |
|---|---|
| 简要摘要 | "In 2-3 sentences, explain..." |
| 详细解释 | "Explain thoroughly, including edge cases..." |
| 只要代码 | "Provide only the code, no explanation." |
| 带注释的代码 | "Provide the code with inline comments explaining each non-obvious step." |
| 分步指南 | "Write a numbered step-by-step guide for..." |

> ⭐ **团队应统一到一两种模式**，而不是各用各的措辞
> ——这让 PR 里 AI 生成内容的详细程度可预测。

---

## 5. 结构化思维格式

调试或代码审查任务，要求结构化分析能得到一致组织的结果：

```markdown
Issue Summary   [一句话描述问题]
Root Cause      [技术解释为什么会发生]
Solution        [代码修复 + 简要说明]
Prevention      [未来如何避免]
```

> ⭐ **一致的标题便于扫读**，特别适合输出要被贴到
> ticket 或 PR 评论的异步评审流程。

---

## 6. ⭐ 机器可解析输出

自动化流程需要结构化、可被下游提取的输出。

**用一致的分隔符包裹**：

```markdown
Machine-Readable Output Format

OUTPUT_START
TYPE: code-review
VERSION: 1.0
SEVERITY: warning
FILE: src/auth/login.ts
LINE: 47
MESSAGE: Unhandled promise rejection in login flow
SUGGESTION: Wrap the await call in a try/catch block
OUTPUT_END
```

> 一个简单的脚本就能提取这些块，转成
> **JSON、GitHub annotations 或 Jira ticket**。

这与 `four-dimension-eval.md` 的"用 `--output-schema` 约束返回固定 JSON"是同一原则：
**跨版本可比的前提是格式固定。**

---

## 速查

| 目标 | 手段 |
|---|---|
| 全队输出一致 | 技能里的模板 |
| 每次响应都遵循 | ⭐ system_prompt |
| 临时控制 | prompt 里的措辞模式 |
| 要贴到 ticket | 结构化思维格式（固定标题） |
| 要被 CI 消费 | ⭐ 分隔符包裹 + 解析脚本 |
| 控制长短 | 固定措辞模式，团队统一 |
