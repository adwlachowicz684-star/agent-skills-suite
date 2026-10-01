---
name: skill-input
description: 技能的输入侧契约：输入校验与分诊（残缺/矛盾/超范围）、数据依赖与前置产物声明、假设登记、相对时间必须解析、工具参数名不可猜。当用户给的信息不全、技能拿到错误时段的数据、或要判断"缺的东西该推断还是该问"时使用。
  Do NOT use for 输出格式与长度（用 skill-output）、执行期错误与恢复（用 skill-recovery / skill-execution）、示例与判断依据（用 skill-examples）。
---

# 输入侧契约

## 边界

- 用于：**技能"拿到什么"——校验、依赖、假设、时间解析、参数构造**
- 不用于：输出长什么样 → 《skill-output》
- 不用于：跑砸了怎么办 → 《skill-recovery》
- 不用于：措辞与文体 → 《skill-crafting》

## 核心原则

> ⭐⭐⭐⭐⭐ **依赖缺失是"响的失败"，假设不成立是"静的成功"。**
> ⭐⭐⭐⭐⭐ **时间窗口错了不报错——它有结果、有数字、有趋势，只是都是另一个时段的。**

```
□ ⭐⭐⭐⭐⭐ 被丢弃的需求必须出现在输出里（矛盾输入时模型默认选一个且不告诉你）
□ ⭐⭐⭐⭐⭐ 先判超范围，再判残缺，最后判矛盾
□ ⭐⭐⭐⭐⭐ "需要 Python"不是声明，python: ">=3.11" 才是
□ ⭐⭐⭐⭐⭐ 批量必须先枚举出 N；输出报"共 N / 成功 M / 失败 K"三段，不只报 status
□ ⭐⭐⭐⭐⭐ 猜参数名是幻觉高发区，而它会真的发出一次请求
□ ⭐⭐⭐⭐ 只写假定不写"不成立时"，比不写更糟
□ ⭐⭐⭐⭐ 同一任务内同一个问题最多问一次（硬上限 1 次）
□ ⭐⭐⭐⭐⭐ "除 X 之外"不是修饰语，是对集合的运算符——需额外一步才生效
□ ⭐⭐⭐⭐⭐ 来源冲突时听谁必须写明；上下文里的既有结论不算来源
□ ⭐⭐⭐⭐⭐ 校验通过 ≠ 输入是对的：容器合规、内容为空时后续全在处理 0 条
□ ⭐⭐⭐⭐⭐ 触发发生在语义完整之前；必需槽位要列出并一次性问完
```

## 路由表（按需深读）

