# skill-creator：一个元技能的完整架构

> 相关：《skill-authoring》的 `skill-authoring/references/forty-skills-lessons.md` ·
> 《skill-automation》的 `skill-automation/references/comparator-ab-eval.md` · `skill-evaluating/references/skill-test-pyramid-four.md` ·
> 《skill-examples》的 `skill-examples/references/examples-three-branches.md`
> 前置：那些讲⭐ 该怎么做，
> 这份讲⭐⭐⭐⭐⭐ ⭐ 一个⭐ 真正⭐ 把⭐ 这些⭐ 全部⭐ 实现了的⭐ 元技能⭐ 长什么样——
> ⭐⭐⭐⭐⭐ ⭐⭐⭐ 以及⭐ 它⭐ 有三处⭐ 设计⭐ 与我们⭐ 已有结论⭐ 精确对上。

---

> 下篇：见 `skill-gallery/references/skill-creator-agents-and-stats.md`

## 目录
- [1. ⭐⭐⭐⭐ 定位：把 ad-hoc 变成工程流程](#1--定位把-ad-hoc-变成工程流程)
- [2. ⭐⭐⭐⭐ 目录结构全景](#2--目录结构全景)
- [3. ⭐⭐⭐⭐⭐ 核心循环：一次跑两个子代理](#3--核心循环一次跑两个子代理)
- [4. ⭐⭐⭐⭐⭐ 断言必须带证据](#4--断言必须带证据)

## 1. ⭐⭐⭐⭐ 定位：把 ad-hoc 变成工程流程

> ⭐⭐⭐⭐ **"⭐ 核心价值：⭐⭐⭐⭐⭐ ⭐ 把
> ⭐ '写 prompt → 测试 → 评估 → 迭代'
> ⭐⭐⭐⭐ ⭐⭐⭐ 这个⭐ ad-hoc 过程⭐ 标准化为⭐ 可重复的⭐ 工程流程。"**

```
五项能力：
⭐⭐⭐⭐ Create     —— ⭐ 访谈式引导编写技能（最佳实践内建）
⭐⭐⭐⭐⭐ Eval      —— ⭐ 并行执行测试 + 量化打分 + 交互式评审
⭐⭐⭐⭐ Improve    —— ⭐ 反馈驱动的迭代循环，带前后对比
⭐⭐⭐⭐⭐ Benchmark —— ⭐ 跨配置的统计分析（mean / stddev / delta）
⭐⭐⭐⭐⭐ Optimize  —— ⭐ description 触发优化，带 train/test 切分
```

> ⭐⭐⭐⭐ 这⭐ 五项⭐ 合起来⭐ 正好⭐ 覆盖⭐ 了我们⭐ 这套库⭐ 的⭐ 大部分⭐ 技能划分：
> ```
> Create    → skill-authoring / skill-crafting
> Eval      → skill-evaluating
> Improve   → skill-refining
> Optimize  → skill-description
> Benchmark → skill-evaluating（统计纪律那部分）
> ```
> ⭐⭐⭐⭐⭐ ⭐⭐⭐ 换⭐ 句话说：⭐⭐⭐⭐⭐ ⭐⭐⭐ 我们⭐ 用⭐ 十几个⭐ 技能⭐ 覆盖的⭐ 东西，
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 它⭐ 用⭐ 一个⭐ 技能⭐ 覆盖。⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐ **这是⭐ "⭐ 元技能"⭐ 与
> ⭐ "⭐ 技能库"⭐ 的⭐ 两种⭐ 组织⭐ 形态**——⭐⭐⭐⭐⭐ ⭐⭐⭐ 前者⭐ 是⭐ 一个工具，
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 后者⭐ 是⭐ 一套⭐ 参考资料。⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ **而⭐ 我们⭐ 这套
> ⭐ 恰恰⭐ 是⭐ 后者。**

---

## 2. ⭐⭐⭐⭐ 目录结构全景

```
skill-creator/
├── SKILL.md                 ⭐ 核心指令（约 500 行）
├── agents/                  ⭐⭐⭐⭐⭐ 子代理指令（注意：不在 references/ 里）
│   ├── grader.md            ⭐ 对断言逐条打分
│   ├── comparator.md        ⭐ 盲比 A/B
│   └── analyzer.md          ⭐ 事后分析为什么某版本更优
├── scripts/                 ⭐ Python 工具链
│   ├── quick_validate.py    ⭐ 结构校验
│   ├── run_eval.py          ⭐ 触发测试
│   ├── run_loop.py          ⭐ 优化循环（eval → improve → 重复）
│   ├── improve_description.py
│   ├── aggregate_benchmark.py
│   ├── generate_report.py
│   ├── package_skill.py
│   └── utils.py
├── eval-viewer/             ⭐⭐⭐⭐ 可视化评审界面
│   ├── generate_review.py
│   └── viewer.html
├── references/
│   └── schemas.md           ⭐ JSON Schema
└── assets/
    └── eval_review.html     ⭐ 评审模板
```

> ⭐⭐⭐⭐⭐ 两个⭐ 结构⭐ 决策⭐ 值得⭐ 单独⭐ 拎出来：
>
> **① ⭐⭐⭐⭐⭐ `agents/` 是一个独立于 `references/` 的目录**
> ```
> references/ → ⭐ 被模型"读"的知识
> ⭐⭐⭐⭐⭐ ⭐⭐⭐ agents/    → ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 被模型"变成"的角色（子代理提示词）
> ```
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 这个⭐ 区分⭐ 很干净：⭐⭐⭐⭐⭐ ⭐⭐⭐ 一个⭐ 是⭐ 资料，
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 一个⭐ 是⭐ 人格。⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 而我们
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 此前⭐ 记的⭐ `skill-patterns/references/five-design-patterns.md` 里的
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ "⭐ Reviewer 模式"⭐ 在⭐ 这里⭐ 有了⭐ 物理⭐ 落点。
>
> **② ⭐⭐⭐⭐ `eval-viewer/` 与 `assets/eval_review.html`**
> ⭐⭐⭐⭐⭐ ⭐⭐⭐ 它⭐ 把⭐ "⭐ 让人看结果"⭐ 也⭐ 做成了⭐ 产物，
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐ 而不只是⭐ 在终端里⭐ 打⭐ 一行 pass_rate。
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ **这⭐ 与⭐ 我们⭐ 那条⭐ "⭐ 先摆测试结果⭐ 给人看，
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 再改技能"⭐ 是⭐ 同一个⭐ 判断——
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 而且⭐ 它⭐ 进一步⭐ 意识到：
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐⭐ **光说"要看"不够，⭐⭐⭐⭐⭐ ⭐⭐⭐ 得把"怎么看"也做出来。**

---

## 3. ⭐⭐⭐⭐⭐ 核心循环：一次跑两个子代理

```
Draft Skill → Write Test Cases → ⭐ Spawn Parallel Runs → Grade
   → Review → Improve → ⭐ Repeat
```

> ⭐⭐⭐⭐⭐ **"⭐ 对每个⭐ 测试用例，⭐⭐⭐⭐⭐ ⭐⭐⭐ 同时⭐ 启动 ⭐ 两个 ⭐ 子代理：
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐⭐ `with-skill run` —— ⭐⭐⭐⭐⭐ ⭐⭐⭐ 带着技能执行任务
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ `baseline run`  —— ⭐⭐⭐⭐⭐ ⭐⭐⭐ 同一任务，⭐⭐⭐⭐⭐ ⭐⭐⭐ 不带技能（或用旧版本）"**

```
⭐⭐⭐⭐⭐ 关键：⭐⭐⭐⭐⭐ ⭐⭐⭐ 不是"跑一次技能、人工判断好不好"
⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐ 而是 ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ **每一次都是一对：有技能 vs 无技能**
```

> ⭐⭐⭐⭐⭐⭐ **这是⭐ 我们⭐ 已有⭐ 结论的⭐ 一次⭐ 精确⭐ 实现。**
> ⭐⭐⭐⭐⭐ ⭐⭐⭐ 我们⭐ 记过⭐ 两条：
> ```
> ① ⭐⭐⭐⭐⭐ "baseline 会不会也通过？⭐⭐⭐⭐⭐ ⭐⭐⭐ 会就毫无价值"（benchmark-assertions-delta）
> ② ⭐⭐⭐⭐⭐ "blind A/B comparison（盲评）"（comparator-ab-eval）
> ```
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 而⭐ 这里⭐ 给出的是⭐ **怎么同时满足这两条**——
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 不是⭐ 先跑技能、⭐⭐⭐⭐⭐ ⭐⭐⭐ 再回头补一个 baseline，
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐ **而是⭐ 结构上⭐ 就让⭐ 它们⭐ 成对出现：
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 每个⭐ 用例⭐ 天然⭐ 产生⭐ 一对⭐ 对比样本。**
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 这⭐ 比⭐ "记得去做 A/B"⭐ 可靠得多——
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐⭐ ⭐⭐⭐ **它⭐ 是⭐ 流程的⭐ 默认形状。**

---

## 4. ⭐⭐⭐⭐⭐ 断言必须带证据

```json
{ "expectations": [
    { "text": "Output includes a summary section",
      "passed": true,
      "evidence": "Found '## Summary' header at line 3 with 4 bullet points" } ],
  "summary": { "passed": 5, "failed": 1, "total": 6, "pass_rate": 0.83 } }
```

```
⭐⭐⭐⭐⭐ 两条硬规则：
   ① ⭐⭐⭐⭐⭐ 断言是 ⭐ binary pass/fail（不是 1–5 分）
   ② ⭐⭐⭐⭐⭐⭐ ⭐ evidence is required（必须引用证据）
```

> ⭐⭐⭐⭐⭐ 第 ② 条⭐ 与⭐ 我们⭐ 已有的⭐ 一条⭐ 完全同一：
> ⭐⭐⭐⭐⭐ **"⭐ PASS 必须有 concrete 证据，⭐⭐⭐⭐⭐ ⭐⭐⭐ 不'疑罪从无'"**
> （`skill-evaluating/references/assert-on-environment.md`）。
> ⭐⭐⭐⭐⭐ ⭐⭐⭐ 而⭐ 这里⭐ 把⭐ 它⭐ 做成了⭐ **数据结构里的⭐ 必填字段**——
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 有 `passed` 就必须有 `evidence`，⭐⭐⭐⭐⭐ ⭐⭐⭐ 否则⭐ schema 不合规。
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 这⭐ 又是⭐ 一次⭐ "⭐ 书面规则⭐ 升级为⭐ 代码"⭐ 的实例。
>
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 第 ① 条⭐ 也⭐ 值得⭐ 记：⭐⭐⭐⭐⭐ ⭐⭐⭐ **binary 而非打分**。
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 理由⭐ 是⭐ 可判定的：⭐⭐⭐⭐⭐ ⭐⭐⭐ 打分需要⭐ 一个
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ "⭐ 什么是 3 分"⭐ 的⭐ 标准，⭐⭐⭐⭐⭐ ⭐⭐⭐ 而⭐ 那个标准⭐ 本身
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐ 又需要⭐ 主观⭐ 判断——⭐⭐⭐⭐⭐ ⭐⭐⭐ 于是⭐ 循环回去了。
> ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐ 这⭐ 与 `skill-evaluating/references/assert-on-environment.md` 的
> "⭐ 断言打在⭐ 环境状态上⭐ 而非⭐ 文字上"⭐ 是⭐ 同一族：⭐⭐⭐⭐⭐ ⭐⭐⭐ **都⭐ 在⭐ 消除
> ⭐ "看起来对"⭐ 与 ⭐ "真的对"⭐ 之间的⭐ 模糊地带。**

---

---

## 速查

```
□ ⭐⭐⭐⭐ 定位：把"写 prompt→测试→评估→迭代"从 ad-hoc 变成可重复工程流程
   ⭐⭐⭐⭐⭐ 五项：Create / Eval / Improve / Benchmark / Optimize
   ⭐⭐⭐⭐⭐ 它是"一个工具"，我们这套是"一套资料"——两种组织形态
□ ⭐⭐⭐⭐ 目录：SKILL.md + ⭐⭐⭐⭐⭐ agents/（grader·comparator·analyzer）+ scripts/ + eval-viewer/
   ⭐⭐⭐⭐⭐ agents/ 独立于 references/：references=被读的知识，agents=被变成的角色
   ⭐⭐⭐⭐ eval-viewer/ 把"让人看结果"也做成产物——光说"要看"不够，得把"怎么看"也做出来
□ ⭐⭐⭐⭐⭐ 核心循环：每个用例同时跑两个子代理（with-skill + baseline）
   ⭐⭐⭐⭐⭐⭐ 关键在"结构上成对"而非"记得去做 A/B"——它是流程的默认形状
□ ⭐⭐⭐⭐⭐ 断言：binary pass/fail + ⭐⭐⭐⭐⭐⭐ evidence 必填
   ⭐⭐⭐⭐⭐ binary 而非打分："什么是3分"的标准本身又要主观判断，循环回去了
```
