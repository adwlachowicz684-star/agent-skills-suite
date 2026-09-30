---
name: skill-input
description: 技能的输入侧契约：输入校验与分诊（残缺/矛盾/超范围）、数据依赖与前置产物声明、假设登记、相对时间必须解析、工具参数名不可猜。当用户给的信息不全、技能拿到错误时段的数据、或要判断"缺的东西该推断还是该问"时使用。
  Do NOT use for 输出格式与长度（用 skill-output）、执行期错误与恢复（用 skill-recovery / skill-execution）、示例与判断依据（用 skill-examples）。
---

# 输入侧契约

## 边界

- 用于：**技能"拿到什么"——校验、依赖、假设、时间解析、参数构造**
- 不用于：输出长什么样 → 《skill-output》
- 不用于：跑砸了怎么办 → 《skill-recovery》
- 不用于：措辞与文体 → 《skill-crafting》

## 核心原则

> ⭐⭐⭐⭐⭐ **依赖缺失是"响的失败"，假设不成立是"静的成功"。**
> ⭐⭐⭐⭐⭐ **时间窗口错了不报错——它有结果、有数字、有趋势，只是都是另一个时段的。**

```
□ ⭐⭐⭐⭐⭐ 被丢弃的需求必须出现在输出里（矛盾输入时模型默认选一个且不告诉你）
□ ⭐⭐⭐⭐⭐ 先判超范围，再判残缺，最后判矛盾
□ ⭐⭐⭐⭐⭐ "需要 Python"不是声明，python: ">=3.11" 才是
□ ⭐⭐⭐⭐⭐ 猜参数名是幻觉高发区，而它会真的发出一次请求
□ ⭐⭐⭐⭐ 只写假定不写"不成立时"，比不写更糟
□ ⭐⭐⭐⭐ 同一任务内同一个问题最多问一次（硬上限 1 次）
```

## 路由表（按需深读）

| `ambiguous-references-in-user-input.md` | ⭐⭐⭐⭐⭐ "也这样"不缺成分只缺指向；⭐⭐⭐⭐⭐ 分诊三类全过而指向不明；⭐⭐⭐⭐⭐ ≥2候选不得自行选 |
| `input-validation-and-triage.md` | ⭐⭐⭐⭐⭐ 残缺/矛盾/超范围；先判超范围 |
| `data-dependency-declaration.md` | ⭐⭐⭐⭐⭐ 数据依赖；前置产物读不到时模型会自己造一份 |
| `assumption-registry.md` | ⭐⭐⭐⭐⭐ 假设≠依赖；静的成功；规模假设只在生产崩 |
| `relative-time-resolution.md` | ⭐⭐⭐⭐⭐ 相对时间必须在执行时解析并写进输出 |
| `inference-vs-asking.md` | ⭐⭐⭐⭐⭐ 缺的该推断还是该问；⭐⭐⭐⭐⭐ 判据是错了能不能被看出来；⭐⭐⭐⭐⭐ L2 推断并标注在首行 |
| `tool-argument-construction.md` | ⭐⭐⭐⭐⭐ "用 X 工具"不是参数说明；200+成功+缺内容最静默 |
| `inference-vs-asking.md` | ⭐⭐⭐⭐⭐ 缺的东西该推断还是该问：按错了的代价分 |

## Critical Rules

- ⭐⭐⭐⭐⭐ 无数据必须写"未获取"，不得用推断值填充
- ⭐⭐⭐⭐⭐ 时间窗口解析结果写进输出首行
- ⭐⭐⭐⭐⭐ 401/403 → 停止并报告，重试上限 0 次（重试不改变权限）
- ⭐⭐⭐⭐⭐ 矛盾输入必须标注"以下两项冲突，本次取了 A"
- ⭐⭐⭐⭐ 假设章节必须同时写"不成立时"的表现
- ⭐⭐⭐⭐ 环境细节不写死，改为运行时探测

## 何时不用（边界）

- ⭐⭐⭐ "输出该多长" → 《skill-output》的 `output-length-budget`
- ⭐⭐⭐ "失败后怎么重试" → 《skill-recovery》的 `retry-budget`
- ⭐⭐⭐ "这句话含不含糊" → 《skill-crafting》的 `vague-word-blacklist`

## 参考

- 相关技能：《skill-output》（另一端）·《skill-execution》（执行期）·
  《skill-recovery》（失败）·《skill-content》（默认动作）·
  《skill-crafting》（措辞）
