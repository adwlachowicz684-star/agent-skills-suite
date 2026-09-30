---
name: skill-judging
description: 判定一次技能运行算不算通过。用于写断言（打在环境状态上还是模型输出上）、设计 LLM-as-Judge、判读 delta 与 VibeCheck、确定"什么必须交给代码/Hook 判"而不是交给模型、做故障注入评测。
  Do NOT use for 组织一次评估与搭评测集（用 skill-evaluating）、触发与加载问题（用 skill-triggering）、质量评分维度与 Rubric（用 skill-quality）、CI 与自动 A/B（用 skill-automation），也不用于从零写技能。
---

# 判定一次运行算不算通过

## 边界

- 用于：**断言怎么打** · **judge 怎么设计** · **确定性边界** · **故障注入** · **delta 判读**
- 不用于：评测集设计 · 触发排查 · 维度打分 · CI 编排
- ⭐ **"测什么、跑几遍、对照谁" → 《skill-evaluating》**
- ⭐ **"打几分、按哪些维度" → 《skill-quality》**

## 核心原则

> ⭐ **一次运行只有两个结果：通过，或者不通过。
> 而"通过"这个结论本身，是整套评估里最容易被伪造的东西。**

```
断言打在哪，决定它能不能被伪造
  打在模型输出上 → ⭐ 模型可以生成"已预订"而什么都没发生
  ⭐⭐⭐⭐⭐ 打在环境状态上 → 查系统里真的有一条预订
```

> ⭐⭐⭐⭐⭐ **能用代码判的，永远不要用模型判。**
> 代码判的结果不因 prompt 变化而变化，模型判的会——
> 于是你改一次技能，判定标准也跟着漂移了一次。

## 路由表（按需深读）

| `skill-judging/references/assert-on-environment.md` | ⭐⭐⭐⭐⭐ 断言打在环境状态而非模型输出；⭐ 三项优质断言特征；确定性→Rubric→稳定性分层 |
| `skill-judging/references/benchmark-assertions-delta.md` | ⭐⭐⭐ 断言好坏与 delta 判读表；⭐⭐⭐ VibeCheck 只保留稳定出现的差异；⭐ 约束型要写抑制测试 |
| `skill-judging/references/deterministic-first.md` | ⭐⭐⭐⭐ 确定性优先：能用代码判的别交给模型；四个地方的同一原则 |
| `skill-judging/references/determinism-boundary.md` | ⭐⭐⭐ 只有 Hook 是确定性的；决策流程第一个"是"就定；两条反模式 |
| `skill-judging/references/judge-design.md` | ⭐⭐⭐ LLM-as-Judge 四要素、三种偏差、校准；⭐ 能不用就不用 |
| `skill-judging/references/fault-injection-eval.md` | ⭐⭐⭐ 先写恢复契约再注入故障；故障矩阵；确定性注入计划 |

**写断言**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **断言打在环境状态上** | `skill-judging/references/assert-on-environment.md` |
| **被判定为"通过"的三种伪造方式** | `skill-output/references/output-kind-three.md` |
| **"0 / 无" 不是答案，是未获取** | `skill-output/references/numbers-in-output.md` |

**必须交给代码判的**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **确定性优先** | `skill-judging/references/deterministic-first.md` |
| ⭐ **什么放 Hook、什么放技能** | `skill-judging/references/determinism-boundary.md` |
| **Hooks 的退出码三档** | `skill-security/references/hooks-skill-cooperation.md` |

**用模型当判官时**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **LLM-as-Judge 设计** | `skill-judging/references/judge-design.md` |
| **评分 Rubric（Accuracy 有否决权）** | `skill-quality/references/quality-rubric.md` |
| **评分必须引用证据，否则分数通胀** | `skill-evaluating/references/eval-roles.md` |

**测失败路径**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **故障注入评测** | `skill-judging/references/fault-injection-eval.md` |
| **替身只替成功响应 = 失败路径没被测** | `skill-evaluating/references/test-doubles-fixtures.md` |
| **失败路径最易漏却线上最常见** | `skill-evaluating/references/eval-set-two-dimensions.md` |

## 强制工作流（MANDATORY）

1. **先问这个判定能不能用代码做**：能 → 写成脚本断言，不要进 judge。
2. **能打在环境上就不打在输出上**：查系统状态，不要读模型说了什么。
3. **写"没做成"的分支**：⭐ **一项检查没做成 ≠ 没发现问题**——unknown 和 pass 必须分开。
4. **给判定一个反例**：⭐ **baseline 会不会也通过？会就毫无价值**。
5. **校准**：judge 的结论抽 10 条人工核一遍，看偏差方向。
6. **判读 delta**：>+20% 发布 · 0% 是冗余或 eval 测错了 · ⭐ **负 = 技能有害**。

## Critical Rules

- ⭐ **"输出说成功了" 和 "世界真的变了" 之间没有任何机制保证一致**——断言必须落在后者
- ⭐ **不会失败的检查不是保守，是无效**——删掉输出它还能执行吗？不能就是自我确认
- ⭐⭐⭐⭐⭐ **判定型产物可以靠"永远猜同一个答案"拿高分**——测试集要均衡，且必须有"无法判定"这一类
- 模型当判官会有三种偏差，其中**偏爱更长/更自信的输出**最常见
- ⭐ **分数是"被测物"和"标尺"的比值**——长期 100% 通过的测试集不是好消息
- 注入的故障必须**可复现、可撤销**，否则测出来的"恢复"无法归因

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "输出里写了已创建，所以通过了" | 查系统里有没有。输出是声明，环境是事实。 |
| "检查项都执行了，没发现问题" | ⭐ 没做成和没问题是两回事，unknown 要单独报。 |
| "用模型打分方便，就别写脚本了" | 判据会随 prompt 漂移，你改技能时标准也变了。 |
| "测试集 100% 通过" | 那是测试集失效的信号，把它改坏一次验证。 |
