# 参数替换：让一个技能当多个用

> 相关：《skill-structuring》的 `frontmatter.md` ·
> 《skill-crafting》的 `preflight-gate.md`
> 前置：本技能其余文档讲静态结构，这份只讲运行时参数替换机制。

---

## 目录

- [1. 四种占位符](#1-四种占位符)
- [2. ⭐ 0-based：最经典的踩坑](#2--0-based最经典的踩坑)
- [3. ⭐⭐ 会损坏代码的陷阱](#3--会损坏代码的陷阱)
- [4. 命名参数与提示](#4-命名参数与提示)
- [5. 参数对不上时的行为](#5-参数对不上时的行为)
- [6. 转义](#6-转义)

---

## 1. 四种占位符

```
$ARGUMENTS          命令后你输入的全部内容
$ARGUMENTS[0] / $0  第一个参数
$ARGUMENTS[1] / $1  第二个参数
$name               在 frontmatter 里声明过的具名参数
```

**单参数用法**：

```markdown
---
name: summarize-file
description: Summarizes a document in 5 bullet points.
argument-hint: "[file-path]"
---

Read $ARGUMENTS and summarize it in 5 bullet points.
```

> `/summarize-file notes/meeting.md`
> → 模型读到 "Read notes/meeting.md and summarize it"

**多参数用法**：

```markdown
Migrate the $0 component from $1 to $2.
```

> `/migrate-component SearchBar JavaScript TypeScript`
> → `$0 = SearchBar`、`$1 = JavaScript`、`$2 = TypeScript`

**含空格的值要加引号**：

```
/draft-email "Acme Supplies" overdue
   → $0 = Acme Supplies、$1 = overdue
不加引号 → $0 只是 "Acme"
```

> ⭐ 索引用 shell 风格的引号规则，多词值必须包起来才算一个参数。

---

## 2. ⭐ 0-based：最经典的踩坑

```
⭐ $0 是第一个参数，不是 $1。
```

> ⭐ **想拿第一个参数要写 `$0`，写成 `$1` 是经典失误。**
> `$ARGUMENTS[0]` 与 `$0` 等价，只是写法更长。

---

## 3. ⭐⭐ 会损坏代码的陷阱

> ⭐ **参数替换在加载时执行——模型读到之前就已经替换完了。**

这意味着：**正文里任何长得像 `$1` / `${1}` / `$ARGUMENTS` 的文本都会被替换。**

| 场景 | 后果 |
|---|---|
| bash 函数 `local path=$1` | ⭐ 有参数时被换成 CANARY_A，**代码损坏**；无参数时被替换成空 |
| 花括号形式 `${1}` | ⭐ **同样不安全**，一样被替换 |
| awk `'{print $5, $1}'` | ⭐ **单引号也不提供保护**，字段引用也被替换 |

> ⭐ **这是静默的**——没有报错，只是技能正文里的 shell 示例变成了一串垃圾，
> 而模型会照着这段损坏的示例执行。

**正确写法（三条）**：

```
① ⭐ 所有含 $N 的代码示例，移到 references/*.md
   ——⭐ reference 文件不参与替换，能安全显示字面量 $1
② 在 SKILL.md 顶部用 XML 标签捕获参数，之后一律用捕获后的标签，不再用裸 $N
③ 纯散文与输出字符串里可直接使用替换
```

> ⭐ 第 ① 条是这一段最该记住的：**会过时的、含 shell 变量的代码示例，
> 本来就属于 references，这条陷阱只是给了它第二个理由。**

---

## 4. 命名参数与提示

三个以上参数时数字会难读，改用命名：

```markdown
---
name: draft-email
arguments: [client, reason]
argument-hint: "[client] [reason]"
---

Draft a short follow-up email to $client about $reason.
```

> ⭐ **名字按位置对应**：`$client` 是第一个，`$reason` 是第二个。
> `arguments: client reason`（不带括号）同样有效。

**`argument-hint` 的作用边界**：

```
⭐ 它不改变技能如何运行
⭐ 只在菜单里显示该输入什么
——让你或同事不必打开文件就能想起参数格式
```

> ⭐ 这是个低成本高收益的字段：**团队里别人第一次用你的技能时，
> 有没有 hint 的差别就是"要不要先去读文件"。**

---

## 5. 参数对不上时的行为

| 情况 | 结果 |
|---|---|
| 技能里根本没有占位符 | ⭐ 自动在末尾追加 `ARGUMENTS: 你的输入` |
| 写了 `$2` 但只传了 2 个参数 | ⭐ `$2` **原样保留为字面文本** |
| 具名参数没传值 | 展开为空字符串 |
| 传入的值本身含 `$1` | ⭐ 当作字面文本，**不会被二次展开** |

> ⭐ 第二行最容易咬人：**模型看到一个孤零零的 `$2`，可能会去猜它是什么。**
> 这也解释了为什么"参数个数可能不足"的技能必须写兜底说明。

---

## 6. 转义

```
⭐ 想在散文里写 $1.00 这样的字面量 → 用反斜杠转义：\$1.00
```

三条边界：

```
· ⭐ 只有紧贴 token 的单个反斜杠才起转义作用
· \\$1 会保留两个反斜杠，且 $1 仍会被展开
· ⭐ 反斜杠不能阻止 ${CLAUDE_*} 变量的替换——那些照常替换
```

> ⭐ 最后一条很实用：**`${CLAUDE_SKILL_DIR}`、`${CLAUDE_SESSION_ID}` 这类
> 内置变量在参数插入之后仍然会被替换**，可以用来做按会话隔离的输出路径。

---

## 速查

```
□ ⭐ $0 是第一个参数（不是 $1）
□ 多词值加引号
□ ⭐⭐ 含 $N 的代码示例必须移进 references/（正文会被替换、静默损坏）
□ ⭐ 花括号 ${1} 与单引号 awk 都不安全
□ 3 个以上参数用命名参数
□ argument-hint 只影响菜单显示
□ ⭐ 参数不足时 $N 会原样留下，模型可能去猜 → 要写兜底
□ ⭐ 字面 $ 用反斜杠转义，但挡不住 ${CLAUDE_*}
□ ${CLAUDE_SKILL_DIR} / ${CLAUDE_SESSION_ID} 仍会替换
```

**一句话**：

> ⭐⭐ **参数替换发生在模型看到内容之前——
> 所以你写在正文里的 shell 示例，会在模型读到时就已经被改坏了。**
