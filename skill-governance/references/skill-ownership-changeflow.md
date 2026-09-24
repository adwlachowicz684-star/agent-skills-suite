# Owner 制度与变更流程

> 相关：《skill-governance》的 `retirement-pipeline.md` ·
> `ops-iteration-sop.md` · 《skill-distribution》的 `team-conventions-pr.md`
> 前置：`team-conventions-pr.md` 讲评审清单，
> 这份讲⭐ 谁对技能负责、以及一次改动要走完什么流程。

---

## 目录

- [1. ⭐ 为什么必须有 Owner](#1--为什么必须有-owner)
- [2. ⭐ Owner 的三项职责](#2--owner-的三项职责)
- [3. ⭐ 变更流程七步](#3--变更流程七步)
- [4. ⭐⭐ 一个真实翻车案例](#4--一个真实翻车案例)

---

## 1. ⭐ 为什么必须有 Owner

```
⭐ 每个技能必须有一个 Owner。这不是形式主义。
```

**不设 Owner 会发生什么**（一个很具体的场景）：

```
你们团队的 code-review 技能谁都能改，结果：
  小王加了一条 CSS 规则
  老张加了一条 SQL 规则
  实习生加了一条他在网上看到的"最佳实践"

⭐ 三个人互相不知道对方改了什么。
⭐ 一个月后 SKILL.md 变成了一锅粥。
```

**Owner 的准确定位**：

```
❌ Owner = 唯一能改技能的人
✅ ⭐ 任何人都可以提 PR
   ⭐ Owner 是最终的审批者和质量负责人
```

> ⭐ 这个区分很关键：它不是要垄断修改权，而是要解决
> **"新规则是否和已有规则矛盾、是否让技能膨胀"** 这个判断没人做的问题。

**怎么选、怎么交接**：

```
· 谁写的初版谁就是 Owner
· ⭐ 那个人离职，交接时必须指定新 Owner
· ⭐⭐ 没有 Owner 的技能应该被归档或删除
     ——⭐ 没人管的基础设施比没有更危险
```

---

## 2. ⭐ Owner 的三项职责

```
① Review PR：所有技能修改必须经过 Owner review
   ⭐ 不是走流程，是确保新规则不和已有规则矛盾、不让技能膨胀

② ⭐ 跑 eval：每次修改后 Owner 负责确认 eval 没有退化
   ——这和代码改完跑测试是一个道理

③ 决定发布：大的变更（新增规则类别、改变输出格式）由 Owner 拍板
```

> ⭐ 第 ② 项是这套制度真正的技术内核：
> **技能改动的可信度来自 eval，不来自"看起来合理"。**

---

## 3. ⭐ 变更流程七步

```
1. 本地修改技能
2. ⭐ 本地跑 eval，对比 baseline
3. eval 没退化 → 提 PR
4. ⭐ PR 描述必须写明：改了什么、为什么改、eval 结果
5. Owner review
6. CI 自动跑 eval
7. 合并到 main；⭐ 如果 eval 提升了，更新 baseline
```

**核心纪律**：

```
⭐⭐ 任何技能的修改都必须跑 eval。
你不会接受一个没跑测试的代码 PR。技能的修改也一样。
```

> 理由很直白：**你加了一条新规则，怎么知道它真的有效？
> 怎么知道它没有让别的规则出问题？⭐ 只有 eval 能回答。**

---

## 4. ⭐⭐ 一个真实翻车案例

```
老张给 code-review 技能加了一条"函数不超过 30 行"的规则。
听起来非常合理。
```

**跑完 eval 的结果**：

```
pass_rate: 0.85 → 0.72   ⭐ 掉了 13 个百分点
```

**为什么**：

```
⭐ 因为模型开始把"函数超过 30 行"标记为问题，
⭐ 但有些测试用例里的函数就是需要 40 行
   ——比如一个包含完整 switch-case 的状态机。
```

> ⭐⭐ **这个案例的价值在于它同时说明了三件事**：
>
> 1. ⭐ **一条"看起来正确"的规则会真实地损害表现**——
>    不跑 eval 永远发现不了，因为每次输出都"看起来很专业"
> 2. ⭐ **规则的代价往往落在边界情形上**（状态机函数），
>    而这正是 `three-failure-modes.md` 说的"隐式上下文依赖"
> 3. ⭐ **退回旧版本不是可耻的**——`retirement-pipeline.md` 的
>    "归档 ≠ 删除"在这里同样适用，**保留被推翻的规则及其 eval 数据**
>    是团队最值钱的资产之一

**配套的版本管理**（与 `version-changelog-practice.md` 一致）：

```
· 技能用语义化版本
· 通过标准 PR 流程评审改动
· 用代表性 prompt 测试
· ⭐ 在 changelog 里记录破坏性变更
```

**最小 changelog 格式**：

```markdown
# code-review.md changelog

## v1.3.0 — 2026-03-01
- Added: dependency vulnerability check to checklist
- Changed: security section elevated above suggestions

## v1.2.0 — 2026-01-15
- Added: accessibility checklist items for frontend reviews

## v1.1.0 — 2025-12-01
- Fixed: output format section now explicit about blocking vs non-blocking
```

> ⭐ 版本控制还能抓回归：
> **如果 code-review.md 的某次改动导致审查漏掉安全检查，
> git 历史会准确告诉你改了什么、什么时候改的。**

**一句值得记住的话**：

```
⭐ PR 流程让"审查你应用代码的那些人"，
⭐ 也去审查"指导模型行为的那些指令"——
⭐ 而后者的重要性并不更低。
```

---

## 速查

```
□ ⭐ 每个技能必须有 Owner
□ ⭐ Owner ≠ 唯一能改的人；是最终审批者与质量负责人
□ ⭐ 谁写初版谁是 Owner；离职必须交接
□ ⭐⭐ 没有 Owner 的技能应归档或删除（没人管的基础设施更危险）

Owner 三职责：
□ Review PR（防矛盾、防膨胀）
□ ⭐ 跑 eval 确认没退化
□ 拍板大变更（新规则类别、输出格式改变）

变更七步：
□ 本地改 → ⭐ 跑 eval 比 baseline → 提 PR
□ ⭐ PR 写明：改了什么/为什么/eval 结果
□ Owner review → CI 跑 eval → 合并 → ⭐ 有提升就更新 baseline

□ ⭐⭐ 没跑 eval 的技能 PR 不接受（同没跑测试的代码 PR）

changelog：
□ 语义化版本 + 破坏性变更显式记录
□ ⭐ git 历史是定位回归的第一工具
```

**一句话**：

> ⭐⭐ **"函数不超过 30 行"听起来无比正确，
> 直到 eval 告诉你 pass_rate 从 0.85 掉到了 0.72。**
