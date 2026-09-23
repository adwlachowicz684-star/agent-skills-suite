# 调用控制：用权限规则限定哪些技能可被用

> 相关：`runtime-controls.md`（frontmatter 开关：`disable-model-invocation` / `user-invocable`）
> 这份讲**权限规则层**——不改技能文件，从外部控制谁能调什么。
> 相关：《skill-crafting》的 `skill-structuring` 的 `frontmatter-fields.md`（`allowed-tools` 字段）

---

## 目录

- [1. 三层控制，各管一段](#1-三层控制各管一段)
- [2. 语法：精确匹配与前缀匹配](#2-语法精确匹配与前缀匹配)
- [3. 三种用法](#3-三种用法)
- [4. ⭐ allowed-tools 的授权时效](#4--allowed-tools-的授权时效)
- [5. 内置命令的边界](#5-内置命令的边界)
- [6. 选型建议](#6-选型建议)

---

## 1. 三层控制，各管一段

| 层 | 位置 | 控制什么 | 谁改 |
|---|---|---|---|
| frontmatter 开关 | 技能文件内 | 模型能否自动调用 / 用户能否手动调用 | 技能作者 |
| ⭐ **权限规则** | 外部 settings/permissions | ⭐ **具体的允许/拒绝** | 用户 / 管理员 |
| `allowed-tools` | 技能文件内 | 调用期间免确认哪些工具 | 技能作者 |

> 三者不是替代关系：
> frontmatter 是**作者声明意图**，权限规则是**执行侧强制**。
> ⭐ **权限规则的优先级高于技能自己的声明。**

---

## 2. 语法：精确匹配与前缀匹配

```
Skill(name)        精确匹配 —— 只匹配这个名字
Skill(name *)      前缀匹配 —— 匹配以 name 开头、带任意参数
```

`*` 在这里是**参数通配符**，不是名字通配：

```
Skill(review-pr *)   ✅ 匹配 review-pr 后接任何参数
Skill(review*)       ❌ 不是"匹配所有 review 开头的技能"
```

---

## 3. 三种用法

### ① 全局禁用所有技能

在 `/permissions` 的 **deny** 规则里加：

```
Skill
```

单独一个 `Skill` = 拒绝整个技能工具。

### ② 白名单：只允许指定的几个

```
Skill(commit)
Skill(review-pr *)
```

> ⭐ **这是收紧的正确姿势**——默认全开，显式列出允许的。

### ③ 黑名单：禁止特定的几个

```
Skill(deploy *)
```

**命名约定在这里直接变成安全资产**：
如果你把生产部署类技能统一命名为 `deploy-*` 前缀，
**一条规则就能拒掉整类危险操作**。

---

## 4. ⭐ allowed-tools 的授权时效

这是最容易被误解的一条：

> 定义了 `allowed-tools` 的技能，会在**调用它的那一轮**内
> 授予 Claude 免逐次确认使用这些工具的权限。
>
> ⭐ **这个授权在你发送下一条消息时清除。**

两点含义：

1. **它不是"永久授权"**——只覆盖那一轮，粒度很细，这是好事
2. **它不是安全边界**——见 `least-privilege.md`：
   真正的访问控制主要是**工具设计**问题，不是声明问题。
   你的基础权限设置仍然管辖所有其他工具的审批行为。

---

## 5. 内置命令的边界

有一批内置命令也能通过 Skill 工具调用，但**不是全部**：

```
✅ 可调用：/init · /security-review
❌ 不可调用：/compact 等
```

> 也就是说——**不要假设"斜杠命令都能用权限规则管"**，
> 只有走 Skill 工具的那一批才受 `Skill(...)` 规则约束。

---

## 6. 选型建议

| 你的目的 | 用哪层 |
|---|---|
| 某个技能只能我手动触发、别自动用 | frontmatter `disable-model-invocation: true` |
| 禁止整个团队用某一类技能 | ⭐ 权限规则 deny + 命名前缀 |
| 只允许新成员用安全的几个 | ⭐ 权限规则白名单 |
| 调用时不想被反复询问工具确认 | `allowed-tools`（仅该轮有效） |
| 防止危险操作真的执行 | ⭐ 都不够——需要 `approval-gates.md` 的人工批准门 |

> ⚠️ **权限规则能阻止"谁可以调用"，但阻止不了"被调用后做什么"。**
> 后者要靠工具层的最小权限（见 `least-privilege.md`）和批准门（见 `approval-gates.md`）。

---

## 速查

| 需求 | 写法 |
|---|---|
| 全禁 | deny: `Skill` |
| 只允许某技能 | allow: `Skill(commit)` |
| 允许某技能带参数 | allow: `Skill(review-pr *)` |
| 禁用一类 | deny: `Skill(deploy *)` |
| 只让我手动触发 | frontmatter `disable-model-invocation: true` |
| 该轮免确认工具 | frontmatter `allowed-tools`（下条消息即失效） |
