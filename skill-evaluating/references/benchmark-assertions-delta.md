# 断言好坏、delta 判读与 VibeCheck

> 相关：《skill-evaluating》的 `assert-on-environment.md` ·
> `eval-loop-official.md` · `comparator-ab-eval.md` · `skill-test-pyramid-four.md`
> 前置：那些讲"断言打在哪、盲评怎么做"，
> 这份讲⭐⭐⭐ **断言本身的写法与⭐⭐⭐ delta 的判读表**——
> 含⭐⭐⭐ 一个"⭐ 不用猜断言"的发现方法。

---

## 目录

- [1. ⭐⭐⭐ 好断言 vs 坏断言](#1--好断言-vs-坏断言)
- [2. ⭐⭐⭐ 五条规则](#2--五条规则)
- [3. ⭐⭐⭐⭐ VibeCheck：别猜断言](#3--vibecheck别猜断言)
- [4. ⭐⭐⭐ delta 判读表](#4--delta-判读表)
- [5. ⭐⭐ 评委失效的四种症状](#5--评委失效的四种症状)
- [6. ⭐⭐ 已验证的五条模式](#6--已验证的五条模式)

---

## 1. ⭐⭐⭐ 好断言 vs 坏断言

**坏断言（delta 会是 0%）**：

```
❌ "The response is helpful"      → 太模糊，baseline 也过
❌ "The response is correct"      → 不针对技能
❌ "The response describes three phases"
   ⭐⭐⭐ → ⭐⭐⭐⭐ 模型⭐ 本来就知道这个（baseline 必然通过）
```

**好断言（会显示真实 delta）**：

```
✅ "The output does NOT use binary contrast patterns such as 'not X — it's Y'"
   ⭐⭐⭐ → 具体、可测，⭐ baseline 会失败
✅ "The response includes the @context field pointing to nanda.dev namespace"
   ⭐⭐⭐ → ⭐⭐⭐ ⭐ 真正的⭐ 新增知识（模型不可能自己知道）
✅ "Processes are categorized into safety levels rather than a flat list"
   → 技能才教的具体格式
```

**一条通用写法**：

> ⭐⭐⭐⭐ **"Output does NOT contain tricolons"
> ⭐⭐⭐ ⭐ 比 ⭐ "output sounds natural" ⭐ 可靠得多。**

> ⭐⭐⭐⭐ 核心判据：**baseline 会不会也通过？**
> 会 → 这条断言⭐ 测的是模型基线能力，不是技能的贡献。
> ⭐⭐⭐ 这与 `eval-loop-official.md` 的
> "两组都通过的断言没有区分度"是⭐ 同一条的第二个来源，
> ⭐⭐ 但这里给出了⭐⭐⭐ **一个可操作的检验**：**先跑一次 baseline。**

---

## 2. ⭐⭐⭐ 五条规则

```
① ⭐⭐ 具体：测⭐ 精确模式，不是感觉
② ⭐⭐⭐ 二值：评委必须能⭐  unambiguously 回答 yes/no
③ ⭐⭐⭐⭐ ⭐ 瞄准⭐ 技能独有提供的东西——⭐⭐⭐ baseline 也会过的断言毫无价值
④ ⭐⭐⭐ ⭐ 每个 eval ⭐ 3–5 条断言：够测量，⭐ 又不至于噪音累积
⑤ ⭐⭐⭐ 正负混合："does NOT contain X" ⭐ 与 ⭐ "DOES contain Y" ⭐ 都要有
```

> ⭐⭐⭐ 第 ⑤ 条与我们已有的 `eval-case-design.md`
> "负向用例测的是'它没做什么'"完全对上——
> ⭐⭐ 但那里说的是⭐ 用例，这里说的是⭐ 断言：
> **每个用例内部也要有正负两类断言。**

---

## 3. ⭐⭐⭐⭐ VibeCheck：别猜断言

不知道该给一个新技能写什么断言时：

```
① ⭐⭐ 生成 ⭐ 10–20 组⭐ 配对输出（有技能 vs 无技能），用不同 prompt
② ⭐⭐⭐ 让模型⭐ 比较两组，⭐ 提出⭐ 行为差异
③ ⭐⭐⭐ ⭐ 检查哪些差异是⭐ 稳定出现的
④ ⭐⭐⭐ 那些⭐⭐⭐ 稳定的模式 ⭐ 才成为你的⭐ 正式断言
```

> ⭐⭐⭐⭐ **"This prevents guessing at assertions that don't actually differentiate."**
>
> ⭐⭐⭐ 这个方法解决了一个⭐ 很实际的问题：
> 我们已有的 `skill-test-pyramid-four.md` 说
> "先用 CLI 手跑一遍校准预期，再写自动断言"——
> ⭐⭐ 但⭐ 手跑一遍仍然要靠你猜哪些差异重要。
> **VibeCheck 用"稳定出现"这个客观标准替代了你的猜测。**
>
> ⭐⭐⭐ 两者合起来是完整流程：手跑校准 → VibeCheck 找差异 → 写断言 → 跑 baseline 验证区分度。

---

## 4. ⭐⭐⭐ delta 判读表

```
Delta = pass_rate − baseline_pass_rate
```

| Delta | 含义 | ⭐ 该做什么 |
|---|---|---|
| ⭐⭐⭐ >+20% | Strong skill | ⭐ 发布 |
| +1% ~ +20% | Weak signal | 改进 eval 或技能 |
| ⭐⭐⭐⭐ 0% | ⭐ 无效果 | ⭐⭐⭐ **技能是冗余的，⭐⭐⭐ 或 eval 测错了东西** |
| ⭐⭐⭐⭐ Negative | ⭐ 技能有害 | ⭐⭐⭐ 技能让模型困惑，或 eval 本身有问题 |

> ⭐⭐⭐⭐ **"0%"那一格最锋利**：它把"技能没用"拆成了⭐ 两种可能，
> ⭐⭐⭐ 而且⭐ **第二种（eval 测错了）比第一种更常见**——
> 因为写一个 baseline 也会过的断言，太容易了。
>
> ⭐⭐⭐⭐ **"Negative"那一格** 与我们已有的
> `capability-offset-net-gain.md`（59% 抵消）、
> `three-skill-ceiling.md`（挂载 >3 下滑）、
> `skillsbench-vs-realworld.md`（弱模型有技能反而更差）
> ⭐⭐⭐⭐ 是⭐ 第四个独立来源——
> **"技能可能让结果变差"这件事，现在有四个来源从不同角度证实了。**
>
> ⭐⭐ 发布策略只有一条：
> ⭐⭐⭐ **只发布 delta 为正的技能；零或负 → 不发布，回去改。**

**完整指标（含成本）**：

```
pass_rate    mean + stddev
time_seconds mean + stddev
tokens       mean + stddev
delta = { pass_rate, time_seconds, tokens }
```

> ⭐⭐⭐ 一句很到位的解读：
> ⭐⭐⭐⭐ **"13 秒开销换 50 点提升" 与 "token 翻倍换 2 点提升"
> ⭐⭐⭐ ⭐ 是完全不同的权衡。**
>
> ⭐⭐ 这与 `quality-rubric-nine-dims.md` 的 L3 成本层
> （质量分提升 ÷ 增加的 token）是同一思路。

---

## 5. ⭐⭐ 评委失效的四种症状

| 症状 | ⭐ 可能原因 | 修法 |
|---|---|---|
| ⭐⭐⭐ 全部通过 | 断言太模糊 | 更具体、更二值 |
| ⭐⭐⭐ 跨运行不一致 | 评委不确定 | ⭐⭐⭐ 需 `temperature=0`，⭐⭐ 判决前先 CoT |
| ⭐⭐⭐⭐ 技能与 baseline 同分 | ⭐ 测的是模型已有的知识 | ⭐⭐⭐ 重新设计成⭐ **行为抑制测试** |
| ⭐⭐⭐ 技能得分低于 baseline | 技能约束过度 | 检查技能指令是否与 prompt 冲突 |

> ⭐⭐⭐⭐ **第三行的"重新设计成行为抑制测试"是本份最妙的一条**：
> 如果一个技能的作用是"⭐ 让模型不要做某事"（比如不要写 AI 味），
> ⭐⭐⭐ 那么正向断言（"输出要有 X"）必然 baseline 也过——
> ⭐⭐⭐⭐ **必须反过来测"输出⭐ 不含 X"**，才能测出它的贡献。
>
> ⭐⭐⭐ 这与 `eight-practical-lessons.md` 的
> "不要请求用户贴密钥""不允许 push 到 main"这类⭐ 约束型技能
> 直接相关：**约束型技能的 eval 必须写成抑制测试。**

---

## 6. ⭐⭐ 已验证的五条模式

```
✅ ⭐⭐⭐ 行为抑制类技能⭐ 最容易评测（humanize: +53%）
✅ ⭐⭐⭐ 新增知识注入⭐ 若真的新颖则有效（geo-optimizer: +50%）
❌ ⭐⭐⭐ 常识注入 ⭐ delta 为 0（charting / prd-creator / hunter-skeptic-referee）
❌ ⭐⭐⭐ 需要系统访问权限的技能⭐ 无法这样评测（process-cleanup: −5%）
⚠️ ⭐⭐ 长而贵的 prompt ⭐ 费钱但不提升信号（saas-launch-audit）
⭐⭐⭐ ⭐ 2–3 个精心设计的 eval ⭐⭐ 胜过 ⭐ 10 个平庸的
```

> ⭐⭐⭐⭐ **"常识注入 delta 为 0"** 是对
> `knowledge-delta-checklist.md`（该有的是模型不知道的）
> ⭐⭐⭐ 的⭐ 直接实证——**你写常识，delta 就是 0，一个点都涨不了。**
>
> ⭐⭐⭐ **"2–3 个精心设计的 eval 胜过 10 个平庸的"**
> 与我们已有的"3–5 条断言"、少样本"3 个高质量 = 5 个普通"
> ⭐⭐⭐ 是⭐ 同一规律的第三次出现：**质量远重于数量。**

---

## 速查

```
□ ⭐⭐⭐⭐ 核心判据：⭐ baseline 会不会也通过？会 → 这条断言毫无价值
   ⭐⭐⭐ 写法："does NOT contain X" ⭐ 比 "sounds natural" 可靠得多
□ ⭐⭐⭐ 五规则：具体 · ⭐⭐⭐ 二值 · ⭐⭐⭐⭐ 瞄准技能独有 · ⭐⭐⭐ 3–5条 · ⭐⭐⭐ 正负混合
□ ⭐⭐⭐⭐ VibeCheck：10–20 组配对输出 → 模型提差异 → ⭐⭐⭐ 只保留⭐ 稳定出现的
   ⭐⭐⭐ 用"稳定出现"替代你的猜测

□ ⭐⭐⭐ delta：>+20% 发布 · +1~20% 改进 · ⭐⭐⭐ 0% = ⭐ 冗余⭐ 或 ⭐⭐ eval 测错了
   ⭐⭐⭐⭐ 负 = 技能有害（⭐⭐⭐⭐ 第四个独立来源证实"技能可能让结果更差"）
   ⭐⭐⭐ 只发布 delta 为正的
   ⭐⭐⭐ 成本要看 delta{time, tokens}：13秒换50点 ≠ token翻倍换2点

□ ⭐⭐⭐⭐ 评委失效第三行：⭐ 技能与 baseline 同分 → ⭐⭐⭐ 重设为⭐ 行为抑制测试
   ⭐⭐⭐⭐ ⭐ 约束型技能的 eval ⭐ 必须写成"输出不含 X"
□ ⭐⭐⭐ 常识注入 delta 恒为 0（实证）；⭐⭐⭐ 2–3 个好 eval > 10 个平庸
```

**一句话**：

> ⭐⭐⭐⭐ **断言的核心判据是"baseline 会不会也通过"——会就毫无价值，所以约束型技能（教模型别做某事的）必须把 eval 写成"输出不含 X"的抑制测试，否则永远测出 0% delta；
> delta 为负意味着技能有害（这已是第四个独立来源），只发布 delta 为正的技能。**