| `skill-input/references/ambiguous-references-in-user-input.md` | ⭐⭐⭐⭐⭐ "也这样"不缺成分只缺指向；⭐⭐⭐⭐⭐ 分诊三类全过而指向不明；⭐⭐⭐⭐⭐ ≥2候选不得自行选 |
| `skill-input/references/input-validation-and-triage.md` | ⭐⭐⭐⭐⭐ 残缺/矛盾/超范围；先判超范围 |
| `skill-input/references/data-dependency-declaration.md` | ⭐⭐⭐⭐⭐ 数据依赖；前置产物读不到时模型会自己造一份 |
| `skill-input/references/assumption-registry.md` | ⭐⭐⭐⭐⭐ 假设≠依赖；静的成功；规模假设只在生产崩 |
| `skill-input/references/relative-time-resolution.md` | ⭐⭐⭐⭐⭐ 相对时间必须在执行时解析并写进输出 |
| `skill-input/references/inference-vs-asking.md` | ⭐⭐⭐⭐⭐ 缺的该推断还是该问；⭐⭐⭐⭐⭐ 判据是错了能不能被看出来；⭐⭐⭐⭐⭐ L2 推断并标注在首行 |
| `skill-input/references/ambiguous-input-selection.md` | ⭐⭐⭐⭐⭐ 多个都合法时按相似度选≠用户意图；⭐⭐⭐⭐⭐ 选错零信号（每个候选都合法）；⭐⭐⭐⭐ 默认规则要可复现 + 选中对象回显首行 |
| `skill-input/references/tool-argument-construction.md` | ⭐⭐⭐⭐⭐ "用 X 工具"不是参数说明；200+成功+缺内容最静默 |
| `skill-input/references/user-input-omissions.md` | ⭐⭐⭐⭐⭐ 用户没说的不是授权；⭐⭐⭐⭐⭐ 补的依据是训练分布不是本项目；⭐⭐⭐⭐⭐ 确认会把"没说"变成"说了" |
| `skill-input/references/input-cardinality.md` | ⭐⭐⭐⭐⭐ 默认基数是 1；⭐⭐⭐⭐⭐ "这些文件"与"这个文件"差别极小；⭐⭐⭐⭐⭐ N 由上下文数出来而非枚举出来；批量必须报 共N/成功M/失败K |
| `skill-input/references/input-negation-and-exceptions.md` | ⭐⭐⭐⭐⭐ "除了/只/除非"不属于动作·对象·修饰任何一类，需额外一步才生效；⭐⭐⭐⭐⭐ 排除项通常是数量最大的一批；⭐⭐⭐⭐⭐ N 是减法之后的；⭐⭐⭐⭐⭐ 已排除项必须出现在输出里 |
| `skill-input/references/input-source-precedence.md` | ⭐⭐⭐⭐⭐ 用户话/配置文件/状态三来源无默认优先级；⭐⭐⭐⭐⭐ 默认是"最近的"且几乎总错；⭐⭐⭐⭐⭐ 覆盖配置必须报"本次覆盖了 X（默认 Y）"；⭐⭐⭐⭐⭐ 上下文结论不算来源 |
| `skill-input/references/input-passes-validation-but-wrong.md` | ⭐⭐⭐⭐⭐ 错误响应体/空壳/旧数据三者都能让流程全绿；⭐⭐⭐⭐⭐ `get(k,[])` 吃掉 error 字段；⭐⭐⭐⭐⭐ 校验只查容器不查内容；默认值集合 {null,0,"",[],1970-01-01} 需第二信号交叉确认 |
| `skill-input/references/input-arrives-late.md` | ⭐⭐⭐⭐⭐ 第一条消息就能独立完成 → 模型不问直接做；⭐⭐⭐⭐⭐ 用户以为在补充，技能当成中途变更；⭐⭐⭐⭐⭐ 判据是"技能跑到哪一步"不是"用户意图"；⭐⭐⭐⭐⭐ 未开始执行时的补充要丢弃中间结论 |

## Critical Rules

- ⭐⭐⭐⭐⭐ 无数据必须写"未获取"，不得用推断值填充
- ⭐⭐⭐⭐⭐ 输入含 error 字段时视为取数失败，≠"0 条"；不得用 `get(k, [])` 兜掉
- ⭐⭐⭐⭐⭐ 来源冲突按"用户 > 配置 > 状态"取值；用 updated_at 判新旧，不用读取顺序
- ⭐⭐⭐⭐⭐ 时间窗口解析结果写进输出首行
- ⭐⭐⭐⭐⭐ 401/403 → 停止并报告，重试上限 0 次（重试不改变权限）
- ⭐⭐⭐⭐⭐ 矛盾输入必须标注"以下两项冲突，本次取了 A"
- ⭐⭐⭐⭐ 假设章节必须同时写"不成立时"的表现
- ⭐⭐⭐⭐ 环境细节不写死，改为运行时探测

## 何时不用（边界）

- ⭐⭐⭐ "输出该多长" → 《skill-output》的 `output-length-budget`
- ⭐⭐⭐ "失败后怎么重试" → 《skill-recovery》的 `retry-budget`
- ⭐⭐⭐ "这句话含不含糊" → 《skill-crafting》的 `vague-word-blacklist`

## 参考

- 相关技能：《skill-output》（另一端）·《skill-execution》（执行期）·
  《skill-recovery》（失败）·《skill-content》（默认动作）·
  《skill-crafting》（措辞）
