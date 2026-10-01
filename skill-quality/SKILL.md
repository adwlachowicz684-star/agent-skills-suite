---
name: skill-quality
description: 技能的质量标准、评分 rubric 与验收门槛。当需要判断一个技能"够不够好"（打分、分级、准入门槛）、设计评分维度与权重、区分能力问题与偏好问题、或建立团队质量基线时使用。含多维 rubric、分级标准、指标定义与常见评分误区。
  Do NOT use for 跑评测的具体方法（用 skill-evaluating）、诊断某个技能为什么不工作（用 skill-triggering / skill-evaluating 的排错文档）、拆分与瘦身决策（用 skill-refining），也不用于技能内容本身该怎么写（用 skill-crafting）。
---

# 技能质量标准

## 边界

- 用于：**评判一个技能好不好**——打分、分级、定门槛、建基线
- 不用于：跑评测的具体方法 → 《skill-evaluating》
- 不用于：诊断为什么不工作 → 《skill-triggering》《skill-evaluating》
- 不用于：怎么写正文 → 《skill-crafting》

## 核心原则

> ⭐⭐⭐⭐ **评分的目的不是给一个数字，是让"哪里该改"变得可见。**

```
□ ⭐⭐⭐⭐⭐ 一个总分只能用来排序，不能用来改
      → 分维度打分，且维度要对应可行动作
□ ⭐⭐⭐⭐⭐ 每个维度必须能回答"低分意味着要去改什么"
□ ⭐⭐⭐ 权重本身就是方法论声明——看权重就知道团队认为什么重要
```

> ⭐⭐⭐⭐⭐ **知道一套评估"能量什么、不能量什么"，
> 才不会把分数当成真相本身。**

## 路由表

| `skill-quality/references/quality-rubric.md` | ⭐⭐⭐⭐ 基础评分表：维度定义与档位 |
| `skill-quality/references/quality-rubric-nine-dims.md` | ⭐⭐⭐⭐⭐ 九维打分：⭐ **实测表现 23 / 可执行具体性 17 / 失败模式 12 占 52%**；⭐⭐ 量不到什么 |
| `skill-quality/references/graded-rubric.md` | ⭐⭐⭐⭐ 分级 rubric（S/A/B/C）与判据 |
| `skill-quality/references/four-dimension-eval.md` | ⭐⭐⭐⭐ 四维度评估：触发 / 执行 / 输出 / 成本 |
| `skill-quality/references/official-checklist.md` | ⭐⭐⭐ 官方检查清单 |
| `skill-quality/references/metrics.md` | ⭐⭐⭐⭐ 指标定义：⭐⭐⭐⭐ 必须报**净增益**（新增通过 − 回归） |
| `skill-quality/references/capability-vs-preference.md` | ⭐⭐⭐⭐⭐ **能力问题 vs 偏好问题**——⭐ 修法完全不同 |
| `skill-quality/references/skill-lift-eval.md` | ⭐⭐⭐⭐ Lift 度量：⭐⭐⭐⭐ 对无技能基线，不只是对上一版 |
| `skill-quality/references/skill-replaces-not-adds.md` | ⭐⭐⭐⭐⭐ **技能是替换不是叠加**；⭐⭐⭐⭐⭐ 只写模型做不到的；大而全的技能半衰期最短 |
| `skill-quality/references/consistent-wrongness.md` | ⭐⭐⭐⭐⭐ **一致性是正确性的伪装**；稳定地错最难被发现；⭐⭐⭐⭐⭐ 必须有独立外部基准 |

## Critical Rules

- ⭐⭐⭐⭐⭐ **分维度打分，不只看总分**——总分掩盖短板（实测 16.1/23 却总分 68.4 的真实案例）
- ⭐⭐⭐⭐⭐ **只报毛通过率会掩盖"换血"**——必须报回归数
- ⭐⭐⭐⭐⭐ **能力问题（做不到）用示例/规则修；偏好问题（做法不合意）用约束/格式修**
- ⭐⭐⭐⭐ **分数长期 100% 不是一个好消息**——定期把技能改坏一次，测试集不报警说明坏的是测试集
- ⭐⭐⭐⭐ **baseline 会不会也通过？会就说明这条断言毫无价值**
- ⭐⭐⭐⭐⭐ **技能触发后替换的是模型的默认行为**——写"模型做不到"的，别写"模型本来就会"的
- ⭐⭐⭐⭐⭐ **"没人报 bug"不等于健康**——一致性错误恰恰不产生 bug 报告
- ⭐⭐⭐⭐ 权重分配要显式写出来——它是团队方法论的声明
- ⭐⭐⭐ 分级要有"停止条件"，不只写"允许做什么"

## 常见误区

| 误区 | ⭐ 问题 |
|---|---|
| ⭐⭐⭐⭐⭐ 只看总分 | 掩盖短板，且无法指导改动 |
| ⭐⭐⭐⭐⭐ 用正向断言测约束型技能 | baseline 必过，测了个寂寞 |
| ⭐⭐⭐⭐ 分数稳定就放心 | ⭐⭐⭐⭐⭐ **分数是"被测物/标尺"的比值，两者可能一起烂** |
| ⭐⭐⭐ 指标没有后果 | ⭐⭐⭐⭐ 变成"我们知道自己在变差"的记录，不是阻止变差的机制 |
| ⭐⭐⭐ 追求维度多 | ⭐⭐⭐ 维度越多，单维样本越少，噪声越大 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与路由校验 |
| `scripts/estimate_tokens.py <dir>` | 成本基线 |

## 参考

- 相关技能：《skill-evaluating》（怎么跑评测）·《skill-triggering》（不触发排查）·
  《skill-governance》（SLO 与错误预算）·《skill-crafting》（正文写法）
