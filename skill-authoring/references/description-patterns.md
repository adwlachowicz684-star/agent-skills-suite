# description 写法：四种模式与三个致命错误

> ⭐ **description 是唯一的路由依据。**
> 正文在被触发之后才加载——所以"什么时候用"写在正文里等于没写。

## 目录

- [一条铁律](#一条铁律)
- [三种可抄的模式](#三种可抄的模式)
- [三种致命错误](#三种致命错误)
- [四条写法原则](#四条写法原则)
- [中间地带：太宽与太窄](#中间地带太宽与太窄)
- [一个自检](#一个自检)

## 一条铁律

> ⭐ **永远不要把 "when to use" 放进正文。**

正文在 description 触发**之后**才加载。
触发上下文必须**就在 description 字段里**。

这条被违反得极频繁——
很多人把触发条件写在正文第一段的"适用场景"里，
然后困惑为什么技能从不自动触发。

## 三种可抄的模式

**① 任务 + 关键词**

```yaml
description: >
  Standardize Terraform plan diff reviews.
  Use for Terraform, plan, diff, infrastructure review,
  IAM, network, cost topics.
```

**② 问题 + 解法**

```yaml
description: >
  Fix failing CI builds by analyzing logs and suggesting fixes.
  Use for CI, build failure, GitHub Actions, pipeline debug.
```

**③ 领域 + 动作**

```yaml
description: >
  Generate release notes from git history.
  Use for release, changelog, version, git log, notes.
```

三种模式共同点：**先说干什么，再显式列触发词**。

## 三种致命错误

**① 太模糊——匹配不上具体请求**

```yaml
❌ "Helps with infrastructure reviews."
❌ "一个处理文档的有用技能"
```

> 没有任何具体动作，也没有任何触发词。
> **模型无法据此路由。**

**② 缺触发词——看起来很专业但匹配不上**

```yaml
❌ "A comprehensive solution for code analysis."
```

"comprehensive solution" 不是任何人会说的话。

**③ ⭐ 太长——把关键词埋掉了**

```yaml
❌ "This skill provides a complete end-to-end solution for
    reviewing and analyzing infrastructure-as-code changes
    including but not limited to Terraform, Pulumi, and
    CloudFormation templates with a focus on security best
    practices and cost optimization strategies."
```

关键词散落在长句里，语义匹配被稀释。

> ⭐ **长 description 还有第二重代价**：
> 装了很多技能时，**描述会被压缩以省字符预算**，
> 可能把你精心写的触发词削掉。

## 四条写法原则

```
① ⭐ 关键词前置
   最重要的词放在第一句

② ⭐ 显式写 "Use for X, Y, Z"
   别指望模型自己推断出触发词

③ ⭐ 匹配用户词汇，不是内部术语
   用用户真的会打出来的词

④ 控制在合理长度
   ——别为了短而牺牲关键词，也别为了全而写成长文
```

第 ③ 条最容易被违反：
团队内部叫"工单"，用户说"问题单"；
内部叫"灰度"，用户说"先给几个人试试"。

## 中间地带：太宽与太窄

两个极端都致命，且**同样常见**：

**太宽**

```
"helps with coding tasks"
→ 与每一个编码技能竞争
→ ⭐ 赢不了任何一场竞争
→ agent 降低它的优先级，因为它对任何具体查询都不是最佳匹配
```

**太窄**

```
"generates TypeScript interfaces from OpenAPI 3.1 YAML specifications"
→ 只对这一句话触发
→ 说 "make types from my API spec" 或
   "convert this swagger file to TypeScript" 的用户全部错过
```

✅ 目标：**能覆盖约 80% 的人会用来描述这个技能的方式。**

一个实用的写法骨架（2–5 句，覆盖三类触发）：

```
① 显式触发：这个技能做什么
② 隐式触发：它解决什么问题
③ 情境触发：什么上下文暗示它相关
```

## 一个自检

写完 description，问四个问题：

```
① 读回来：模型会知道什么时候该触发它吗？
② ⭐ 我用同事的原话测过吗？
   ——手动测试用的是"你写 description 时的那套措辞"，当然会匹配
③ 它和谁抢同一批触发词？能区分开吗？
④ 关键词在前半部分吗？（被截断时还能剩什么）
```

第 ② 条展开：**请一个没读过你 description 的同事描述他想要什么，
然后用他的原话测。** 这是唯一能发现"词汇鸿沟"的方法。

第 ④ 条也值得单独说：
既然描述可能被压缩截断，
**把最关键的触发词放在前面就不只是风格问题，是可靠性问题。**

## 几条硬约束（别踩）

```
name        ≤ 64 字符，小写字母/数字/连字符
            不能以连字符开头或结尾，不能有连续连字符
            ⭐ 必须与父目录名完全一致

description ≤ 1024 字符，非空，无 XML 标签
            ⭐ 第三人称（"Processes Excel files"，不是 "I can help"）

保留字      name 里不能含 "anthropic" / "claude"
```

违反时的表现：

```
name 超长 / description 超长 / 含保留字 → ⭐ 加载时被拒（静默）
第一人称描述                          → 能用，但触发正确率下降
```

## 排错速查

| 症状 | 原因 | 修法 |
|---|---|---|
| 从不触发 | 描述与用户语言不匹配 | 用真实用户的措辞重写 |
| 对错误请求触发 | 太宽，无否定触发 | 收窄作用域，加显式排除 |
| ⭐ 间歇性触发 | 与另一技能冲突 | 检查可组合性，消除歧义 |
| 触发了但输出错 | **指令**含糊（不是描述问题） | 加具体示例与预期输出格式 |
| ⭐ 测试通过但生产不灵 | 测试措辞是作者的词汇 | 用非作者的不同说法测 |
| 无法判断是否触发 | 没有可观测性 | 装监控，看真实触发率 |
