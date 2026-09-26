# 代码审查技能实例：八步与三档判词

> 相关：（已移至 _parked 领域实例库）的 `code-review-trust.md` ·
> `five-starter-skills.md` · 《skill-evaluating》的 `four-dimension-eval.md`

---

## 目录

- [1. 一个真实的高分实例](#1-一个真实的高分实例)
- [2. 八步](#2-八步)
- [3. ⭐ 三档判词逻辑](#3--三档判词逻辑)
- [4. ⭐ 三条硬规则](#4--三条硬规则)
- [5. 本报告 vs 人工审查](#5-本报告-vs-人工审查)

---

## 1. 一个真实的高分实例

这是一个被评为 A 级的审查技能，结构值得完整学习。
它的核心是**把"审查"拆成八个可自动化判定的步骤**。

---

## 2. 八步

| 步 | 检查 | 判定 |
|---|---|---|
| 1 | 里程碑前缀（先新格式，回退旧格式） | — |
| 2 | ⭐ **命名规范**（分支名、提交前缀、祈使语气、无 Co-Authored-By） | PASS/WARN/FAIL |
| 3 | ⭐ **文档新鲜度**（跑共享工具，warn 模式） | WARN |
| 4–5 | — | — |
| 6 | ⭐ **代码质量扫描** | FAIL/WARN |
| 7 | **提交格式**（首行 ≤72、多行用 `-`、>20 条建议 squash） | WARN |
| 8 | 生成报告 | — |

### 第 2 步：命名规范

```
分支名匹配 feature/PREFIX-#.#-description
每条提交以 PREFIX-#.#: 开头（与分支里程碑一致）
⭐ 提交信息用祈使语气（前缀后第一个词不是过去式：
   不能是 Added / Fixed / Updated）
无 Co-Authored-By 行
```

> ⭐ "祈使语气"这条有具体的机械判据——
> **检查前缀后第一个词是不是过去式**。可自动化。

### 第 3 步：文档新鲜度

```bash
.claude/skills/_shared/doc-freshness.sh --mode=warn
```

```⭐ warn 模式永远退出 0——无论是否过期都继续审查。⭐ 但 /pr 跑的是 block 模式，这里标记的过期会阻塞后续 /pr，直到用户提交文档更新。
```

> 这个设计很妙：**同一个工具两种模式**，
> 审查时只警告、提交时阻断。
> 与 `four-dimension-eval.md` 里"阈值按用途分档"同理。

### 第 6 步：代码质量扫描

| 级别 | 模式 |
|---|---|
| ⭐ **FAIL** | 疑似密钥：`sk-[a-zA-Z0-9]`、`AKIA[A-Z0-9]`、`password=`、`secret=`、`token=` |
| WARN | TODO 后 20 字符内没有里程碑上下文 |
| WARN | 调试语句：`console.log`、`fmt.Println`、`print(`、`debugger` |
| WARN | ⭐ 任何新增单文件超过 500 行 |

---

## 3. ⭐ 三档判词逻辑

```
Code Review Report
==================
Branch / Milestone / Mode / Commits
Naming Convention:  [PASS | WARN (N) | FAIL (N)]
Documentation:      [PASS | WARN (N)]
Code Quality:       [PASS | WARN (N) | FAIL (N)]
Commit Format:      [PASS | WARN (N)]
Details: [每条 WARN/FAIL 带 file:line]
Verdict: [CLEAN | READY FOR PR (N warnings) | NEEDS FIXES (N failures)]
```

```⭐ 任何 FAIL      → NEEDS FIXES（且建议列出具体修复）⭐ 只有 WARN      → READY FOR PR⭐ 全部 PASS      → CLEAN
```

> ⭐ **FAIL 与 WARN 必须有不同后果**，否则分级没有意义。
> 这与 `quality-rubric.md` 的"单项否决"是同一思路。

---

## 4. ⭐ 三条硬规则

```
① ⭐ 只读——这个技能绝不修改文件，只报告
② 两种模式跑完全相同的检查（分支模式 / PR 模式）
③ ⭐ 疑似密钥永远是 FAIL，绝不放过
```

第 ③ 条对应 `least-privilege.md` 的"密钥永不进入上下文"——
**在审查侧就要拦住**。

---

## 5. 本报告 vs 人工审查

> ⭐ **这补充人工审查，而非替代——
> 它抓的是规范漂移，不是逻辑 bug。**

这句声明很重要：
**技能要写明自己不做什么**（对应 `scope-section.md` 的边界章节），
否则用户会误以为跑过就等于审过了。

---

## 速查

| 设计点 | 做法 |
|---|---|
| 分级 | ⭐ FAIL 阻断、WARN 不阻断 |
| 可自动化 | 祈使语气、密钥模式、行数——都能脚本查 |
| 双模式 | 同一工具 warn / block 两种退出行为 |
| 权限 | ⭐ 只读，只报告 |
| 边界 | ⭐ 声明"不查逻辑 bug" |
| 报告 | ⭐ 每条带 file:line |
