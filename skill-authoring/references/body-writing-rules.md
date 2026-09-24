# 正文写作九条：可逐条检查的启发式

> 这份不是原则，是**可机械执行的检查项**。
> 每条都给了改前改后。

## 目录

- [祈使句优先](#祈使句优先)
- [具体胜于抽象](#具体胜于抽象)
- [一条 bullet 一个主张](#一条-bullet-一个主张)
- [步骤要编号](#步骤要编号)
- [决策点内联](#决策点内联)
- [命令要写全](#命令要写全)
- [解释 WHY](#解释-why)
- [给具体阈值](#给具体阈值)
- [约束要就地](#约束要就地)

## 祈使句优先

```
✅ "Run X"
⚠️ "You should run X"
❌ "It is recommended to run X"
```

> **去掉助动词。** 每一级弱化都在给模型留"这是建议不是要求"的余地。

frontmatter 里同理，description 用**动词开头**：

```
❌ "A skill for running tests"
✅ "Pick and run the smallest correct validation step
     (checks → focused Jest → broader suites).
     Use whenever you modify code and need confidence quickly."
```

差别：第二版有**动词开头**、**具体流程**、**情境触发**。

## 具体胜于抽象

```
❌ "use appropriate tools"        → 写出真实工具名
❌ 占位符代码                      → 给能跑的代码
```

判据：**这段代码原样复制到别处能跑吗？**
（见 `writing-style.md` 的占位符陷阱。）

## 一条 bullet 一个主张

```
❌ "做 A 和 B 和 C"     ← 拆开
```

理由不是美观：

> ⭐ **agent 扫得更快，漏得更少。**
> 一条 bullet 里塞三件事，模型经常只执行第一件。

## 步骤要编号

```
✅ 1. / 2. / 3.
❌ - / - / -
```

> **agent 用数字比用项目符号更能跟踪进度。**

这也让"跳到第 3 步""第 2 步失败了"这类交互有明确指代。

## 决策点内联

不要把所有分支扔到最后：

```markdown
### Step 3: Check the response

If the response is 200:
  - Proceed to Step 4
If the response is 403:
  - The site has a WAF. Try HEAD instead of GET.
If the response is 5xx:
  - The server is down. Stop and escalate.
```

> ⭐ 这正是 `guidance-forms.md` 里的
> **`if <可观察谓词> then`**——条件必须可执行，不能写"视情况"。

## 命令要写全

```
❌ "Run the health check tool"
✅ "Run: `node tools/crawl/crawl-health.js --json`"
```

抽象描述会让模型**自己编一个命令**，
然后你会得到一个看起来对但路径不对的调用。

## 解释 WHY

```
❌ "Use HEAD requests for existence checks"
✅ "Use HEAD requests for existence checks —
     they transfer no body, making them 10-50x faster
     and less likely to trigger rate limits"
```

> ⭐ WHY 建立的是**心智模型**，
> 让模型能在没覆盖到的场景里做出正确推断。
> 只给 WHAT，它只能照抄。

## 给具体阈值

```
❌ "If the save rate is low, investigate"
✅ "If the save rate is below 80%, investigate —
     this means >20% of fetched content is being lost"
```

这条和 `grounding-verification.md` 的"可观察判据"是同一件事：
**"低"不是判据，"低于 80%"才是。**

## 约束要就地

```
❌ 把规则塞在末尾的 "Notes" 章节
✅ ⭐ 移到它所约束的那个步骤旁边
```

> **埋在尾部的规则会被漏掉。**
> 这是截断保头不保尾之外，第二个"放错位置等于没放"的场景。

## 反面清单：该删的东西

```
□ 重复的规则
□ 重述的上下文
□ "如果需要别的随时告诉我"
□ 填充性的开场白
```

## 改技能时绝不能动的东西

如果你是在**重构**一个已有技能（不是重写），这些是**行为**，
碰了就改变了技能做什么：

```
□ ⭐ 工作流步骤的集合
   ——可以为了清晰重命名或重排，但绝不删、不增、不合并
□ 任何显式的 must / do not / never 规则
   ——那是用户有意写下的
□ frontmatter 里的 allowed-tools: 列表
□ 必需的产物路径、文件命名约定、输出格式
□ ⭐ description 里的触发范围
   ——可以 sharpen 措辞，但绝不收窄或放宽匹配范围
□ ⭐ 记录边界情况的示例
   ——那些是对 description 契约的测试
```

> ⭐ **拿不准某个改动是"性能优化"还是"行为改变"时，先问用户。**

## 一个可抄的重构流程

```
① 盘点：git status --porcelain + 编辑历史，列出候选文件与行数
② 过滤：只看作用域内的 .md / .tmpl / .prompt
③ 通读每个文件，记下结构划分
④ ⭐ 逐文件出 diff 计划
   格式：启发式 → 位置 → 建议改动
   一条 bullet 一个违规
   ❗ 这一步不要动手改
⑤ ⭐ 给用户看 diff 计划，等批准
⑥ 用 Edit 逐处修改
   ⭐ ——用 Edit 不用 Write：最小 diff 可审查，整体重写会藏住回归
⑦ 重新通读每个文件，确认行为没变
⑧ 报告：每个文件 起→止 行数、关键收益、以及
   ⭐ 哪些文件没动（已经够紧，或改动会跨越行为线）并说明原因
```

第 ⑧ 条里"明确说出哪些没动"这点值得学——
**沉默的不作为容易被误认为遗漏**。
