# 谁能调用：两个 frontmatter 字段

> 相关：《skill-structuring》的 `frontmatter.md` ·
> `argument-substitution.md` · 《skill-governance》的 `skill-invocation-control.md`
> 前置：`skill-invocation-control.md` 讲权限规则层，
> 这份只讲⭐ 作者侧的两个声明字段。

---

## 目录

- [1. 默认行为](#1-默认行为)
- [2. ⭐ disable-model-invocation：只有你能调](#2--disable-model-invocation只有你能调)
- [3. ⭐ user-invocable: false：只有模型能调](#3--user-invocable-false只有模型能调)
- [4. ⭐ 与参数技能的搭配](#4--与参数技能的搭配)
- [5. 选型判据](#5-选型判据)

---

## 1. 默认行为

```
⭐ 默认情况下，你和模型都能调用任何技能。

· 你：输入 /skill-name 直接调用
· 模型：判断相关时自动加载
```

两个字段用来打破这个默认。

---

## 2. ⭐ disable-model-invocation：只有你能调

```yaml
disable-model-invocation: true
```

**适用场景**：

```
⭐ 有副作用的操作
⭐ 或者你想自己掌控时机的操作

典型：/commit · /deploy · /send-slack-message
```

> ⭐ 官方给的理由很直白：
> **你不希望模型因为"你的代码看起来准备好了"就决定去部署。**

> ⭐ 这与 `budget-truncation.md` 那条呼应——设了它还能把该技能的
> description **从元数据预算里移除**，等于**既更安全又省预算**，双重收益。

---

## 3. ⭐ user-invocable: false：只有模型能调

```yaml
user-invocable: false
```

**适用场景**：

```
⭐ 作为背景知识、但本身不构成一个"动作"的技能
```

典型例子：`legacy-system-context` —— 解释某个老系统如何工作。

> ⭐ 判据很精彩：**模型在相关时应该知道这些知识，
> 但 `/legacy-system-context` 对用户来说不是一个有意义的动作。**
> 用户不会想"帮我执行一下背景知识"。

---

## 4. ⭐ 与参数技能的搭配

```
⭐ 带参数的技能（/component SearchBar form）通常要设
   disable-model-invocation: true
```

原因很实在：

```
模型不知道该填什么参数。
它自动触发一个需要 $name / $type 的技能，只能去猜——
⭐ 猜出来的参数会被静默填进去。
```

> ⭐ 所以经验法则是：**有必填参数 = 人来调**，除非参数有可靠默认值。

---

## 5. 选型判据

```
问：这个技能是一个"动作"吗？
    ├ 否（是背景知识）→ user-invocable: false
    └ 是 ↓
问：这个动作有副作用吗？
    ├ 有（部署/发送/提交）→ disable-model-invocation: true
    └ 无 ↓
问：需要人填参数吗？
    ├ 需要 → disable-model-invocation: true
    └ 不需要 → 保持默认（两边都能调）
```

> ⭐ 这张决策树把两个字段从"记得配一下"变成了"按问题走一遍"。

---

## 速查

```
默认：你和模型都能调

□ ⭐ 有副作用 / 想自己掌控时机 → disable-model-invocation: true
    （commit / deploy / send-slack-message）
□ ⭐ 只是背景知识、不构成动作 → user-invocable: false
    （legacy-system-context）
□ ⭐ 带必填参数的技能 → 通常也要 disable-model-invocation
    （否则模型只能猜参数，猜错还静默）
□ ⭐ 前者还额外省掉 description 的元数据预算

判据顺序：
□ 是不是一个"动作"？否 → user-invocable: false
□ 有副作用吗？有 → disable-model-invocation: true
□ 需要人填参数吗？需要 → disable-model-invocation: true
```

**一句话**：

> ⭐ **用户不会想"帮我执行一下背景知识"，
> 而你不希望模型因为"代码看起来准备好了"就去部署。**
