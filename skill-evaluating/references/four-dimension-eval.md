# 四维评估：能写进 CI 的那四个维度

> 前置：`metrics.md`（八层评估模型）· `eval-tooling.md`（pass@k、基线对比）·
> `test-pyramid.md`（四层金字塔）
> 这份只讲**可直接代码实现的四维框架**——每维给出断言方式和判据。

---

## 目录

- [1. 为什么是四个维度](#1-为什么是四个维度)
- [2. Outcome：该做的事做了吗](#2-outcome该做的事做了吗)
- [3. Process：顺序对吗](#3-process顺序对吗)
- [4. Style：符合规范吗](#4-style符合规范吗)
- [5. Efficiency：有没有绕弯路](#5-efficiency有没有绕弯路)
- [6. ⭐ 先确定性检查，再模型评分](#6--先确定性检查再模型评分)
- [7. 阈值怎么设才不误报](#7-阈值怎么设才不误报)
- [8. 用例分级与规模](#8-用例分级与规模)

---

## 1. 为什么是四个维度

技能的失效是**静悄悄的**——没有报错，只有"结果不对劲"。
四条失效路径，各对应一个维度：

| 失效路径 | 症状 | 维度 |
|---|---|---|
| 工具调用中断 | 文件未生成、关键步骤缺失 | **Outcome** |
| ⭐ 结果对了但过程走歪 | 备份→修改 变成 修改→备份 | **Process** |
| 完成了但不合规 | 风格不一致、格式错 | **Style** |
| 完成但太贵 | 500 token/3 步 变成 2000 token/12 步 | **Efficiency** |

> ⭐ **第二条最值得注意**：最终输出正确，但执行路径有数据丢失风险。
> **只看结果会完全漏掉这类问题。**

---

## 2. Outcome：该做的事做了吗

**原理**：不依赖模型打分，解析运行日志做硬性断言。

```python
expected = ["src/index.ts", "src/types.ts", "README.md"]
created  = [e["path"] for e in events if e.get("type") == "file_write"]
missing  = [f for f in expected if f not in created]
assert not missing, f"Outcome 失败：缺失 {missing}"
```

典型失败：**工具调用了，但脚本中途退出，文件没生成**。

---

## 3. Process：顺序对吗

**原理**：提取 tool_use 序列，验证预期顺序（子序列匹配，不要求连续）。

```python
def is_subsequence(sub, seq):
    it = iter(seq)
    return all(item in it for item in sub)

assert is_subsequence(["backup", "edit_file", "verify"], tool_calls)
```

### ⭐ 命令抖动检测

同一工具**连续调用**超过阈值，几乎总是异常：

```python
from itertools import groupby
for name, grp in groupby(tool_calls):
    if len(list(grp)) > 3:
        print(f"⚠️ 命令抖动：{name} 连续调用 {len(list(grp))} 次")
```

> 这是发现"模型在原地打转"最便宜的手段——
> 不需要模型评委，纯计数。

---

## 4. Style：符合规范吗

**原理**：定义 rubric，让模型做结构化评分。

```json
{
  "code_style": {
    "description": "代码是否符合 ESLint 规范",
    "scale": "1-5",
    "anchors": {"1": "完全不符合", "3": "部分符合", "5": "完全符合"}
  }
}
```

⭐ **关键**：用 `--output-schema` 约束返回固定格式 JSON，
**否则跨版本的分数无法量化对比**。

这与 `judge-design.md` 一致——评分必须机器可读，不能是自然语言。

---

## 5. Efficiency：有没有绕弯路

**原理**：每次运行强制记录 `timing.json`，对比开/关技能的成本收益。

```json
{
  "with_skill":    {"total_tokens": 1200, "duration_ms": 3500, "tool_calls": 5},
  "without_skill": {"total_tokens": 2000, "duration_ms": 6000, "tool_calls": 12}
}
```

```
Token 节省 800 (40.0%)
时间节省 2500ms (41.7%)
```

> ⭐ **必须对比"不开技能"的基线**——
> 这是唯一有意义的问题。见 `regression-baseline.md`。

---

## 6. ⭐ 先确定性检查，再模型评分

顺序不能反：

```
① 确定性检查：预期命令/事件 + 预期产物    → 快速、可解释
② rubric 评分：对质量需求做结构化打分     → 慢、有主观性
```

> 确定性检查回答：**"它做对基础事情了吗？"**
> 但不回答：**"它按你想要的方式做了吗？"**

**保持第一层轻量**，在加入模型评分之前先有快速可解释的基础保障。

> 这与 `test-pyramid.md` 第 1 层"结构 lint 不用 LLM 判"是同一条原则：
> **能用代码判的，绝不交给模型。**

---

## 7. 阈值怎么设才不误报

LLM 评分类指标**天然有波动**。用固定阈值会疯狂误报。

> ⭐ **阈值 = 基线均值 − 3×标准差**，而不是拍一个固定值。

配套要求：

- ⭐ **测试环境必须与线上一致**：模型版本、依赖版本、外部 API 的 mock
  ——否则评估结果没有参考价值。**用 Docker 容器化是好实践**。
- 环境漂移会让整套基线失效，比阈值设置影响大得多。

---

## 8. 用例分级与规模

**规模**：不需要大型基准集。

```
⭐ 10–20 条提示就够，用 CSV 管理即可
```

**四个角度**（与 `trigger-eval-set.md` 一致）：

| 类型 | 测什么 | 数量 |
|---|---|---|
| 显式调用 | 直接点名，验证基础功能 | 5–8 |
| 隐式调用 | 只描述场景不提技能名，测 description 是否够清晰 | 5–8 |
| 上下文调用 | 加业务干扰，测是否仍正确触发 | 若干 |
| ⭐ **负向控制** | ⭐ **明确不该触发的场景，防误触发** | 3–5 |

> ⭐ **负样本是验证 description 是否过宽的唯一手段**。

**分级**（CI 提速）：

```
P0 / P1  →  每次 PR 的 CI 跑
P2       →  夜间或发布前跑全量
```

⭐ **每次手动修复，都应该变成一条新用例**——
只有锁定预期行为，才能规模化评估。

---

## 速查

| 要查什么 | 用哪维 | 手段 |
|---|---|---|
| 文件/产物生成了吗 | Outcome | 代码断言 |
| 步骤顺序对吗 | Process | 子序列匹配 |
| ⭐ 模型在原地打转吗 | Process | ⭐ 同工具连续 >3 次 |
| 输出合规吗 | Style | rubric + 固定 JSON schema |
| 是不是变贵了 | Efficiency | timing.json 对比基线 |
| 会不会误触发 | 负向用例 | 3–5 条 |
| 阈值设多少 | — | ⭐ 基线均值 − 3σ |
