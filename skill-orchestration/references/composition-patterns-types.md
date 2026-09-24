# 组合的四种依赖类型与三个反模式

> 相关：《skill-orchestration》的 `skill-chaining-composition.md` ·
> `collision-arbitration.md` · 《skill-patterns》的 `solid-for-skills.md`
> 前置：`skill-chaining-composition.md` 讲"叠加加载与交接协议"，
> 这份讲⭐ **依赖关系的类型学 + 组合反模式**。

---

## 目录

- [1. 前提：单个技能做一件事](#1-前提单个技能做一件事)
- [2. ⭐ 四种依赖类型](#2--四种依赖类型)
- [3. ⭐⭐ 三个组合反模式](#3--三个组合反模式)
- [4. ⭐ 四条最佳实践](#4--四条最佳实践)
- [5. ⭐ 状态靠什么传递](#5--状态靠什么传递)

---

## 1. 前提：单个技能做一件事

> ⭐ **一个技能做一件事。真实任务常常需要多个技能。
> 组合就是 Claude 把技能拼起来处理复杂请求的方式。**

---

## 2. ⭐ 四种依赖类型

**① 顺序依赖**（最常见）

```
Skill A → Skill B，A 的输出是 B 的输入
例：clip-aware-embeddings → collage-layout-expert
    [生成嵌入]              [用嵌入做排版]
```

**实现要点**：

```
⭐ 在 description 里引用上游技能：
   "...Requires embeddings from clip-aware-embeddings skill..."
```

**② 并行组合**

```
多个技能同时作用于同一输入的不同方面：
   ┌ color-theory-expert ──────┐
Photo ──┼── photo-composition-critic ─┼── 综合分析
   └ event-detection-expert ───┘
```

> ⭐ 实现上每个技能独立运作，由用户或编排者合并结果。

**③ 层级（元技能）**

```
一个技能编排其他技能：
   design-archivist（meta）
     ├── vibe-matcher
     ├── color-theory-expert
     └── competitive-cartographer
```

**④ 递归**

```
⭐ 技能可以针对子问题调用自身
   "分解成子任务 → 逐个求解 → 合并"
   常见于规划类技能
```

---

## 3. ⭐⭐ 三个组合反模式

**❌ 循环依赖**

```
Wrong: Skill A 依赖 B，B 依赖 A
   skill-coach → skill-documentarian → skill-coach（环！）

Fix: ⭐ 让依赖单向，或抽出共享功能
```

**❌ ⭐ 隐式依赖**（最隐蔽）

```
Wrong: 技能假定另一个技能存在，但没写
   description: "Uses CLIP embeddings for search"
   ⭐ 但没提 clip-aware-embeddings 这个技能

Fix: ⭐ 在 description 或 README 里显式声明依赖
```

**❌ 单体式反组合**

```
Wrong: 一个技能想做所有事
   name: photo-everything-expert
   description: "Handles composition, color, events, layout, embeddings..."

Fix: ⭐ 拆成聚焦的、可组合的技能
```

> ⭐ 第二个最值得警惕：**隐式依赖在单独测试时完全看不出来**，
> 只在"被单独调用"的生产场景暴露——
> 与 `three-failure-modes.md` 的"隐式上下文依赖"是同一类。

---

## 4. ⭐ 四条最佳实践

**① 文档化依赖**

```markdown
## Dependencies
- **Required**: `clip-aware-embeddings` for vector search
- **Optional**: `color-theory-expert` for palette analysis
```

> ⭐ Required / Optional 这个区分很关键——它决定了**缺失时该怎么处理**。

**② 使用一致的数据格式**

```
Embeddings:    float 数组，或 .npy 文件路径
Color palettes: hex 数组，或 LAB 元组
Scores:        ⭐ 0.0–1.0 归一化浮点
```

> ⭐ 分数统一到 0–1 这一条特别实用：**跨技能比较时才有意义**。

**③ ⭐ 缺依赖时优雅降级**

```python
def analyze_with_optional_color():
    try:
        palette = load_palette()          # 依赖 color-theory
    except FileNotFoundError:
        palette = extract_basic_colors(image)   # ⭐ 降级，不是崩掉
```

**④ ⭐ 组合关键词（提升可发现性）**

写在 description 里：

```
"Composes with X, Y, Z"
"Extends X with Y capabilities"
"Downstream of X"
"Input for Y workflows"
```

> ⭐ 这跟 `namespace-collision.md` 的"排除声明互相点名"是同一招，
> 只是方向反过来：**那个说"别找我"，这个说"接在我后面"。**

---

## 5. ⭐ 状态靠什么传递

> ⭐ **状态就是对话历史。不需要特殊的传递机制。**

```
早期技能产生计划 → 后期技能执行它
早期技能发现问题 → 后期技能修复它
早期技能写设计   → 后期技能写代码
```

**设计给组合用的四条**：

```
① ⭐ 单一职责——做多件事的技能组合得很差
   （别的技能无法干净地调用其中一段）
② ⭐ 清晰的输入/输出契约
   哪怕是非正式的："本技能假定计划已经写好"
③ ⭐ 不重复劳动——A 写了测试，B 就不该再写一遍
④ ⭐ 幂等性——重新调用应当是安全的
   （组合涉及回溯"重做这一步"时，幂等性就很重要）
```

**两个推荐的编排顺序**：

```
⭐ 流程类技能在前（brainstorming / planning / debugging）
   实现类技能在后

⭐ 验证类技能在动作之后
   （跑测试、检查构建、代码评审、规格评审）
   ——在宣告成功之前抓住问题
```

**组合变难的四个信号**（可当检查表用）：

```
· 指令冲突（"总是 TDD" vs "这类代码不写测试"）
  → 修法：显式排序，或把各自范围写清
· 技能发现失败（该装的帮助技能没装，组合就断了）
· ⭐ 隐式依赖（B 假定 A 先跑过，单独调用就出意外）
  → 修法：B 的指令里检查所需状态
· 长工作流（很多技能串行，上下文变长）
  → 修法：⭐ 技能尽量"上下文轻"
```

**常见失败模式**（六条，抄下来当检查表）：

```
· ⭐ 技能重叠——Claude 无法决定调哪个
· 隐藏依赖——不按顺序调用就断
· ⭐ 长序列不做上下文清理——组合负担越来越重
· 为单独使用而建的技能——组合不起来
```

---

## 速查

```
四种依赖：
□ 顺序（A 输出 → B 输入，⭐ description 里引用上游）
□ 并行（各自独立，由编排者合并）
□ 层级（元技能编排子技能）
□ 递归（对子问题调用自身）

⭐⭐ 三个反模式：
□ 循环依赖 → 单向化或抽共享
□ ⭐ 隐式依赖 → ⭐ 必须显式声明（单独测试看不出来）
□ 单体技能 → 拆分

四条实践：
□ ⭐ 文档化依赖，区分 Required / Optional
□ 统一数据格式（⭐ 分数统一 0.0–1.0）
□ ⭐ 缺依赖时优雅降级，不崩
□ ⭐ description 写组合关键词（"Downstream of X"）

□ ⭐ 状态 = 对话历史，无需特殊传递机制
□ 单一职责 / 清晰契约 / 不重复劳动 / ⭐ 幂等
□ ⭐ 流程类在前、验证类在动作之后
□ ⭐ 长工作流下技能要"上下文轻"
```

**一句话**：

> ⭐ **隐式依赖单独测试时完全看不出来，
> 只在"被单独调用"的生产场景暴露——所以必须写进 description。**
