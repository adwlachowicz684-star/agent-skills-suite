---
name: skill-execution
description: 技能的执行期行为——输出契约与 Schema-First、前置门禁、进度报告、状态检查、幂等与恢复、错误处理与熔断、无限循环与超时、防绕开（反理性化）、落地验证。用于 agent 跳步、输出形状不稳、中途才来要输入、失败后静默继续、长任务无反馈、声称完成但没做。
  Do NOT use for 从零创建技能的整体流程（用 skill-authoring）、正文措辞与指令形态（用 skill-crafting）、目录与 frontmatter 结构（用 skill-structuring）、脚本本身的写法（用 skill-scripting），也不用于一次性提示词。
---

# 技能的执行期行为

## 边界

- 用于：**输出契约** · 前置门禁 · 进度报告 · 状态检查 · 幂等与恢复 · 错误与熔断 · 防绕开 · 落地验证
- 不用于：整体创建流程 · 正文措辞 · 目录与 frontmatter · 脚本写法 · 一次性提示词

## 核心原则

> ⭐⭐ **技能跑到一半才来问你要东西——或者更糟，默默即兴发挥一条替代路径——而这都发生在你已经走开之后。**

| 失败形态 | ✅ 该用什么 | ❌ 常见错误 |
|---|---|---|
| 缺前置条件 | ⭐ STEP 0 前置门禁 | 边跑边问 / 即兴回退 |
| 输出形状不稳 | ⭐ Schema-First + 四道防线 | 散文描述格式 |
| 长任务无反馈 | 按阶段报 + 降级必须说 | 闷头跑完 |
| 失败后静默继续 | 非 0 退出 + 熔断 | 打 "success" 后继续 |
| 声称完成但没做 | ⭐ 落地验证（建造者不当审计员） | 只检查"它说了正确的话" |

> ⭐⭐ **一个技能可以通过每一条评估查询，却依然自信地从过期表里报出错误数字。**
> 而技能会被调用几百次且每次都不经复核。

## 路由表（按需深读）
| `seven-contracts.md` | ⭐⭐⭐ 七契约：从说明书到责任契约；★别把HTTP 200当成功 |
| `output-contract.md` | ⭐ 输出契约：Schema-First、四道防线 |
| `output-contract-templates.md` | ⭐ 模板钉 assets/、三种目录语义 |
| `output-control.md` | 输出控制三层次与模板 |
| `preflight-gate.md` | ⭐ STEP 0：声明/验证/拦截三条 MUST NOT |
| `progress-reporting.md` | 长任务按阶段报、降级必须说 |
| `state-check.md` | ⭐ 行动前先查状态 |
| `idempotency-resume.md` | ⭐ 幂等、状态文件、恢复与回滚 |
| `error-handling.md` | 失败处理、重试、熔断、降级 |
| `infinite-loop-timeout.md` | ⭐ 无限循环与超时：终止条件、每技能单独 timeout |
| `anti-rationalizations.md` | ⭐ 反理性化：agent 找借口跳过步骤 |
| `grounding-verification.md` | ⭐ 落地与验证：怎么证明"完成了" |

**输出形状**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **Schema-First 与四道防线** | `references/output-contract.md` |
| **模板放哪、目录语义** | `references/output-contract-templates.md` |
| **输出控制三层次** | `references/output-control.md` |

**执行过程**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **开始前收齐前置条件** | `references/preflight-gate.md` |
| **长任务怎么报进度** | `references/progress-reporting.md` |
| ⭐ **行动前先查状态（别重复做）** | `references/state-check.md` |
| ⭐ **失败后能恢复、能回滚** | `references/idempotency-resume.md` |
| **重试/熔断/降级** | `references/error-handling.md` |
| ⭐ **终止条件与超时** | `references/infinite-loop-timeout.md` |
| ⭐ **agent 找借口跳步** | `references/anti-rationalizations.md` |

**收尾**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **怎么证明"完成了"** | `references/grounding-verification.md` |

## Critical Rules

**STEP 0（前置门禁）**：

1. ⭐ **不得在已知缺少前置条件的情况下开始执行**
2. ⭐ **不得中途暂停去要一个 STEP 0 本可收集到的输入**
3. ⭐ **不得即兴发挥未声明的回退路径**
4. ⭐ `Prerequisites: none` 要显式写——缺失该章节是缺陷，不是默认值
5. ⭐ **"运行期间你会问用户什么"也算前置条件**——趁用户还在场一次问完，缺失项一次性全报
6. **前置条件失败 → 快速失败；运行时失败 → 优雅降级**

**输出**：

- ⭐ **Schema-First**：先定结构再写内容，不是写完再描述
- 模板钉进 `assets/`，正文只引用路径
- 输出格式钉死 + 一个填好的示例——**一个示例胜过十句"请注意格式"**

**执行**：

- ⭐ **任何重试或轮询都必须声明最大次数**——见过跑满 200 次烧光 token 的生产事故
- **删除 / push / 部署必须设人工确认门槛**（先输出命令清单，确认后再执行）
- ⭐ **同一工具连续调用 >3 次 = 命令抖动**，这是循环的信号
- ⭐ **绝不臆造进度**——恢复前检查点缺失/过期时，安全停止

**验证**：

- ⭐⭐ **建造者不能当审计员**——派全新只读子代理复核，agent 默认会"幻觉式合规"
- 校验**分必做与按需**——过度验证是最大单一成本源
- 禁用"应该 / 看起来 / 我很有信心"作为通过证据

## 何时不用（边界）

- 从零创建技能的整体流程 → 《skill-authoring》
- 正文措辞、指令形态、示例设计 → 《skill-crafting》
- 目录布局、frontmatter、加载机制 → 《skill-structuring》
- ⭐ 脚本本身的 CLI 契约与退出码 → 《skill-scripting》
- 评估打分与触发测试 → 《skill-evaluating》

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | ⭐ 自举校验：结构、路由表覆盖、孤立文件、行数上限 |

## 参考

- 相关技能：《skill-crafting》（措辞与形态）·《skill-scripting》（脚本契约）·
  《skill-evaluating》（`assert-on-environment.md` 断言打在环境状态上）
