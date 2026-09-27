---
name: skill-content
description: 技能各章节的内容来源与写法——正文该放什么（Gotchas/模板/程序优于声明）、措辞与语气规范、操作卡写法、指令高度校准、验证章节与升级条件怎么写、示例即契约、以及把既有提示词/SOP/专家经验/真实范例沉淀成技能。用于写某个章节时不知道放什么、示例该怎么写、验证条件太空泛、要把一段提示词转成技能。
  Do NOT use for 创建流程与阶段顺序（用 skill-authoring）、加载与 frontmatter 排查（用 skill-loading）、触发词与 description（用 skill-description）、评估打分与触发测试（用 skill-evaluating）。
---

# 技能的章节内容

## 边界

- 用于：**正文该放什么** · 措辞规范 · 验证章节 · 示例 · **素材来源转换**（提示词/SOP/专家经验/范例）
- 不用于：创建流程顺序 · 目录布局 · frontmatter 排查 · description 触发 · 评估打分

## 核心原则

> ⭐ **每个章节都要回答"这段配得上它的 token 成本吗？模型已经知道什么？"**

三个最高信号的内容类型（按价值排序）：

```
1. ⭐⭐⭐⭐⭐ Gotchas      ——只有踩过才知道的反直觉事实
2. ⭐⭐⭐⭐   输出模板      ——一例胜十句描述
3. ⭐⭐⭐    验证/升级条件  ——把废话写成可判定条件
```

> ⭐ **最低信号：概念解释、标准操作教程、以及"看起来相关"的背景。**

## 何时不用本技能

- 想按什么顺序创建 → `skill-authoring` 的 `workflow.md`
- description 与触发词 → `skill-description`
- 交付形态（配方/模板/禁令）→ `skill-crafting` 的 `guidance-forms.md`
- 触发率评测 → `skill-evaluating` 的 `trigger-tuning-loop.md`

## 路由表（按需深读）
| `portability-across-projects.md` | ⭐⭐⭐⭐⭐ 环境耦合会报错/组织耦合不会；⭐⭐⭐⭐⭐ L3 环境细节改为运行时探测；⭐⭐⭐⭐ 升模型要做减法 |
| `default-actions.md` | ⭐⭐⭐⭐⭐ 省略不是留白：默认值表；⭐⭐⭐⭐ 最贵的三处省略；⭐⭐⭐ 主动设默认
| `terminology-table.md` | ⭐⭐⭐⭐⭐ 模型不会做同义消解；⭐⭐⭐⭐⭐ 术语表第三列（不要用的说法）
| `instruction-ordering.md` | ⭐⭐⭐⭐⭐ 五段式骨架（契约/红线/术语/流程/验证）；⭐⭐⭐⭐ 验证不能放最后；目录即黄金位 |
| `gotchas-mining.md` | ⭐⭐⭐⭐⭐ Gotchas 是采集的不是写的；六个矿脉；⭐不可推理性筛子 |
| `anthropic-team-lessons.md` | ⭐⭐⭐⭐⭐ 官方团队七课：不陈述显然·Gotchas 最高信号·避免 railroading·技能自带记忆·helper 库 |
| `skill-anatomy.md` | ⭐⭐⭐⭐ 正文该放什么：Gotchas / 模板 / ⭐ 程序优于声明 |
| `examples-as-contract.md` | ⭐⭐⭐⭐ 示例即契约：改技能时不许动的那些示例 |
| `examples.md` | ⭐⭐⭐ 示例怎么写：含 Rationale 字段与模糊输入档 |
| `validation-escalation.md` | ⭐⭐⭐ 验证与升级：把"检查格式"写成可判定条件 |
| `verification-section.md` | ⭐⭐⭐ 验证章节怎么写（含证据对照表） |
| `operator-card-style.md` | ⭐⭐⭐ 操作卡写法 + Keep/Delete 清单；安装/贡献/隐私章节一律删 |
| `body-writing-rules.md` | ⭐⭐⭐ 正文写作九条：可逐条检查的启发式 |
| `prompt-altitude-three-laws.md` | ⭐⭐★★★ 高度检验法（三种诠释/崩掉）；★三条律含逃生口 |
| `writing-style.md` | ⭐⭐ 措辞、语气、格式规范 |
| `real-examples.md` | ⭐⭐ 真实技能范例拆解 |

**写正文**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 正文该放什么 | `skill-anatomy.md` · `anthropic-team-lessons.md` |
| 措辞与语气 | `writing-style.md` · `body-writing-rules.md` |
| 指令写多具体 | `prompt-altitude-three-laws.md` |
| 排版成操作卡 | `operator-card-style.md` |

**写验证与示例**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 验证章节 | `verification-section.md` · `validation-escalation.md` |
| ⭐ 示例 | `examples.md` · `examples-as-contract.md` |

**从既有素材转**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 提示词 → 技能 | `prompt-to-skill.md` |
| 迁移/重构既有提示词 | `prompt-migration.md` |
| 判断该做成哪一类 | `skill-types.md`（Anthropic 九种类型） |
| 看真实范例 | `real-examples.md` |

## Critical Rules

- ⭐ **不写模型已知道的概念**（PDF、HTTP、JSON 是什么）——零增量
- ⭐ **禁令要带理由**，且写清正面对应物——纯禁令会反噬
- 单行 ≤28 词；禁用"尽量""酌情""合适即可"——对模型等于没有约束
- ⭐ **示例必须含 Rationale**——只给输入输出，模型学到的是格式不是判断
- ⭐ **验证条件要可判定**："检查格式"不是条件，"文件名匹配 `^[a-z-]+$`"才是
- 引用保持一层深度，禁止 A → B → C 链
- ⭐ **删除 / push / 部署必须设人工确认门槛**

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "多解释一下背景更好" | ⭐ 这段"为什么"能改变下一步动作吗？不能就删。 |
| "示例放一两个意思一下" | ⭐ 示例是契约：改技能时不许动的那几个，正是回归锚点。 |
| "验证写'检查输出是否合理'" | 不可判定 = 不存在。 |
| "这个技能相关，肯定有帮助" | ⭐ **"看起来相关"正是主要风险源**。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 自举校验：结构、路由表覆盖、孤立文件、行数上限 |
| `scripts/estimate_tokens.py <dir>` | 估算正文与 references 成本 |

## 参考

- 相关技能：《skill-authoring》（创建流程）·《skill-crafting》（交付形态与反模式）·
  《skill-description》（触发词）·《skill-gallery》（完整样本）
