# 输出 schema：让"输出对不对"变成一条命令

> 相关：`skill-output/references/output-contract.md`（人读的输出契约）·
> `skill-output/references/structured-output-pipeline.md`（结构化≠正确）·
> `skill-output/references/output-stability-contract.md`（稳定性）
> 分工：
> `skill-output/references/output-contract.md` 定义⭐⭐⭐ **输出长什么样**（给人看）；
> 本份定义⭐⭐⭐⭐⭐ **输出能被机器判定对错的那部分**（schema）。

---

## 目录

- [1. ⭐⭐⭐⭐⭐ 契约 vs schema：两件事](#1--契约-vs-schema两件事)
- [2. ⭐⭐⭐⭐⭐ 没有 description 的字段等于省掉一半提示](#2--没有-description-的字段等于省掉一半提示)
- [3. 必填、可空与"未获取"](#3-必填可空与未获取)
- [4. ⭐⭐⭐⭐ schema 合规 ≠ 值正确](#4--schema-合规--值正确)
- [5. 一个可直接抄的 schema.yaml](#5-一个可直接抄的-schemayaml)
- [6. ⭐⭐⭐⭐ 什么时候不该上 schema](#6--什么时候不该上-schema)

---

## 1. ⭐⭐⭐⭐⭐ 契约 vs schema：两件事

| | 输出契约 | ⭐ 输出 schema |
|---|---|---|
| 读者 | 人（看格式是否对） | ⭐⭐⭐⭐⭐ **机器（能否判定对错）** |
| 形态 | 模板、示例、字数 | 字段、类型、约束 |
| 判据 | "看起来像" | ⭐⭐⭐⭐ `validate()` 通过与否 |
| 能自动化吗 | 不能 | ⭐⭐⭐⭐⭐ 能 |

> ⭐⭐⭐⭐ 判据：⭐⭐⭐⭐⭐ **"输出一个 JSON"不是 schema，字段定义才是。**
> 正如"需要 Python 环境"不是依赖声明，`python: ">=3.11"` 才是。

上 schema 的唯一理由不是整齐，是⭐⭐⭐⭐⭐ **它让"输出对不对"从需要人读，变成一条命令**。

---

## 2. ⭐⭐⭐⭐⭐ 没有 description 的字段等于省掉一半提示

```yaml
# ❌
- name: status
  type: string
```

> ⭐⭐⭐⭐⭐ `status` 可以指 HTTP 状态、订单状态、或评审状态。
> ⭐⭐⭐⭐ **模型是把字段描述当作抽取指令在用的**——
> 你写了描述，它才知道该往里填什么；不写，它就按自己的默认值填。

```yaml
# ✅
- name: status
  type: string
  description: >
    本次评审结论。仅取 passed / failed / needs_changes 三值之一。
    不要填 HTTP 状态码，不要填自由文本。
```

> ⭐⭐⭐⭐⭐ **一个没有 description 的字段，等于省略了你一半的提示。**
> 这是"每一处模糊都是一次授权模型替你决定"的完美实证。

枚举值要写死三值，并显式排除最常见的误填——⭐⭐⭐⭐ **排除项比定义项更值钱**，因为误填是往"看起来合理"的方向走的。

---

## 3. 必填、可空与"未获取"

三档，不要只用两档：

| 档位 | 含义 | ⭐ 用途 |
|---|---|---|
| `required: true` | 必须有值 | 主结论 |
| `nullable: true` | 可以没有（正常情况） | 可选字段 |
| ⭐⭐⭐⭐⭐ `unknown` 显式值 | 查了但没查到 | ⭐⭐⭐⭐⭐ **防静默编造** |

> ⭐⭐⭐⭐⭐ 第三档最常被省，而它恰恰是唯一能防住"模型把 0 当成结果"的那档。

理由：`nullable` 只能表达"可以没有"，无法区分"确实没有"与"没查到"。而⭐⭐⭐⭐⭐ **在这两者之间，模型的默认动作是填一个——通常填 0 或"无"**，因为它看起来中性。

```yaml
- name: new_issues
  type: integer
  # ⭐ 必须允许这个字面值出现在输出里
  allowed_special: ["unknown"]
  description: 新增问题数。未获取到时必须填字符串 "unknown"，禁止填 0。
```

---

## 4. ⭐⭐⭐⭐ schema 合规 ≠ 值正确

> ⭐⭐⭐⭐⭐ **约束解码只保证响应符合 schema 的类型和结构，不保证值是对的。**
> 源文本有歧义时，模型完全可以给一条负面评价返回 `{"sentiment":"positive"}`。

危险在于所有门禁都是绿的：

```
JSON 解析 ✅ · schema 通过 ✅ · 字段齐全 ✅ · ⭐ 值是猜的 ❌
```

所以流程必须是两段，不能只有第一段：

```
① schema 校验（结构）→ 失败则重试或报错
② ⭐⭐⭐⭐⭐ 语义校验（值）→ 在应用代码里做，不在提示里做
```

第 ② 步的三条最实用：总额 == 行和？币种一致？⭐⭐⭐⭐⭐ **ID 真的存在吗？**

---

## 5. 一个可直接抄的 schema.yaml

```yaml
version: 1
fields:
  - name: summary
    type: string
    required: true
    max_lines: 3
    description: 一句话结论，不含过程。

  - name: items
    type: array
    required: true
    description: 逐条结果。每条必须有 id 与 status。
    items:
      - name: id
        type: string
        required: true
        description: 来源中的原始 ID，不要重新编号。
      - name: status
        type: enum
        values: [passed, failed, needs_changes]
        required: true

  - name: coverage
    type: number
    required: true
    description: 覆盖率 = 成功条数 / 扇出清单条数。分母来自清单，不是来自返回数。
    range: [0, 1]

  - name: failures
    type: array
    required: true
    description: ⭐ 失败清单。为空也要显式给 []，不得省略该字段。
```

> ⭐⭐⭐⭐ `failures` 那条是交接协议的核心：⭐⭐⭐⭐⭐ **没有一方在撒谎，
> 是交接协议里没有这个字段**——有 schema 时它无法被省略。

---

## 6. ⭐⭐⭐⭐ 什么时候不该上 schema

```
❌ 输出是自由文本（报告、建议、解释）→ 用契约模板，不要硬套 schema
❌ 字段会频繁变动 → schema 会变成维护负担，且过期 schema 会拒绝正确输出
❌ ⭐⭐⭐ 只读一次、没人消费 → 结构化的收益来自"被消费"，没人消费就是纯成本
```

> ⭐⭐⭐⭐ **schema 的价值来自下游。** 有下游（脚本解析、另一个技能、CI 断言）才值得上；
> 没有下游，它只是把"看起来对"换成了"解析通过"。

---

## 路由表

| 想解决什么 | 去哪 |
|---|---|
| 输出模板、示例、字数 | `skill-output/references/output-contract.md` |
| 结构对了但值是错的 | `skill-output/references/structured-output-pipeline.md` |
| 两次跑出来的不一样 | `skill-output/references/output-stability-contract.md` |
| 输出里有假数字 | `skill-output/references/numbers-in-output.md` |
| 输出里有占位符 | `skill-output/references/placeholder-in-output.md` |
