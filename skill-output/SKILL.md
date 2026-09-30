---
name: skill-output
description: 技能的输出契约与产物设计。当需要定义技能"交付什么"（输出格式、字段、模板、长度与稳定性、结构化输出的语义校验、进度汇报、有据可查验证）时使用。含输出契约模板、快照测试、结构化流水线与常见输出缺陷。
  Do NOT use for 执行过程本身的控制（用 skill-execution）、正文措辞与示例写法（用 skill-crafting）、脚本的 stdout/stderr 约定（用 skill-scripting），也不用于评估输出质量（用 skill-quality）。
---

# 技能的输出契约

## 边界

- 用于：**技能交付什么**——格式、字段、模板、稳定性、可解析性
- 不用于：执行过程控制（重试、停止、并发）→ 《skill-execution》
- 不用于：正文怎么写 → 《skill-crafting》
- 不用于：脚本的 stdout/stderr → 《skill-scripting》
- 不用于：输出质量打分 → 《skill-quality》

## 核心原则

> ⭐⭐⭐⭐ **技能的价值在出口，不在入口。**
> 夸奖一个 agent 的入口能力之前，先把出口能力做扎实。

```
□ ⭐⭐⭐⭐⭐ 能被解析比看起来好看重要
     "输出一个 JSON"不是契约，schema 才是
□ ⭐⭐⭐⭐ 输出是所有下游（人、脚本、其他技能）的唯一接口
□ ⭐⭐⭐⭐⭐ 输出里任何一处模糊，都是模型替你决定的地方
```

## 路由表

| `skill-output/references/output-kind-three.md` | ⭐⭐⭐⭐⭐ 三类产出（产物/判定/变更）；⭐⭐⭐⭐⭐ 判定型不均衡测试集可拿 90 分假象；⭐⭐⭐⭐⭐ 变更型断言世界状态 |
| `skill-output/references/output-contract.md` | ⭐⭐⭐⭐ 输出契约基础：字段、类型、必填 |
| `skill-output/references/output-contract-templates.md` | ⭐⭐⭐⭐ 可抄的输出模板 |
| `skill-output/references/structured-output-pipeline.md` | ⭐⭐⭐⭐⭐ **结构化≠正确**：schema 合规不保证值；⭐⭐⭐⭐⭐ 无 description 的字段=省略了一半提示 |
| `skill-output/references/output-stability-contract.md` | ⭐⭐⭐⭐ `/clear` 后跑两遍测试法；⭐⭐⭐ 长度上限 ≤ 基线 ×1.5 |
| `skill-output/references/output-control.md` | ⭐⭐⭐⭐ 输出控制：长度、详尽度、抑制冗长 |
| `skill-output/references/numbers-in-output.md` | ⭐⭐⭐⭐⭐ 单位/精度/口径/派生算法；⭐⭐⭐⭐⭐ 虚假精度是廉价权威感；⭐⭐⭐⭐⭐ 0 vs 无数据 |
| `skill-output/references/output-ordering-priority.md` | ⭐⭐⭐⭐⭐ 顺序不是排版是主张；⭐⭐⭐⭐⭐ 默认顺序=生成顺序≠重要程度；⭐⭐⭐⭐⭐ 覆盖率/例外必须在前5行 |
| `skill-output/references/output-length-budget.md` | ⭐⭐⭐⭐⭐ "详尽"不是长度规格；⭐⭐⭐⭐⭐ 每段给上限不给下限；⭐⭐⭐⭐⭐ 长度膨胀是最安静的退化 |
| `skill-output/references/enumeration-and-completeness.md` | ⭐⭐⭐⭐⭐ 没有分母就没有完成；⭐⭐⭐⭐⭐ 覆盖率必须出现在输出里；"全面"是无上限的词 |
| `skill-output/references/output-template-vs-scale.md` | ⭐⭐⭐⭐⭐ 模板是某个规模的隐式承诺；⭐⭐⭐⭐⭐ 规模变大时严格遵守模板=输出不可用；⭐⭐⭐⭐⭐ 0 条时空模板最危险 |
| `skill-output/references/progress-reporting.md` | ⭐⭐⭐ 进度汇报：长任务的可见性 |
| `skill-output/references/grounding-verification.md` | ⭐⭐⭐⭐ 有据可查验证：⭐⭐⭐⭐⭐ 每个结论要能追溯到源 |
| `skill-output/references/output-becomes-fact.md` | ⭐⭐⭐⭐⭐ 输出进入上下文后获得与用户输入同等地位；自我确认闭环；不可追溯的结论永久变成事实 |

## Critical Rules

- ⭐⭐⭐⭐⭐ **schema 校验之后还要做语义校验**（总额==行和？ID 真存在？）
- ⭐⭐⭐⭐⭐ **每个字段都要写 description**——模型把字段描述当抽取指令用
- ⭐⭐⭐⭐ **长度膨胀是最容易被忽略的退化**：内容对、但越来越啰嗦，没人会报 bug
- ⭐⭐⭐⭐ 不稳定性测试要清会话再跑——否则第二次会自洽
- ⭐⭐⭐⭐ 部分成功必须报覆盖率，否则"分析完成"就是谎言
- ⭐⭐⭐ 输出模板要能被机器解析，不只是好看
- ⭐⭐⭐⭐ 输出重写/压缩最多 2 轮；超过则停止并报告当前状态（不得无限循环打磨措辞）

## 常见缺陷

| 缺陷 | ⭐ 后果 |
|---|---|
| ⭐⭐⭐⭐⭐ 字段无 description | 模型按自己的理解填（`status` 可指三种东西） |
| ⭐⭐⭐⭐⭐ 结构正确但值是猜的 | ⭐⭐⭐⭐ 所有门禁全绿，值是错的 |
| ⭐⭐⭐⭐ 无终止条件的"详尽报告" | 要么永不结束，要么自行宣布完成 |
| ⭐⭐⭐⭐ 省略失败项 | ⭐⭐⭐⭐⭐ "分析完成 12480 行"技术上真实且完全误导 |
| ⭐⭐⭐ 输出越来越长 | 静默退化，没人报 bug |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与路由校验 |
| `scripts/estimate_tokens.py <dir>` | 成本基线 |
| `skill-output/references/output-schema.md` | ⭐⭐⭐⭐⭐ 机器可判定的输出字段契约；无 description 的字段=省掉一半提示 |

## 参考

- 相关技能：《skill-execution》（执行期控制）·《skill-crafting》（正文与示例）·
  《skill-scripting》（脚本输出约定）·《skill-quality》（质量评分）
