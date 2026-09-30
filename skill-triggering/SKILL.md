---
name: skill-triggering
description: 技能的触发与加载诊断——技能不触发、乱触发、改了不生效、加载失败、命中率低、被更强的竞争者抢走、优先级被覆盖。用于排查"为什么这个技能没有被调用"以及"为什么调用了它而不是我想要的那个"，含四层定位法、误触发与漏触发的相反修法、触发评测集设计、优先级覆盖层。
  Do NOT use for 触发之后的评测打分与质量评分（用 skill-evaluating）、description 的写法与触发词设计（用 skill-description）、frontmatter 字段与加载机制（用 skill-loading），也不用于写一次性提示词。
---

# 触发与加载诊断

## 边界

- 用于：**不触发** · **乱触发** · **改了不生效** · **加载失败** · 命中率诊断 · 优先级覆盖
- 不用于：触发后的质量评分 · description 写法 · frontmatter 字段 · 一次性提示词

## 核心原则

> ⭐ **触发问题是分层的。先确认它在哪一层，再动手。**

```
① 文件层（~80%）  目录/文件名/YAML/name 不匹配
② 触发层（~15%）  description 与用户实际用词不匹配、被竞争者抢走
③ 加载层（~5%）   未被读取、被压缩挤出
④ 行为层          触发了但做错（→ skill-evaluating）
```

> ⭐⭐⭐ **80% 的问题在第 ① 层。先花 2 分钟查文件名/目录/YAML，
> 比直接改 description 收益高 5 倍——而多数人恰恰一上来就改 description。**

## 何时不用本技能

- 已经触发了，只是输出不好 → `skill-evaluating`
- description 该怎么写 → `skill-description`
- frontmatter 字段含义 → `skill-loading` 的 `skill-loading/references/frontmatter-full-reference.md`

## 路由表（按需深读）
| `skill-triggering/references/troubleshooting-order-five-cases.md` | ⭐⭐⭐⭐ 五步排错顺序；五类用例；⭐ 别一上来补正文 |
| `skill-triggering/references/hit-rate-four-questions.md` | ⭐⭐⭐⭐ 四类问题诊断；⭐⭐⭐ 纪律约束型最容易被理性化绕过 |
| `skill-triggering/references/trigger-tuning-loop.md` | ⭐⭐⭐ 误触发 vs 漏触发修法相反；生成的查询首先是诊断 |
| `skill-triggering/references/trigger-eval-set.md` | ⭐⭐⭐ 触发 Eval 集：⭐ near-miss 负例是承重的一半 |
| `skill-triggering/references/priority-override-layers.md` | ⭐⭐⭐ 临时 Prompt > 技能 > 全局 Rule；用非作者措辞测试 |
| `skill-triggering/references/description-by-collision-risk.md` | ⭐⭐⭐ 按碰撞风险分级 + 混淆伙伴审计 |
| `skill-triggering/references/troubleshooting-manual.md` | ⭐⭐⭐ 四层定位法 + 症状诊断表 |
| `skill-triggering/references/reload-debug.md` | ⭐⭐⭐ 改了不生效：⭐ 先 `/reload-skills`，不是重启 |
| `skill-triggering/references/trigger-debugging.md` | ⭐⭐ 触发不稳：欠触发 / 过触发 / 冲突 |
| `skill-triggering/references/triggering.md` | ⭐⭐ 触发机制基础 |
| `skill-triggering/references/discovery.md` | ⭐⭐ 发现性测试 |
| `skill-triggering/references/incremental-debug-procedure.md` | ⭐ 最小配置起步、增量验证、diff 测试 |

**按症状查**：

| 症状 | 读 |
|---|---|
| ⭐ **改了不生效 / 技能不加载** | `skill-triggering/references/reload-debug.md` |
| **四层定位 / 症状诊断表** | `skill-triggering/references/troubleshooting-manual.md` |
| **触发不稳：欠触发 / 过触发 / 冲突** | `skill-triggering/references/triggering.md` · `skill-triggering/references/trigger-debugging.md` |
| ⭐ **命中率低，不知是哪种病** | `skill-triggering/references/hit-rate-four-questions.md` |
| ⭐ **改 description 越改越差** | `skill-triggering/references/troubleshooting-order-five-cases.md` |
| **被别的技能抢走** | `skill-triggering/references/description-by-collision-risk.md` · `skill-triggering/references/priority-override-layers.md` |

**建触发测试集**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **near-miss 负例** | `skill-triggering/references/trigger-eval-set.md` |
| 调优循环 | `skill-triggering/references/trigger-tuning-loop.md` |
| 发现性测试 | `skill-triggering/references/discovery.md` |

## Critical Rules

- ⭐ **改了不生效，先 `/reload-skills`，不是重启**——重启只在"顶层 skills 目录是会话中新建"时才必要
- ⭐⭐ **误触发和漏触发修法相反**：误触发加反触发并点名排除；漏触发补同义说法
- ⭐⭐⭐ **"手动测试用自己的措辞"是最大的测试错误**——请同事用他的原话测
- ⭐ **触发问题优先查文件层**（80%），不是 description
- ⭐⭐ **生成的查询首先是诊断**——"应该触发"那批里出现不对的，是 description 太宽的信号
- ⭐ 超过 10 个技能，误触发就从边缘情况变成主要维护负担
- 负例优先级**高于**正例——不该触发时能不触发更难也更重要

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "加载失败我改了三遍了" | ⭐ 先 `/reload-skills`，再查文件层。改三遍说明你在猜。 |
| "我用自己写的措辞测过，能触发" | ⭐ 那是作者的词汇不是用户的。 |
| "技能不触发，肯定是描述写得不好" | ⭐ 80% 是文件层问题。先查文件名/目录/YAML。 |
| "多加几个触发词更保险" | 触发词堆砌会扩大误触发，先分清是误触发还是漏触发。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 第 ① 层：结构 lint（文件名、YAML、路由覆盖） |
| `scripts/gen_eval_set.py "用途一句话"` | 生成触发测试集（正/负例） |

## 参考

- 相关技能：《skill-evaluating》（触发后的评测）·《skill-description》（写法）·
  《skill-loading》（加载机制与 frontmatter）
