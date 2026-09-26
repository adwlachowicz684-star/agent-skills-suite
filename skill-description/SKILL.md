---
name: skill-description
description: 写好 Agent Skill 的 name 与 description，让它在该触发时触发、不该触发时不抢戏。用于写 frontmatter 描述、选触发词与负向排除、诊断"打不出技能"/"乱触发"、按碰撞风险定长度，以及理解激活机制与覆盖优先级。
  Do NOT use for 技能正文的措辞与结构（用 skill-crafting）、目录与 frontmatter 字段规范（用 skill-structuring）、触发效果的量化评测（用 skill-evaluating），也不用于多技能路由仲裁（用 skill-orchestration）。
---

# 描述与触发设计

## 边界

- 用于：**写 name / description** · 选触发词与负向排除 · 诊断不触发与误触发 · 定描述长度 · 理解激活机制
- 不用于：正文措辞 · 目录与字段规范 · 量化评测 · 多技能路由

## 核心原则

**description 是唯一的发现机制。** 写不好它，正文再好也不会被读到。

> ⭐⭐⭐ **触发是纯 LLM 推理，不是关键词匹配**——所以"堆触发词"无效，
> 而"堵住模型自己干的近路"有效。

**三个数字**：

```
基础描述            20% 激活
+ 含 "Use when"    72–90%
⭐⭐⭐ 祈使句 + 否定约束  100%（650 次对照）
```

## 路由表（按需深读，不要一次全读）
| `debug-not-following.md` | ⭐⭐⭐★★★★★ 问Claude何时用此技能→复述描述；★中途失效=截断 |
| `description-tuning-official-loop.md` | ⭐⭐⭐ 官方调优循环：60/40切分·跑3次·5轮·★按测试集选防过拟合 |

| 你要做的事 | 读 |
|---|---|
| ⭐ **frontmatter 全字段与样式** | `references/frontmatter.md` |
| ⭐⭐⭐ **激活率实证：四档数据与矛盾证据** | `references/activation-rate.md` |
| ⭐⭐ **激活机制：LLM 推理而非关键词匹配** | `references/activation-mechanism.md` |
| ⭐⭐ **描述要"稍微强势一点"（官方指引）** | `references/pushy-description.md` |
| ⭐ **祈使句 + 否定约束：100% 激活** | `references/imperative-description.md` |
| ⭐ **四种写法模式与三个致命错误** | `references/description-patterns.md` |
| description 改写实录 30%→90% | `references/description-rewrite-case.md` |
| description 四条规则 | `references/description-four-rules.md` |
| ⭐⭐ **作用域句式、反触发、一技能一动词** | `references/description-scope-shape.md` |
| name 与 description 命名 | `references/naming-description.md` |
| ⭐⭐ **不触发九项排查 + 两个错误说法** | `references/trigger-fix-nine-causes.md` |

## 何时不用（边界）

- 正文措辞、示例、输出契约 → `skill-crafting`
- 目录布局、frontmatter 字段规范与校验 → `skill-structuring`
- 触发率/误触发的量化评测集 → `skill-evaluating`
- 两个技能抢同一意图时的仲裁 → `skill-orchestration`

## Critical Rules / 禁止项清单

1. ⭐⭐⭐ **不在 description 里总结工作流**——模型会照它抄近路，跳过正文
2. ⭐⭐⭐ **不在正文里写 "When to Use"**——那是 description 的活
3. ⭐⭐ **不写纯禁令**——必须带替代方案（`NOT for X → 用 Y 代替`）
4. ⭐⭐ **不用 `keywords` 字段做路由**——模型忽略它
5. ⭐⭐ **不用内部黑话**——用真实用户会打的字
6. ⭐ **不堆触发词**——变体对照显示无提升

## 速查

```
□ ⭐⭐⭐ 触发靠 LLM 推理，keywords 字段被忽略，堆触发词无效
□ ⭐⭐⭐ 描述含 WHAT + WHEN + HOW；风险高时加 NOT + ALSO
□ ⭐⭐⭐ 反触发写 "NOT for X → 用 Y 代替"（带替代方案，不是纯禁令）
□ ⭐⭐⭐ 别在 description 里总结工作流——模型会照它抄近路跳过正文
□ ⭐⭐ 长度由碰撞风险定：40–60 / 60–90 / 90–120 词
□ ⭐⭐ 排查顺序：先查文件层（80%），再查描述
□ ⭐⭐⭐ 覆盖优先级 enterprise > personal > project > bundled（同名时宽的赢）
```
