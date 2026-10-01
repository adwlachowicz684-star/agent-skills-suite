---
name: skill-precision
description: 一句话是否真的构成约束——无主语指令的执行主体、条件嵌套的路径爆炸、含糊词、无出处数字、枚举封闭性、列表项关系、指代与术语一致性。用于「指令写了但仍被绕过」「改一处不影响另一处」「模型理解成了另一种关系」「同一件事在两个技能里说法不同」。
  Do NOT use for 指令该用禁令还是配方的形态选择（用 skill-crafting）、示例与判断依据（用 skill-examples）、范围与粒度（用 skill-scoping）、执行期错误与恢复（用 skill-recovery）。
---

# 表述精确性

> 分工：
> 《skill-crafting》定⭐ **这句话用什么形态写**（禁令 / 配方 / 槽位 / 条件）；
> 本技能定⭐⭐⭐⭐⭐ **写出来的这句话是不是真的构成约束**；
> 《skill-examples》定⭐⭐⭐ **示例从哪来**。

## 边界

- 用于：**同一句话的精确性**——主语、分支、关系、指代、数字、术语
- 不用于：整份技能的创建流程 → 《skill-authoring》
- 不用于：瘦身与拆分 → 《skill-refining》
- ⭐ 不用于：示例的采集与取舍 → 《skill-examples》

## 核心原则

> ⭐⭐⭐⭐⭐ **一条"看起来是约束"的句子，和一条"真的是约束"的句子，
> 在成本上完全一样，在效果上差一个数量级。**

```
□ ⭐⭐⭐⭐⭐ 无主语祈使句，模型默认认领为自己的动作——包括它做不到的那些
□ ⭐⭐⭐⭐⭐ 嵌套两层条件 = 未定义的组合比写下的分支多，而那些组合由模型定义
□ ⭐⭐⭐⭐⭐ 含糊词不是"不够具体"，是"授权模型用自己的默认值填充"
□ ⭐⭐⭐⭐⭐ 没写 else 的 if，比不写 if 更糟——它给了"作者考虑过"的信号
□ ⭐⭐⭐⭐ 没有出处的数字看起来是规格，实际是偏好
□ ⭐⭐⭐⭐ 列表只表达"这是一组"，不表达组内是且、或、还是顺序
□ ⭐⭐⭐⭐ "上文/第 3 步/如下"在压缩后指令还在、引用没了
□ ⭐⭐⭐⭐ 同一个值在两个技能里各写一遍 = 复制时切断了同步关系
```

## 路由表（按需深读）

| `skill-precision/references/imperative-subject-drift.md` | ⭐⭐⭐⭐⭐ 无主语指令的执行主体漂移；"确保"压缩掉了主语和 else；模型会生成"已确认" |
| `skill-precision/references/nested-condition-explosion.md` | ⭐⭐⭐⭐⭐ 嵌套条件的路径按乘法增长；决策表把乘积变成和；表行数=最少用例数 |
| `skill-precision/references/conditional-branch-writing.md` | ⭐⭐⭐⭐⭐ 没有 else 的 if = 授权模型自己定义 else；"有但不可用"那一档 |
| `skill-precision/references/conflicting-instructions.md` | ⭐⭐⭐⭐⭐ 详尽vs简洁等五类冲突；模型默认折中不是二选一；按「被约束的维度」分组才能发现 |
| `skill-precision/references/list-item-relations.md` | ⭐⭐⭐⭐⭐ 列表项是且/或/顺序；默认解读是且+顺序；混合列表最隐蔽 |
| `skill-precision/references/enumeration-closed-vs-open.md` | ⭐⭐⭐⭐⭐ 枚举是穷举还是举例；列表越长越像穷举；列表外默认归类且静默 |
| `skill-precision/references/positional-references.md` | ⭐⭐⭐⭐⭐ 上文/第3步/如下；压缩后指令留下而引用没了；给中间产物起名 |
| `skill-precision/references/vague-word-blacklist.md` | ⭐⭐⭐⭐⭐ 含糊词替换表；五类伪装成约束的词；可 grep 的 CI 检查 |
| `skill-precision/references/unjustified-numbers.md` | ⭐⭐⭐⭐⭐ 没有出处的数字；具体性≠有依据；数字+出处+越界动作 |
| `skill-precision/references/terminology.md` | ⭐⭐⭐⭐ 术语表的关键是第三列「不要用的说法」；模型不做同义消解 |
| `skill-precision/references/constraint-carrier-ladder.md` | ⭐⭐⭐⭐⭐ 约束写在哪一层：六层载体；⭐⭐⭐⭐⭐ 可靠性与覆盖面反向；⭐⭐⭐⭐⭐ 需要判断的规则硬编码=错误的硬拦截 |

## Critical Rules

- ⭐⭐⭐⭐⭐ 每条祈使句都要能回答"谁能在这一步真的执行它"；做不到的人/系统那类必须写主语
- ⭐⭐⭐⭐⭐ 条件不超过两层；嵌套 ≥2 层改成决策表或两阶段（先分类再处理）
- ⭐⭐⭐⭐⭐ 写 if 必须写 else，包括"有但不可用"这第三种状态
- ⭐⭐⭐⭐⭐ 枚举超过 5 项按开放处理并显式写"非穷举"
- ⭐⭐⭐⭐ 列表的引导句必须写明组内关系（且 / 或 / 按顺序）
- ⭐⭐⭐⭐ 每个数字要有出处；同一个数字只能有一个出处
- ⭐⭐⭐⭐ 禁止"上文/如下/第 3 步"式指代——给中间产物和章节起名

## 何时不用（边界）

- ⭐⭐⭐ 该用禁令还是配方 → 《skill-crafting》的 `guidance-forms`
- ⭐⭐⭐ 一句话该多长 → 《skill-content》的 `writing-style`
- ⭐⭐⭐ 示例放几个 → 《skill-examples》
- ⭐⭐⭐ 列表项该不该拆成独立步骤 → 《skill-execution》

## 参考

- 相关技能：《skill-crafting》（形态）·《skill-content》（措辞与章节）·
  《skill-examples》（示例）·《skill-output》（输出契约）·
  《skill-evaluating》（怎么验证这些精确性真的有效）
