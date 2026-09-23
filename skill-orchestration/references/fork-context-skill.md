# Fork 上下文技能：把重活隔离出去

> 有些技能天生该跑在**独立子代理**里——
> 大 diff、长日志、需要只读保证的任务。

## 目录

- [什么时候用 fork](#什么时候用-fork)
- [怎么配](#怎么配)
- [动态注入](#动态注入)
- [会发生什么](#会发生什么)
- [四个常见故障](#四个常见故障)
- [Explore vs general-purpose](#explore-vs-general-purpose)

## 什么时候用 fork

```
✅ 产出冗长但主上下文不需要
✅ ⭐ 想强制只读（分析而不行动）
✅ 工作自包含，能返回摘要
❌ 需要频繁来回打磨（→ 主会话）
❌ 延迟敏感（子代理要从零收集上下文）
```

典型场景：**PR 评审**——完整 diff 可能几万行，
但你只需要一份带 severity 和 file:line 的报告。

## 怎么配

```yaml
---
name: review-pr
description: ...
disable-model-invocation: true      # 只能被显式调用
context: fork                        # ⭐ 在隔离子代理里跑
agent: Explore                       # 只读 agent 类型
allowed-tools: Bash(gh *) Read Grep Glob
---
```

关键字段：

```
context: fork              技能内容成为子代理的 prompt，
                           ⭐ 子代理获得自己的上下文窗口

disable-model-invocation   禁用模型自动触发，
                           只能人显式调用 /review-pr

agent:                     指定子代理类型
allowed-tools:             ⭐ 工具白名单（这里是只读工具）
```

## 动态注入

在正文里用 `` !`命令` `` 语法：

```markdown
## Pull Request Context

- PR title and description: !`gh pr view --json title,body --jq '"\(.title)\n\n\(.body)"'`
- Changed files: !`gh pr diff --name-only`
- Full diff: !`gh pr diff`
```

> ⭐ **模型看到指令时，diff 已经内联进去了——
> 它看到的不是这条命令，而是命令的输出。**

这个区别很重要：**技能里写的是"要执行什么来取得上下文"，
而不是"上下文是什么"**——所以每次调用都是新鲜的。

## 会发生什么

调用 `/review-pr` 时：

```
① 创建 fork 上下文（全新的上下文窗口）
② ⭐ !` ` 块先执行，把 PR 数据注入
③ Explore 子代理收到渲染后的技能内容作为 prompt
④ 子代理读 diff、分析、生成评审
⑤ 结果被摘要后返回主会话
⑥ ⭐ 子代理上下文被丢弃
```

> ⭐ 最后两条是关键：**完整 PR diff 从不进入你的主上下文**，
> 对话保持干净，重活由子代理扛。

## 四个常见故障

**① `gh` 未认证**

```
症状：gh pr diff 失败
原因：gh auth status 未通过
⭐ 注意：Claude 不能替你认证
```

**② 漏文件**

```
症状：评审漏掉了一些改动
原因：⭐ PR 有 50+ 文件时，diff 可能超出子代理上下文窗口
修法：加 | head -2000 限制，或分批评审
```

> 这条揭示了一个普遍问题：**"上下文够大"不等于"不会超"**。
> 大输入要先做截断或分批，不能指望窗口无限。

**③ 子代理返回空**

```
症状：什么都没输出
原因：⭐ context: fork 需要显式任务指令
       如果正文只有指南而没有明确任务（"审查这个 diff"），
       子代理可能什么都不产出
修法：正文里必须有明确的 "Review Instructions" 任务段落
```

**④ 评审不符合项目约定**

```
症状：评审意见与团队习惯不符
原因：子代理会同时加载 CLAUDE.md 与技能内容
修法：⭐ 把编码约定写进项目 CLAUDE.md，评审就会参照它们
```

## Explore vs general-purpose

| | `Explore` | `general-purpose` |
|---|---|---|
| 工具 | ⭐ **只读** | 可写 |
| 能改文件/提交/推送 | ❌ | ✅ |
| 适合 | ⭐ 代码评审——你要的是分析，不是行动 | 需要应用修复时 |

> ⭐ **Explore 的只读是特性，不是限制**——
> 评审场景里你明确**不希望**它顺手改东西。

如果确实需要 reviewer 也应用修复，改用 `general-purpose`，
但**要对自动修改保持警惕**（见 `approval-gates.md`）。

## 与"用子代理还是技能"的关系

```
要隔离（大输入/只读保证/不污染主上下文）→ ⭐ fork 的技能
要复用 + 留在主上下文                  → 普通技能
```

fork 技能其实是**两者的组合**：
技能提供可复用的指令，fork 提供隔离。

## 一条提醒

`context: fork` 的子代理**仍然会加载 CLAUDE.md**（除非是 Explore/Plan，
它们跳过——见 `subagent-advanced.md`）。
所以项目级约定会自动生效，
**你不需要在技能里重复 CLAUDE.md 已有的内容**。
