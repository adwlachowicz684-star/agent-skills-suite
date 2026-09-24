# 三类失败模式：欠触发 / 误触发 / 执行失败

> 相关：《skill-evaluating》的 `trigger-debugging.md` ·
> `trigger-eval-set.md` · 《skill-patterns》的 `trigger-fix-nine-causes.md`
> 前置：那些文档讲"怎么修"，这份讲"三类故障各自的根因链路与诊断思路"。

---

## 目录

- [1. ⭐ 一个前提：触发是概率行为](#1--一个前提触发是概率行为)
- [2. 欠触发（Under-trigger）](#2-欠触发under-trigger)
- [3. ⭐ 误触发（False Trigger）——危害更大](#3--误触发false-trigger危害更大)
- [4. ⭐ 执行失败（Execution Failure）——最隐蔽](#4--执行失败execution-failure最隐蔽)
- [5. ⭐ 15 条评测集](#5--15-条评测集)

---

## 1. ⭐ 一个前提：触发是概率行为

```
⭐ 技能的触发依赖模型对 description 的语义匹配，
⭐ ⭐ 而语义匹配是概率行为，不是精确匹配。
```

> ⭐ **这意味着：措辞、范围、排除条件的调整，
> ⭐ 不靠直觉靠数据。**
> 没评测就没基线，没基线就无法迭代。

---

## 2. 欠触发（Under-trigger）

**表现**：用户意图明确匹配，但技能没被激活。

**根因链路**：

```
用户输入 → 匹配 description → 无匹配 → 未加载
                 ↑
            ⭐ 根因在此处
```

**三个根因**：

**① description 写得太窄**（最常见）

```
只写了技术术语，没覆盖用户的自然语言表述。

❌ "Review a pull request diff for correctness and security."

用户可能说：
  "帮我看看这个改动有没有问题"
  "这段代码安不安全"
  "review 一下"
  "check my changes"
⭐ 以上四条全部无法匹配
```

> ⭐ **开发者写 description 时会下意识用精确的技术语言**，
> ⭐ **但用户实际措辞往往更随意、更多样。**
> 这正是 `activation-rate.md` 里"测试措辞是作者的词汇"那条。

**② 语义距离过大**

```
⭐ 中文团队用英文写 description，中文请求触发不了。
⭐ 这不是翻译问题，而是语义空间中的距离问题。
```

> ⭐ **"帮我看看"和 "Review a pull request diff" 在模型内部表示的距离
> 可能远大于预期。**
> 团队成员技术水平参差不齐时，同一功能的描述差异会非常大。

**③ 竞争技能的 description 更宽泛**

```
⭐ 两个技能描述有重叠时，模型倾向选择描述更宽的那个。

例：pr-review 与 code-quality
    若后者 description 更宽泛 → 前者的请求被错误路由
```

**诊断三步**：

```
① 找用户 prompt 与 description 之间的语义断裂点
   （"检查边界条件" ≈ "correctness"，但语义距离大）
② ⭐ 检查竞争技能：grep -r "description:" skills/ | grep -i "check|inspect"
③ 修：在 description 中加入覆盖性表述
```

**修法三条**：

```
① ⭐ 在 description 中直接加入团队常用触发表述，⭐ 包括中英文
② ⭐ 在 Use When 段列出具体触发场景，给模型更多匹配锚点
③ ⭐ 若竞争技能是根因 → 重新划分两个技能的 description 边界，消除重叠
```

---

## 3. ⭐ 误触发（False Trigger）——危害更大

**表现**：用户意图与技能无关，但技能仍被激活，占用上下文并产生干扰输出。

> ⭐ **误触发的危害比欠触发更大——
> ⭐ 欠触发只是功能缺失，误触发是主动干扰。**

**根因链路**：

```
用户输入 → 匹配 description → 错误匹配 → 加载
                 ↑
        ⭐ description 太宽 或 缺少排除条件
```

**三个根因**：

**① description 太宽**

```
⭐ 用了通用动词：review / analyze / check / validate / improve / optimize
⭐ ⭐ 这些词在日常开发语境中的语义范围，
   ⭐ 远比技能的实际能力范围要大。

❌ "Review and analyze code for quality issues."

会错误触发：
  "帮我分析一下这个 bug 的原因"   → 触发（实际是 debug）
  "看看这个函数的时间复杂度"      → 触发（实际是性能分析）
  "这段代码能跑吗"                → 触发（实际是运行验证）
  "review 一下这个设计文档"        → 触发（实际是文档，不是代码）
```

**② 关键词与不相关任务重叠** —— 这些高频动词出现在大量任务中，
一个技能用了它们就意味着**在与所有含这些动词的请求竞争**。

**③ ⭐ 缺少 "Do Not Use When" 段**

```
⭐ Do Not Use When 不是可选项——⭐ 它是控制误触发的主要手段。
⭐ ⭐ 没有这段的技能，误触发率通常高出 2–3 倍。
```

> ⭐ 而且排除条件必须具体：
>
> ❌ `"User asks about something else"` —— 泛泛的排除没用，模型不理解"something else"
> ⭐ ✅ **每一条排除条件都应对应一类真实的误触发 case**

---

## 4. ⭐ 执行失败（Execution Failure）——最隐蔽

**表现**：技能正确触发，但输出质量不达标——漏步骤、格式错、幻觉、范围失控。

> ⭐ **这类最隐蔽，因为触发本身成功了，
> ⭐ 给人一种"技能在工作"的错觉。**

**根因链路**：

```
技能加载 → 读 Steps/Resources → 执行 → 输出质量差
                    ↑
        ⭐ 步骤模糊 / 资源缺失 / 格式未定义
```

**四个根因**：

**① 步骤太模糊**

```
⭐ "Review the code" 不是可执行步骤，它是一个意图描述。

❌ steps:
     - "Review the code for issues"
     - "Check if there are tests"
     - "Provide feedback"

✅ steps:
     - "Read the current diff using git diff HEAD~1"
     - "For each changed file, classify: behavior change | refactor | test | config"
     - "For behavior changes, identify: side effects, error handling, edge cases"
     - "Check if changed code has corresponding test coverage"
     - "Output findings as: [CRITICAL|WARN|INFO] file:line — description"
```

> ⭐ **步骤越模糊，执行结果的方差越大。**
> 这与 `instruction-craft.md` 的"祈使句 + 钉死格式"是同一条。

**② 资源路径错误或缺失**

```
⭐ 技能引用了不存在的模板文件 → 模型读取失败后可能跳过该步骤，
⭐ ⭐ 或者用自己生成的内容替代——这就是幻觉的来源之一。
```

> ⭐ 这条解释了"幻觉"的一个常被忽略的成因：**不是模型编造，
> 是它找不到文件后自己补了一个。**

**③ 输出格式未定义** —— 不知道该输出 list / table / 结构化报告，
于是每次结构都不同。

**④ ⭐ 隐式上下文依赖**

```
⭐ 技能假设了当前工作目录、分支状态或文件结构，但没有显式说明。

例：步骤写 git diff HEAD~1，
    ⭐ 但没考虑 detached HEAD 状态或刚初始化的仓库。
```

> ⭐ **这类假设在开发者本地往往成立，
> ⭐ 但在其他成员的环境或 CI 中可能不成立。**
> 与 `preflight-gate.md` 的 STEP 0 前置门禁是同一件事的两面。

---

## 5. ⭐ 15 条评测集

每个技能构建如下测试集：

```
正例   —— 验证召回率（该触发吗）
⭐ 反例 —— 验证精确率（不该触发吗）
边界例 —— 标定灰色地带的决策边界
```

**构建原则**（两条，都有反直觉之处）：

```
⭐ ① 用团队真实会使用的措辞，⭐ 而不是测试者自己造的措辞
   ⭐ 最好的来源是会话历史——把过去一周的真实请求拿过来，分类标注

⭐ ② 关键不是边界例必须触发或不触发，
   ⭐ 而是⭐ 每次迭代的决策要一致
```

> ⭐ 第 ② 条很重要：**边界例的作用是"决策一致性锚点"，
> 不是"必须答对"**。它测的是你的改动有没有让行为漂移。

**扩展判据**：如果某条边界例（如"依赖升级安全审查"）触发了且输出质量合格，
就可以把它纳入技能的能力范围——**评测集会自然告诉你技能的边界在哪**。

**迭代节奏**：用 15 条评测集量化触发精度，用评分表量化输出质量，
**迭代三轮再上线**。

---

## 速查

```
前提：
□ ⭐ 触发是概率行为，不是精确匹配
□ 没评测就没基线，没基线就无法迭代

欠触发（根因在 description 太窄）：
□ ⭐ 覆盖用户自然语言，不只写技术术语
□ ⭐ 中文团队要写中文触发词（语义距离问题）
□ ⭐ 检查竞争技能是否更宽泛
□ 修：加覆盖性表述 / Use When 段 / 重划边界

⭐ 误触发（危害更大，是主动干扰）：
□ ⭐ 慎用 review/analyze/check/validate/improve/optimize
□ ⭐ 必须有 Do Not Use When
□ ⭐ 排除条件要对应真实误触发 case，不写 "something else"
□ ⭐ 缺这段 → 误触发率高 2–3 倍

⭐ 执行失败（最隐蔽，触发成功给了假象）：
□ ⭐ 步骤要可执行（含命令、维度、输出格式）
□ ⭐ 引用不存在的文件 → 模型自己补内容 = 幻觉来源之一
□ 输出格式必须定义
□ ⭐ 隐式上下文依赖（detached HEAD 等）要显式说明

15 条评测集：
□ 正例测召回 / ⭐ 反例测精确 / 边界例测一致性
□ ⭐ 用真实措辞，来源取会话历史
□ ⭐ 边界例看决策是否一致，不是必须答对
□ 迭代三轮再上线
```

**一句话**：

> ⭐ **欠触发只是功能缺失，误触发是主动干扰——
> 所以 Do Not Use When 不是可选项。**
