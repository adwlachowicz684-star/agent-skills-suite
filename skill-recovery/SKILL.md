---
name: skill-recovery
description: 技能执行失败、跑不完、跑重了、跑断了之后的恢复。当需要写错误处理、停止条件、重试预算、幂等与续跑、循环超时检测、跨会话接续、状态检查，或排查"静默失败""错误被改写成功""N 个半成品"时使用。含反合理化清单。
  Do NOT use for 前置门禁与执行契约（用 skill-execution）、输出格式与模板（用 skill-output）、触发不生效（用 skill-triggering）。
---

# 失败、终止与恢复

## 边界

- 用于：**跑失败了 / 跑不完 / 跑重了 / 跑断了**之后怎么办
- 不用于：前置门禁、执行契约、并发 → 《skill-execution》
- 不用于：输出格式与模板 → 《skill-output》
- 不用于：技能没被触发 → 《skill-triggering》

## 核心原则

> ⭐⭐⭐⭐⭐ **失败路径的规格不能是一句话。**
> ⭐⭐⭐⭐⭐ 成功路径有模板、字段、示例、验收；
> 失败路径只有"如果失败就报告错误"——
> 一句话的规格，模型就用一句话的方式去补。

```
□ ⭐⭐⭐⭐⭐ 技能不会因为没数据而停下，它会编一个
□ ⭐⭐⭐⭐⭐ 错误被改写成功 = 完全不可见的失败
□ ⭐⭐⭐⭐⭐ 只定义"怎么开始"的技能，从不暂停
□ ⭐⭐⭐⭐⭐ "再试一次"改变的是运气，不是条件
□ ⭐⭐⭐⭐⭐ 副作用持久，进度不持久
```

## 路由表

| `execution-error-protocol.md` | ⭐⭐⭐⭐⭐ 错误被吞掉：模型把失败改写成成功；`safe_reply` 字段；禁止解释错误 |
| `error-handling.md` | ⭐⭐⭐⭐⭐ 四段式错误消息（含第④段"明确禁止什么"） |
| `exit-conditions-when-to-stop.md` | ⭐⭐⭐⭐⭐ 只定义怎么开始的技能；跑不动被当成"已完成" |
| `budget-caps-no-progress.md` | ⭐⭐⭐⭐⭐ 无进展检测器：动作不同但状态不变 |
| `infinite-loop-timeout.md` | ⭐⭐⭐⭐ 循环与重试上限 |
| `three-crash-scenes.md` | ⭐⭐⭐⭐ 三起翻车现场：脚本输出 3 万字塞爆上下文 |
| `anti-rationalizations.md` | ⭐⭐⭐⭐⭐ 反合理化：模型给"绕开约束"找的理由 |
| `idempotency-resume.md` | ⭐⭐⭐⭐⭐ 幂等三层次；区分"没写入"vs"已写入但回应丢失" |
| `state-check.md` | ⭐⭐⭐⭐ 先查状态再决定跳过还是重做 |
| `cross-session-continuity.md` | ⭐⭐⭐⭐⭐ 重跑常比接续可靠 |

## Critical Rules

- ⭐⭐⭐⭐⭐ 结构化错误必须带 `safe_reply`——不给"该说什么"，它就自己组织语言，而组织语言正是它开始编的时候
- ⭐⭐⭐⭐⭐ 停止条件必须可判定：范围可枚举 + 每单元产出上限 + 明确的"全部处理完"信号
- ⭐⭐⭐⭐⭐ 条件没变的重试是浪费；"再试一次"改变的是运气，不是条件
- ⭐⭐⭐⭐⭐ 幂等在串行里是加分项，**在并行里是准入条件**
- ⭐⭐⭐⭐⭐ 禁止解释错误——解释的内容不在技能返回里，只能来自猜测

## 何时不用（边界）

- ⭐⭐ "能不能开始"（前置检查）→ 《skill-execution》的 `preflight-gate`
- ⭐⭐ "输出长什么样"→ 《skill-output》
- ⭐⭐⭐ "技能根本没被触发"→ 《skill-triggering》

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与路由校验 |
| `scripts/estimate_tokens.py <dir>` | 成本估算 |

## 参考

- 相关技能：《skill-execution》（前置门禁与契约）·《skill-output》（输出）·
  《skill-triggering》（不触发）·《skill-evaluating》（失败象限诊断）
