# 上手手册：一步一步做出来

> ⭐ **先手动，再封装。**
> 不要一上来就写技能——先手动做几次，确认流程和规则没问题，再固化成技能。

## 目录

- [第 0 步：识别值得做的那件事](#第-0-步识别值得做的那件事)
- [第 1 步：建目录](#第-1-步建目录)
- [第 2 步：写 frontmatter](#第-2-步写-frontmatter)
- [第 3 步：写正文](#第-3-步写正文)
- [第 4 步：渐进加复杂层](#第-4-步渐进加复杂层)
- [第 5 步：测触发](#第-5-步测触发)
- [第 6 步：稳定化](#第-6-步稳定化)
- [七个可直接偷的模式](#七个可直接偷的模式)

---

## 第 0 步：识别值得做的那件事

> ⭐ **最好的技能来自"你注意到自己反复在做的事"**：

```
□ 你打了两次以上的同一段提示词
□ 你手动带着 agent 走过多次的多步工作流
□ 你每次都要提供同样的上下文或约束
```

**启动门槛**（一条很实用的判据）：

```
□ ⭐ 过去至少执行过 5 次，未来还会有 10 次以上
□ 输出是结构化的（而不是开放式闲聊）
□ 有明确的质量标准
```

> ⭐ **"先手动做 3–4 遍再封装"**——
> 呼应 `prompt-to-skill.md` 的录屏生成：
> **它捕捉到了你认为理所当然、却从未写下来的判断**。

---

## 第 1 步：建目录

```bash
mkdir -p ~/.claude/skills/my-skill          # 个人（所有项目通用）
mkdir -p .claude/skills/my-skill            # 项目级（跟仓库走）
```

```
□ 目录名 = 技能名，小写连字符（kebab-case）
□ ⭐ 目录里必须有 SKILL.md（文件名全大写，大小写敏感）
```

> ⚠️ 大小写问题只在 Linux CI 上暴露——
> macOS 不敏感，所以本地测得好好的。

---

## 第 2 步：写 frontmatter

```yaml
---
name: changelog-writer
description: Draft a changelog entry from a set of merged PRs or commits.
  Use when the user asks to write a changelog, release notes,
  or a "what changed" summary for a version bump.
---
```

> ⭐ **把大部分精力花在 description 上**——
> **它是模型决定要不要加载时读的唯一内容。**

**写法**（一句话 + 触发条件）：

```
□ 先说它做什么
□ ⭐ 再说什么时候用——列出用户会实际打出的字面说法
□ 具体，不要泛
  ❌ "Helps with code"（匹配不到有用的任务）
  ✅ "Reviews a diff for SQL injection, XSS, and auth bypass"
□ ⭐ 语义匹配，不是关键词匹配——但触发词仍然要写
□ 保持精简
```

**两个常被引用的长度口径**（不一致，按你的目标平台选）：

```
官方文档示例  name ≤64 字符 · description ≤200 字符
工程实践      建议 description 300–500 字符（覆盖更多触发说法）
```

> ⭐ 取舍：**写太短覆盖不了说法，写太长占上下文**。
> 用 `validate_skill.py` 的告警阈值做本地判断，别猜。

**可选字段**：

```yaml
dependencies: python>=3.8, pandas>=1.5.0
version: 1.0.0
author: Jane Doe
allowed-tools: Read, Write, Grep, Glob
```

> ⚠️ `dependencies` 里声明的库在离线环境装不上——
> 呼应 `skill-distribution` 的 `air-gapped.md`：那种场景要 PEP 723 内联 + 传输时捆绑。

---

## 第 3 步：写正文

> ⭐ **像给一位熟练同事做简报那样写。**

```
□ 用祈使句写具体步骤
□ ⭐ 说"做什么"，不要说"为什么"
  ——技能一旦加载，⭐ 每一行都会留在上下文里并持续计费
□ 先纯 Markdown 起步，别一上来就写脚本
□ ⭐ 附一个简短的输入/输出示例，让它知道"成功长什么样"
```

**示例**（这比任何规则都有效）：

```markdown
### Example
Input:  PR #120（加暗色模式）、#121（修登录重定向循环）
Output:
  Added
    Dark mode toggle in settings (#120)
  Fixed
    Login no longer loops on expired sessions (#121)
```

**边界情况要写**（这一步常被漏）：

```markdown
## Special Cases
如果是测试文件 → 只看测试覆盖，不看实现细节
如果是配置文件 → 只查安全问题，跳过代码质量
```

**反模式也要写**：

```markdown
## Avoid
- 代码库已有 linter 时，不要提风格修改建议
- 不要建议重写整个函数
- ⭐ 不要标记明显是有意为之的问题（有注释标注的）
```

---

## 第 4 步：渐进加复杂层

> ⭐ **不要第一天就想做完美版本**，按三层逐步加：

```
v1 指令层    只有一个 SKILL.md，说明怎么用现有工具达成目标
v2 参考层    加 API_REFERENCE.md 或 schema 文件，提供更深上下文
v3 脚本层    加 scripts/ 里的 Python / Shell，自动化复杂逻辑
```

```
□ scripts/ 与 references/ 是第三层文件
□ ⭐ agent 只在指令要求时才加载，不占基础上下文
□ 确定性工作（解析格式、调用 API、校验）才抽成脚本
```

---

## 第 5 步：测触发

> ⭐ **编辑 SKILL.md 后必须重启 agent**——
> 会话中途改文件**没有任何效果**（技能在启动时加载）。

**5+5 测试法**（这是最实用的判据）：

```
□ 5 条"应该触发"的说法 → 期望 5/5 触发
□ 5 条"相似但不该触发"的 → 期望 0/5 触发

判定：
  ⭐ 该触发的少于 4/5  → description 太窄
  ⭐ 不该触发的超过 1/5 → description 太宽
```

```
✅ 应该触发（代码审查技能为例）
   "Review my latest changes" · "Check this code for bugs"
   "Do a code review on the auth module"
   "Look for security issues in this PR" · "Review the code I just wrote"

❌ 不应该触发
   "Write a new function to parse JSON"
   "Help me with my Docker configuration"
   "Explain what this regex does"
   "Create a README for this project" · "Fix the bug on line 45"
```

> ⭐ **"不触发"是绝大多数技能问题的根因**——
> 调不出来时先改 description，别改正文。

**输出质量测试**（比"能不能跑"重要）：

```
□ ⭐ 在真实项目上测，不要用玩具示例
□ 输出是否遵循了技能里的指令？
□ ⭐ 是否真的比"不开技能"更好？（这是唯一有意义的问题）
□ 是否符合目标项目的既有约定？
□ 有事实错误或幻觉模式吗？
```

**边界测试**：

```
□ 空文件 / 空项目
□ 超大文件（1000+ 行）
□ 多语言混合项目
□ 非标准目录结构
□ ⭐ 不要求完美处理，但绝不能崩或产出明显错误
```

---

## 第 6 步：稳定化

```
□ 加版本头（v1.0 — 日期 — 说明）
□ 加参数文档
□ 加常见失败的错误处理
□ ⭐ 用不同输入再测一轮
□ 跨 agent 兼容测试（若声明支持多个）
```

**迭代时最常见的四类问题**：

| 症状 | 修法 |
|---|---|
| 太啰嗦 | 加约束："输出控制在 200 字内" |
| 缺上下文 | 补指令或 `@` 引用外部文件 |
| 格式不对 | 明确指定输出结构 |
| 不处理边界 | 补错误处理章节 |

---

## 交互微模式

> 七个可直接偷的交互模式（标志解析 / 分阶段执行 / 深度校准 /
> 批评者姿态 / 输出模板 / 迭代闸门 / 默认动作）见 `patterns.md`。

## 自查

```
□ 是否先手动做过几遍再封装？
□ 过去执行过 5 次以上、未来还有 10 次以上吗？
□ 目录名是否 kebab-case 且 = name？
□ ⭐ description 是否列出了用户会打出的字面说法？
□ 是否覆盖了"边界情况"与"Avoid"两节？
□ 是否给了输入/输出示例？
□ ⭐ 是否按 v1→v2→v3 渐进（而非一次做满）？
□ 长内容是否已拆到 references/？
□ ⭐ 是否跑过 5+5 触发测试？
□ 是否在真实项目（非玩具）上测过输出质量？
□ 是否对比过"不开技能"的基线？
□ 是否测了边界（空/超大/多语言/非标准结构）？
□ 是否有版本头与参数文档？
□ 是否用了七个可偷模式中的若干？
□ ⭐ 是否有错误处理与显式输出格式？
□ 无参数时是否仍有有用行为？
```
