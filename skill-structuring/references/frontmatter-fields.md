# Frontmatter 字段速查

> 一份能对着填的字段表。
> ⭐ 含"哪些字段会被静默忽略"——这是最容易踩的坑。

## 目录

- [必填字段](#必填字段)
- [常用可选字段](#常用可选字段)
- [执行类字段](#执行类字段)
- [⭐ 各平台解析差异](#-各平台解析差异)
- [YAML 语法陷阱](#yaml-语法陷阱)
- [完整示例](#完整示例)

## 必填字段

| 字段 | 约束 | 说明 |
|---|---|---|
| **`name`** | ≤64 字符，小写/数字/连字符 | ⭐ 唯一标识，**必须与目录名一致** |
| **`description`** | ≤1024 字符，非空，无 XML 标签 | ⭐ **唯一的路由依据** |

其他都可选。

> ⭐ **只有这两个是规范要求的**。
> 其余字段是否被解析，取决于运行时（见下节）。

## 常用可选字段

| 字段 | 用途 | 成本 |
|---|---|---|
| `license` | 许可证信息或引用 | 5–20 tokens |
| `metadata` | 任意键值对（author / version / 等） | 可变 |
| `allowed-tools` | ⭐ 免确认工具列表 | — |
| `version` | 版本号 | — |

## 执行类字段

有些字段控制**技能怎么被执行**（支持程度因平台而异）：

```
disable-model-invocation   禁用模型自动触发，只能人显式调用
context: fork              在隔离子代理里跑（见 fork-context-skill.md）
agent:                     指定子代理类型
```

> ⭐ 这些字段**决定了技能是"在主会话里跑"还是"在独立上下文里跑"**，
> 写错会让整个隔离设计失效。

## ⭐ 各平台解析差异

> **这是本节最重要的部分。**

`allowed-tools` 的真相：

```
⭐ 它是"免确认"字段，不是"限制"字段
   ——只有部分运行时解析它
```

两个后果：

```
① ⭐ 不要把安全逻辑放在可能被静默剥离的字段里
   安全控制必须在工具层做（见 least-privilege.md）

② 要真正移除工具，得看运行时是否支持
   disallowed-tools 之类的对应字段
```

通用原则：

> ⭐ **规范只保证 `name` 和 `description` 被解析。**
> 任何依赖其他字段生效的设计，都要在目标平台上实测。

## YAML 语法陷阱

按遇到频率排序：

**① `---` 必须顶格**

```
❌ 前置有空行或空格
✅ 第一行就是 ---
```

**② 引号未闭合**

```yaml
❌ description: "这是一个未闭合的描述
✅ description: "这是一个正常的描述"
```

**③ tab 与空格混用**

> YAML 不允许 tab 缩进。混用会直接解析失败。

**④ 多行描述用了错误的折叠语法**

```yaml
# 折叠标量（换行变空格）
description: >
  第一行
  第二行

# 保留换行
description: |
  第一行
  第二行
```

⚠️ 常见故障：**用 `|` 写了很长的内容导致超过 1024 字符被拒**。
超过限制时错误往往不直观。

**⑤ 字段名里的 Unicode 字符**

```
❌ 用了全角冒号或中文键名
   某些解析器会直接失败
```

**⑥ description 为空**

```
⭐ 空的 description = agent 没有东西可以匹配
   这是"技能从不触发"最常见的原因之一
```

## 完整示例

```yaml
---
name: review-pr
description: >
  Review pull requests for correctness, security, conventions,
  and test coverage. Use when reviewing a PR, checking a diff,
  or asked "is this ready to merge".
license: MIT
metadata:
  author: platform-team
  version: 2.1.0
allowed-tools: Bash(gh *) Read Grep Glob
disable-model-invocation: true
context: fork
agent: Explore
---
```

注意这个例子里：

```
□ description 用 > 折叠，避免超出 1024 字符
□ ⭐ 触发词含用户原话 "is this ready to merge"
□ allowed-tools 只给了只读工具
□ ⭐ 执行类字段组合使用（fork + Explore = 隔离且只读）
```

## 自查

```
[ ] name 与目录名一致，且符合字符集与长度？
[ ] description ≤1024 字符、非空、含触发词？
[ ] --- 顶格？
[ ] 引号闭合？无 tab？
[ ] ⭐ 键名全是 ASCII？
[ ] ⭐ 依赖的可选字段，在目标平台上实测过吗？
[ ] ⭐ 没有把安全逻辑寄托在 allowed-tools 上？
```

## 一条提醒

> 校验器能抓结构问题，**抓不了"字段没生效"**。

所以：**改完 frontmatter 之后要重载并让模型复述一遍**
（见 `reload-debug.md`）——
结构合法 ≠ 生效了。
