# Git / PR 工作流类技能

> ⭐ **三个小技能组成一条日常循环**——
> 这是"小而尖、靠组合"的最佳示范。

## 目录

- [三个技能组成的循环](#三个技能组成的循环)
- [技能 1：原子提交](#技能-1原子提交)
- [技能 2：创建 PR](#技能-2创建-pr)
- [技能 3：处理 PR 反馈](#技能-3处理-pr-反馈)
- [内置护栏的价值](#内置护栏的价值)

---

## 三个技能组成的循环

```
git-atomic-commits       把一堆改动拆成干净的提交
        ↓
gh-pr-create             推送 + 用一致的格式开 PR
        ↓
gh-address-pr-comments   取反馈 → 加回归测试 → 修 → 推送 → 回复
```

> ⭐ **注意这是"三个技能"而不是"一个大技能"**——
> 呼应 `skill-authoring` 的 `creation-framework.md` 的粒度判断与
> `skill-authoring` 的 `what-not-to-do.md` 的坑 2：**一个技能一件事**。

---

## 技能 1：原子提交

**目标**：把"一堆改动"变成小的 Conventional Commits，以干净的 git status 收尾。

**它替你决定的三件事**：

```
□ 提交边界怎么切
□ 暂存策略
□ 提交信息怎么写
```

**典型命令模式**：

```bash
git status -sb
git diff --stat
git add -p
git commit -m "feat(scope): …"   # 重复直到干净
```

**内置护栏**（这些才是技能的价值所在）：

```
□ ⭐ 不在 main/master 上提交（分支安全闸门）
□ ⭐ 鼓励把 lockfile 与依赖变更一起提交
□ ⭐ 优先单一目的的提交（必要时用 git add -p）
```

> ⭐ **"不在 main 上提交"是典型的 hook 候选**——
> 呼应 `skill-crafting` 的 `claude-md-vs-skill.md`：这句话含"绝不"且机器能检查，
> ⭐ 最好用 hook 确定性拦截，而不是靠模型记住。

---

## 技能 2：创建 PR

**前置检查**：

```bash
git status -sb
gh auth status
```

**流程**：

```bash
git push -u origin HEAD   # 首次推送设 upstream
git push                  # 之后直接 push
```

**PR 正文格式**（固定下来，每次都一样）：

```markdown
## Summary
## Major changes
<!-- 可选 -->
## Screenshots
## Tests
## Additional info
```

> ⭐ **"每次都一样"是这里的核心价值**：
> 一致性让 PR 更容易被扫读和评审。
> 呼应 `skill-crafting` 的 `output-contract.md` 的输出模板与
> （领域实例库·已归档） 的 `writing-org-context.md` 的固定结构写作。

---

## 技能 3：处理 PR 反馈

**取反馈**：

```bash
gh pr checkout "$PR_NUMBER"
gh pr view "$PR_NUMBER" --json number,title,url,headRefName,baseRefName,comments,reviews
```

**它强制的五件事**（这是最有价值的部分）：

```
1. ⭐ 给反馈分类——有意义的 vs 主观/含糊的
2. ⭐ 修之前先加回归测试（如果可测）
3. ⭐ 推送前跑完整测试套件
4. ⭐ 回复线程时说明改了什么 + 提交 SHA
5. ⭐ 全部推送完之后才重新请求评审
```

> ⭐ **第 1 条尤其值得单独学**——
> **不是所有反馈都要照做**。要求 agent 先分类，
> 避免它把主观偏好当成必须执行的修改，或反之忽略真问题。

**第 4 条**也是好实践：回复里带上**具体改了什么 + commit SHA**，
让评审者能直接跳转验证（呼应 `skill-crafting` 的 `grounding-verification.md` 的证据文化）。

---

## 内置护栏的价值

> ⭐ **回头看这三个技能，真正值钱的不是"能自动化"，
> 而是那些"不许做"的护栏**：

```
□ 不在 main 上提交
□ 修之前先加回归测试
□ 推送前跑完测试
□ 全部推完才重新请求评审
□ PR 正文格式固定
```

> ⭐ 呼应 `skill-crafting` 的 `guidance-forms.md` 与 `legacy-modernization.md`：
> **禁令必须配正面做法**——
> 这里的每一条都既有"不许"（不在 main 提交）也有
> "该怎么做"（切分支、git add -p）。

**与 CI 的衔接**（详见 `skill-governance` 的 `ci-cd-integration.md`）：

```
□ ⭐ CI 是提交后的独立验收，不是远程调试器
□ 本地自检与 CI 用同一套标准
□ CI 失败后：agent 先判断归属，能修就修 + 本地验证 + 重推
```

---

## 自查

```
□ 是否拆成了多个小技能（而非一个大而全的）？
□ ⭐ 是否有"不在 main 上提交"这类分支安全护栏？
□ 是否鼓励 lockfile 与依赖变更一起提交？
□ 是否优先单一目的提交（用 git add -p）？
□ ⭐ PR 正文格式是否固定？
□ ⭐ 处理反馈时是否先分类（有意义 vs 主观）？
□ 是否要求"修之前先加回归测试"？
□ 是否要求推送前跑完整测试套件？
□ ⭐ 回复是否带"改了什么 + commit SHA"？
□ ⭐ 是否要求全部推完才重新请求评审？
□ 每条禁令是否都配了正面做法？
□ ⭐ 机器可确定性检查的护栏是否考虑用 hook？
□ 是否与 CI 流程衔接（而非替代 CI）？
```
