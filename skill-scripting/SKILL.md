---
name: skill-scripting
description: 把技能里的确定性工作做成脚本——脚本该不该抽、CLI 契约、退出码分级、stdout/stderr 分离、纯函数与可重复执行、工具输出设计、脚本依赖管理。用于 agent 每次现想都出错、输出形状不稳、脚本静默失败、结果被调试日志污染、工具描述写不好，也用于脚本 exit 0 却没干活、脚本越写越像第二个技能、换台机器就跑不了、长脚本超时后状态不明。
  Do NOT use for 从零创建技能（用 skill-authoring）、正文措辞与指令形态（用 skill-crafting）、目录与 frontmatter 结构（用 skill-structuring），也不用于一次性命令。
---

# 技能里的脚本

## 边界

- 用于：该不该脚本化 · CLI 契约 · 退出码与错误分级 · 输出设计 · 确定性 · 依赖管理
- 不用于：整体创建流程 · 正文措辞 · 目录与 frontmatter 结构 · 一次性命令

## 核心原则

> ⭐⭐ **模型判断脚本成败靠的是退出码，不是你打了什么字。**
> 失败了还继续往下走、最后打一行 "success" —— 那是在骗模型。

| 判断 | ✅ 做法 | ❌ 常见错误 |
|---|---|---|
| 脚本失败 | 非 0 退出码 + stderr 说明 | 打 "success" 后继续 |
| 结果输出 | 只写 stdout | 结果里混着调试日志 |
| 失败分类 | ⭐ 退出码分级（10/20/30…） | 一律 `exit(1)` |
| 工具输出 | ⭐ 为模型推理设计字段 | 为人类阅读设计 |
| ⭐ 空结果 | ⭐⭐⭐⭐⭐ 带分母 `total/processed` | 只报 `processed: 0` |

> ⭐⭐⭐⭐⭐ **脚本最危险的输出是"成功但没干活"。**
> glob 0 匹配、过滤条件把全部排除、缺依赖后"贴心"降级、前置判断成立就早退——
> 四次都 exit 0，而每一次都意味着脚本没做你以为的那件事。
> → ⭐⭐⭐⭐ **没有分母的成功，等于沉默。**

> ⭐ **能给 agent 的最强工具是代码本身。**
> 模型现想有失败率，脚本没有——跑一万次一个样。
> → ⭐ **能固化成脚本的就别让模型现想。**

## 路由表（按需深读）
| `skill-scripting/references/helper-library-pattern.md` | ⭐⭐⭐⭐ 给 helper 库而非流程；⭐⭐⭐⭐⭐ docstring 是 Gotchas 第二投放点；现场组合 |
| `skill-scripting/references/script-error-messages.md` | ⭐⭐⭐⭐⭐ 四段式错误消息；⭐⭐⭐⭐⭐ 没写'不要推断'模型就会推断；不写密钥 |
| `skill-scripting/references/script-testing.md` | ⭐⭐ golden 文件是变更可见化机制；跑三次测幂等 |
| `skill-scripting/references/script-security-boundary.md` | ⭐⭐ 技能里的安全声明是说明不是锁 |
| `skill-scripting/references/script-cli-contract.md` | ⭐⭐ 退出码分级 + stdout/stderr 分离；绝不设计交互式输入 |
| `skill-scripting/references/deterministic-scripts.md` | ⭐ 纯函数四原则 + ⭐ 跑两次 diff 验证 + 该不该脚本化判据 |
| `skill-scripting/references/scripts-as-production.md` | ⭐ 脚本即生产代码：JSON over stdout 契约 |
| `skill-scripting/references/script-engineering.md` | ⭐ 脚本归位：可重复执行的确定性任务才进 scripts/ |
| `skill-scripting/references/tool-output-design.md` | ⭐⭐ 工具输出是给模型推理的原材料，不是给人看的 |
| `skill-scripting/references/script-silent-success.md` | ⭐⭐⭐⭐⭐ exit 0 但没干活：0 匹配/全过滤/降级/早退；⭐⭐⭐⭐ 输出必须带分母 |
| `skill-scripting/references/script-responsibility-drift.md` | ⭐⭐⭐⭐⭐ 判断进脚本=确定的错误；⭐⭐⭐⭐ 模型绕过脚本重算=确定性被抵消 |
| `skill-scripting/references/script-environment-assumptions.md` | ⭐⭐⭐⭐⭐ cwd 是最贵的假设；换 cwd 跑一次能暴露"存在但是另一个" |
| `skill-scripting/references/script-timeout-and-partial.md` | ⭐⭐⭐⭐⭐ 超时最没信息量；⭐⭐⭐⭐ 半途产物存在但不可用；自超时 exit 30 |

## Critical Rules

1. ⭐⭐ **失败必须诚实**：任何失败路径都要非 0 退出，禁止打印 "success" 后继续
2. ⭐ **stdout 只放结果**，调试与诊断一律走 stderr（否则调试日志被当成结果解析）
3. ⭐ **退出码分级**，让 SKILL.md 的 Error Handling 能精准回退，而不是笼统 `exit(1)`
4. ⭐⭐ **绝不设计交互式输入**——模型会卡死在等待
5. ⭐ **引用自带脚本用 `${CLAUDE_SKILL_DIR}`**，不用相对路径（技能装到别处会失效）
6. ⭐ **确定性验证：跑两次 diff**——任何差异都意味着没达成纯函数保证
7. ⭐ **工具描述写"什么时候该用"**，字段名为推理服务，不是为人阅读
8. ⭐⭐⭐⭐⭐ **脚本不写判断**——业务规则进数据文件或正文；脚本里硬编码的判断会变成"确定的错误"
9. ⭐⭐⭐⭐ **不假设 cwd**，技能资源用 `${CLAUDE_SKILL_DIR}`，项目文件要求显式绝对路径
10. ⭐⭐⭐⭐ **长脚本要有 stderr 进度（带分母）+ 自超时**，超时时输出结构化状态而非被杀

## 何时不用（边界）

- 从零创建技能的整体流程 → 《skill-authoring》
- 正文措辞、指令形态、输出契约 → 《skill-crafting》
- 目录布局、frontmatter、加载机制 → 《skill-structuring》
- 一次性的命令行操作 → 直接执行，不必封装
- ⭐ 需要模型"每次给出新见解"的内容 → 放 `references/` 读进上下文，不是脚本

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | ⭐ 自举校验：结构、路由表覆盖、孤立文件、行数上限 |

## 参考

- 相关技能：《skill-crafting》（措辞与形态）·《skill-structuring》（物理结构）·
  《skill-governance》（脚本安全审计，见 `skill-security/references/pre-install-security-audit.md`）
