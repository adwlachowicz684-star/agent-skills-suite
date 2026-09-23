# 官方评估循环：四步与 benchmark 结构

> 相关：《skill-evaluating》的 `test-pyramid.md` ·
> `four-dimension-eval.md` · `graded-rubric.md` · `claude-ab-loop.md`

---

## 目录

- [1. 两个独立的失败轴](#1-两个独立的失败轴)
- [2. 四步循环](#2-四步循环)
- [3. ⭐ benchmark.json 的三组指标](#3--benchmarkjson-的三组指标)
- [4. 断言要具体可观察](#4-断言要具体可观察)
- [5. ⭐ 盲评 A/B](#5--盲评-ab)
- [6. 触发描述优化](#6-触发描述优化)

---

## 1. 两个独立的失败轴

```
① 输出质量  —— 它产出好结果吗？
② ⭐ 触发精度 —— 它在正确的时机激活吗？
```

> ⭐ 这两者**相互独立**，必须分别测。
> **输出质量再好，触发不了等于零。**

---

## 2. 四步循环

### 步骤 1：定义测试用例

`evals/evals.json` 里每条含三部分：

```json
{
  "skill_name": "csv-analyzer",
  "evals": [{
    "id": 1,
    "prompt": "I have a CSV of monthly sales data in data/sales_2025.csv. Find the top 3 months by revenue and make a bar chart.",
    "expected_output": "A bar chart showing the top 3 months by revenue with labeled axes.",
    "files": ["evals/files/sales_2025.csv"]
  }]
}
```

```
⭐ 先只写 2–3 条
⭐ 跑完第一轮之后再补断言
   —— 你往往在看到产出之前无法定义什么是"好"
```

> 这条很有实操价值：**别在没见过产出时硬写验收标准**。

### 步骤 2：并行运行

> ⭐ **每条 eval 派生独立 agent —— 一个带技能，一个不带（或旧版本）。
> 各自在隔离上下文运行，防止相互污染。**

```
csv-analyzer-workspace/
└── iteration-1/
    ├── eval-1/
    │   ├── with_skill/     { outputs/ timing.json grading.json }
    │   └── without_skill/  { outputs/ timing.json grading.json }
    └── benchmark.json
```

### 步骤 3：打分与基准

三种打分方式，按成本从低到高：

```
① 代码检查     —— 确定性属性
② LLM-as-judge —— 细微质量
③ 人工评审     —— 金标准
```

> ⭐ 与 `deterministic-first.md` 一致：**从代码检查起步**。

### 步骤 4：分析并迭代

每个迭代找可执行的模式：

| 模式 | 含义 | 处置 |
|---|---|---|
| ⭐ 两组都通过 | ⭐ **没有区分度** | 删掉或替换这条断言 |
| 两组都失败 | 断言写错或任务不可能 | 下轮前先修 |
| 有技能通过、无技能失败 | ⭐ 技能确实增值 | 搞清为什么，强化它 |
| ⭐ 跨运行方差大 | ⭐ 指令有歧义 | 加示例或收紧指引 |

```
从失败断言和 transcript 修订 SKILL.md
⭐ 要泛化修复，而不是逐个 case 打补丁
下一轮放 iteration-N+1/，然后对比
```

---

## 3. ⭐ benchmark.json 的三组指标

```json
{
  "with_skill":    { "pass_rate": {"mean":0.83,"stddev":0.06},
                     "time_seconds":{"mean":45.0,"stddev":12.0},
                     "tokens":    {"mean":3800,"stddev":400} },
  "without_skill": { "pass_rate": {"mean":0.33,"stddev":0.10} },
  "delta":         { "pass_rate": 0.50, "time_seconds": 13.0, "tokens": 1700 }
}
```

> ⭐ **delta 把技能的成本（时间、token）与收益（通过率）放在一起算。**

```
13 秒开销换 50 个百分点的提升
  vs
token 翻倍换 2 个百分点的提升
—— 这是完全不同的取舍
```

**统计严谨性**：

> ⭐ **LLM 输出是非确定性的。单次运行告诉你"发生过一次"，
> 不是"通常会发生"。**
>
> `runs_per_configuration` 通常设为 **3**。
> **均值 ± 标准差**能捕捉单次通过/失败所掩盖的方差。

---

## 4. 断言要具体可观察

```
✅ "柱状图的坐标轴有标注"
❌ "输出不错"
```

---

## 5. ⭐ 盲评 A/B

> ⭐ **顺序评估会引入锚定偏差——
> 第二个版本是相对于第一个被评判的。**

消除方法：

```
比较器 agent 收到 A、B 两份输出，⭐ 不带标签
按 rubric 逐维打分，选出胜者并给出理由
→ 消除位置偏差与标签偏差
```

然后：**分析器 agent 读 transcript 找出赢家为什么赢**，
产出带优先级和预期影响的改进建议。

适用范围不止于"有 vs 无"：

```
版本之间 · 竞争技能之间 · ⭐ 同一技能跨模型之间
```

---

## 6. 触发描述优化

> ⭐ **输出质量评估只有在技能会触发时才有意义。**

三步：

```
① 生成约 20 条触发查询
   —— 8–10 条该触发（措辞各异：随意、正式、隐含）
   —— ⭐ 8–10 条不该触发（⭐ 共享关键词但意图不同的 near-miss）
② 跑循环：给当前描述打分，建议能同时降低误报与漏报的修改
③ 应用并验证：更新 frontmatter 的 description，重跑
```

> near-miss 那部分与 `activation-rate.md`、
> `trigger-eval-set.md` 的说法完全一致——**负样本必须共享关键词**，
> 否则测不出真本事。

---

## 速查

| 事 | 做法 |
|---|---|
| 起步用例数 | 2–3 条，跑完再补断言 |
| 运行方式 | ⭐ 独立 agent，有/无技能对照 |
| 打分顺序 | ⭐ 代码 → LLM-as-judge → 人工 |
| 运行次数 | ⭐ 3 次，报告均值 ± 标准差 |
| 关键指标 | ⭐ delta（成本 vs 收益） |
| 两组全过 | ⭐ 无区分度，换断言 |
| 版本对比 | ⭐ 盲评 A/B，不带标签 |
| 触发测试 | 20 条，含共享关键词的 near-miss |
