---
name: skill-refining
description: 优化、瘦身、拆分、翻译与结构化改造已有 Agent Skills。用于技能太啰嗦 / 有空话 / 太耗 token / 该拆未拆 / 触发不稳要重写 description / 要加多语言 / 要按架构分层重组，或上下文预算超标要裁剪。
  Do NOT use for 从零创建新技能（用 skill-authoring）、评估打分与触发测试（用 skill-evaluating）、打包发布与团队推广（用 skill-distribution），也不用于单纯解释概念。
---

# 优化已有技能

## 边界

- 用于：**瘦身** · **拆分** · **翻译** · **架构重组** · **上下文预算裁剪** · **可发现性改造**
- 不用于：从零创建 · 评估打分 · 打包发布 · 概念解释

## 核心原则

> ⭐ **no-op 测试**：逐句问"删掉这句，agent 行为会变吗？"——**没变就整句删**。

```
□ 空操作句（模型本来就会做的）→ 删
□ 抽象原则（没有动作）→ 换成具体动作
□ ⭐ Gotchas（踩坑记录）→ ⭐ 永远别动
```

> ⭐ **Gotchas 是唯一几乎不可能通过 no-op 测试的部分**——
> 它来自实际踩过的坑，是技能里信号最高的内容。

## 路由表（按需深读）
| `four-pitfalls-practice.md` | ⭐⭐⭐ 四坑：★★描述强实现弱→信任崩坏；过细拆分判据 |
| `memory-layering-and-skills.md` | ⭐⭐⭐ 记忆四层：★技能=程序记忆，不该装事实 |
| `skill-rot-rollback-discipline.md` | ⭐⭐⭐ 自改进是版本控制问题；歧义时默认回滚不是保留 |
| `model-migration-audit.md` | ⭐⭐⭐ 升级模型默认做减法；提示性能跨模型只弱相关 |
| `token-cost-optimization.md` | ⭐⭐⭐ 伪技能陷阱；Token泄漏；模型路由层 |
| `skill-evolution-loop.md` | ⭐⭐ 三档信号 + 周月季节奏 + ⭐ 连续5次无用就删 |
| `self-evolution-three-levels.md` | ⭐⭐⭐ 自进化边界：没反馈信号就是把墙撞得更响 |
| `skill-scope-tiering.md` | ⭐⭐ 触发空壳：不删除只调作用域，单技能省 89% 启动开销 |
| `skill-reducer-study.md` | ⭐⭐ 压缩后质量反升 2.8%；>10K token 技能压缩率达 95.8% |
| `split-signals-five.md` | ⭐ 拆分五信号 + 先缩窄再拆 + 按认知动作拆 |
| `version-changelog-practice.md` | ⭐ 版本与 Changelog：三种记录 + 四个常见错误 |
| `version-strategy.md` | ⭐ 版本号判据：调用方会不会坏（不是改了多少字） |
| `split-three-options.md` | ⭐ 三种拆法 + 别过度拆 + 拆后三件事 |
| `iteration-three-levels.md` | ⭐ 版本三层次 + in-session 修改陷阱 + 重构时机 |
| `weekend-lessons.md` | ⭐ 一个周末的六条经验：三对三错与实测数据 |

**瘦身与预算**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **逐句修剪、五种失败模式** | `references/pruning.md` |
| **上下文预算与瘦身清单** | `references/context-budget.md` |
| ⭐ **上下文剖析：目录税 / 加载 / 按需三笔账** | `references/token-profiling.md` |
| ⭐ **预算硬边界：截断砍哪、5,000 token 存活区** | `references/budget-truncation.md` |
| ⭐ **上下文工程：写 / 选 / 压 / 隔** | `references/context-engineering.md` |
| ⭐ **压缩：先改工具再谈摘要、三层级联、30–40% 预算** | `references/context-compression.md` |
| ⭐ **渐进式披露的算术：三层各花多少、22 倍** | `references/disclosure-math.md` |
| **平台差异：本地 vs 托管、上传方式、单请求 ≤8 个** | `references/platform-differences.md` |
| ⭐ **坏味道目录：30 个可快速识别的信号** | `references/skill-smells.md` |
| ⭐ **重构已有技能：表现 vs 行为、六步流程** | `references/refactor-pass.md` |
| ⭐ **去重：按变化频率分组，不是按内容相似度** | `references/deduplication.md` |
| ⭐ **裁剪前先测量：三笔账、四类常见的误剪** | `references/measure-before-cut.md` |
| **太长了该往哪里拆** | `references/splitting.md` |
| ⭐ **目录形状：五个反模式与 30 天审计节奏** | `references/catalog-shape.md` |

**结构与规模**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **何时拆、Router 模式、三层架构** | `references/architecture-layering.md` |
| **实战反模式与七个坑** | `references/anti-patterns-practice.md` |
| ⭐ **可发现性：用户怎么知道技能存在** | `references/discovery-ux.md` |

**多语言**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **翻译什么、不翻译什么、中文场景** | `references/i18n.md` |

**优化工作流本身**：

| 你要做的事 | 读 |
|---|---|
| **优化流程的六步** | `references/workflow.md` |
| **优化场景的借口反驳表** | `references/anti-rationalizations.md` |
| ⭐ **慢 / 无限循环 / 上下文溢出** | `references/runtime-failures.md` |
| ⭐ **从真实执行中迭代、防过拟合** | `references/refine-with-execution.md` |

## 强制工作流（MANDATORY）

1. **跑基线**：`python scripts/validate_skill.py <路径>` + `estimate_tokens.py`，记录行数与 token。
2. **确认真的加载了**：改完让模型复述技能的流程——对得上才算生效。见 **`skill-evaluating`** 的 `reload-debug.md`。
3. **逐句跑 no-op 测试**（`pruning.md`），删掉空操作句。
4. **判断该拆还是该瘦**：正文 >150 行或路由表无可合并项 → 拆（见 `architecture-layering.md`）。
5. **改完复测**：再次 validate + 对比行数与 token，写进汇报。

## Critical Rules

- ⭐ **Gotchas 永远别修剪**——它们是唯一通过不了 no-op 测试的内容
- 拆分后**每个子技能仍要独立合规**：各自的 name/description/边界/验证章节
- ⭐ **合并路由行会损失可发现性**——只在同类项时合并，不要为了省行数乱并
- 中文场景：**`name` 不翻译（标识符），`description` 必须翻译（路由依据）**
- ⭐ **中文日常表达太丰富**——把所有同事会说的说法都写进 description
- 装太多技能时 **description 会被压缩**，可能把匹配用的关键词削掉
- 改完必须**复测触发**——瘦身很容易顺手删掉触发词

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "多留几句更保险" | 每句都要过 no-op 测试。空操作句白占 token。 |
| "Gotchas 太啰嗦，精简一下" | ❌ Gotchas 是信号最高的部分，永远别动。 |
| "拆开会增加跳转成本" | 不拆分才是真的成本——路由表挤爆后谁也找不到。 |
| "翻译时把 name 也译了" | ❌ name 是标识符，必须与目录名一致且 kebab-case。 |
| "行数超一点没关系" | 150 行是自定上限；超了说明该拆，不是该忍。 |

其余见 `references/anti-rationalizations.md`。

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 优化前后各跑一次对比
python scripts/estimate_tokens.py ./my-skill     # 量化瘦身效果
python scripts/gen_eval_set.py "技能用途一句话"   # 改完重测触发
```
