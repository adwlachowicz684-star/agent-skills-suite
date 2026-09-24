# 祈使句 + 否定约束：650 次测试的结论

> 相关：《skill-description》的 `activation-rate.md`（四档数据）·
> `description-rewrite-case.md` · 《skill-crafting》的 `guidance-forms.md`

---

## 目录

- [1. 实验设计](#1-实验设计)
- [2. 六步演化](#2-六步演化)
- [3. ⭐ 为什么祈使句有效](#3--为什么祈使句有效)
- [4. 模板](#4-模板)
- [5. ⭐ 作用域警告](#5--作用域警告)

---

## 1. 实验设计

真实环境基线激活率约 **50%**——模型常常直接执行任务而不调用技能。

```
650 次自动化测试会话
3 个 description 变体（A/B/C）× 4 种环境条件（C1–C4）
每格重复 3 次（N=3）
统计方法：Fisher 精确检验 + 逻辑回归 + CMH 分层分析
```

自动化命令：

```bash
claude -p "" --max-turns 5 --allowedTools "Skill" --output-format json
```

> 把模型限制为只能用 Skill 工具，确保捕捉到真实的激活行为。

---

## 2. 六步演化

| 步 | 改动 | 结果 |
|---|---|---|
| 1 基线 | 默认推荐描述 | **~50%** |
| 2 加 CLAUDE.md | 仓库根加项目上下文 | **~65%（+15pp）** |
| 3 ⭐ 填 keywords 字段 | — | ⭐ **无可测量变化——模型忽略它做路由** |
| 4 ⭐ Pre-prompt hook | 强制注入 | ⭐ **部分配置下降 30pp**（注入命令与技能意图冲突） |
| 5 变体 A（被动 "Use when…"） | — | **77%** |
| 5 变体 B（扩展触发词） | — | 与 A 相近 |
| 5 ⭐ **变体 C（祈使句）** | — | ⭐ **100%，无需任何 hook** |

### 三个可直接记住的否定结论

```
❌ keywords 字段         —— 模型忽略它做路由
❌ Pre-prompt 强制注入   —— 让被动描述下降最多 30pp
❌ 单纯堆触发词          —— 无提升（变体 B ≈ 变体 A）
```

> ⭐ 唯一有效的环境改动是**加 CLAUDE.md 项目上下文（+15pp）**。

---

## 3. ⭐ 为什么祈使句有效

> ⭐ **正向路由（"ALWAYS invoke"）与否定约束（"Do not directly execute X"）
> 必须同时使用。任一单独使用都无效。**

原因：模型有一条更简单的**直接执行**路径。
只说"该调用我"，它仍可能选简单路径；
两者合起来才给出**清晰的排他指令**。

---

## 4. 模板

```yaml
---
name: <name>
description: >
  <domain> expert. ALWAYS invoke this skill when the user asks about
  <trigger list>. Do not <direct action> directly — use this skill first.
---
```

四个组成部分：

```
① 领域标识
② ⭐ 祈使 "ALWAYS invoke" 子句
③ 全面的触发列表
④ ⭐ 否定约束——堵住模型的兜底路径
```

---

## 5. ⭐ 作用域警告

> ⚠️ **这个句式在 description 里有效，在正文里可能反噬。**

`guidance-forms.md` 的实测：
正文里的"不要做 X"因为**没说该做什么**，反而让输出更差。

```
description 里的否定约束 → 治欠触发（召回）→ 有效
正文里的禁令           → 没给替代方案   → ⭐ 可能有害
```

> **位置决定效果。** 别把这条推广到正文。

---

## 速查

| 想要 | 做法 |
|---|---|
| 提高激活率 | ⭐ 祈使句 + 否定约束，两者都要 |
| 堵住直接执行 | "Do not X directly — use this skill first" |
| 加触发词 | 单独加无效，要配合句式 |
| 用 keywords 字段 | ⭐ 无效，别指望它 |
| 用强制注入 hook | ⭐ 有害，别用 |
| 正文里写禁令 | ⭐ 要同时给替代方案 |
