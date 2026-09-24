# 九项排查：技能不工作时的顺序检查

> 相关：《skill-structuring》的 `frontmatter-pitfalls.md` ·
> `loading-mechanics.md` · 《skill-evaluating》的 `troubleshooting-manual.md`
> 前置：那些文档讲"为什么"，这份给一份⭐ 按顺序执行的实操清单。

---

## 目录

- [1. 九项检查](#1-九项检查)
- [2. ⭐ 第 4 项：description 是头号原因](#2--第-4-项description-是头号原因)
- [3. ⭐ 显式调用这个隔离技巧](#3--显式调用这个隔离技巧)
- [4. 兜底：从已知可用的模板重建](#4-兜底从已知可用的模板重建)

---

## 1. 九项检查

> ⭐ **按顺序走，前几项能解决大多数情况。**

**① 检查文件名与目录布局**

```
⭐ 文件必须叫 SKILL.md —— 全大写，一字不差
   ❌ skill.md · ❌ Skill.MD · ❌ SKILLS.md

⭐ 且必须在自己的命名目录里：

✅ ~/.claude/skills/excel-reports/SKILL.md
❌ ~/.claude/skills/SKILL.md     ← 散落文件，被忽略
```

**② 确认用对了目录**

```
~/.claude/skills/     —— 个人技能，每个项目可用
.claude/skills/       —— 项目技能，随仓库提交
```

> ⭐ **混用这两个是最常见的路径错误。**
> 若把技能放在项目目录但从别的目录运行，就找不到。
> 且**项目技能只对该项目生效**。

**③ 重启会话**

```
⭐ 技能在会话开始时被扫描。
⭐ 会话中途新增或编辑的技能，模型还没看见。
```

> ⚠️ 与 `trigger-fix-nine-causes.md` 那条"改了技能不用重启"有出入
> （那份说有实时变更检测）。
> ⭐ **仲裁**：实时检测能发现**新增**的技能；
> ⭐ 但对**已加载会话中的修改**仍需重启——**保守做法是重启**，
> 因为重启永远有效，而"以为生效其实没生效"的排查成本高得多。

**④ 修 description —— ⭐ 头号原因**（见下节）

**⑤ 保持 frontmatter 合法**

```
· 开头结尾的 --- 行
· 合法键名
· ⭐ 不能有游离的 tab
· ⭐ 未加引号的值里避免未转义的尖括号和冒号
· ⭐ description 控制在长度限制内（超出会被截断）

⭐ ⭐ frontmatter 坏了 = 整个技能被静默跳过
```

**⑥ 确认技能已启用**

```
Claude Desktop：检查设置/权限里该功能与具体技能是否开启
Claude Code：   ⭐ 检查是否处于受限权限模式
               ⭐ 检查 frontmatter 是否设了 disable-model-invocation
                  （设了就不会自动触发）
```

**⑦ 清除权限 / 临时目录阻塞**

```
⭐ 若技能跑打包脚本失败，常见原因是工作目录或临时目录的文件系统权限
   （例如被锁死的 /tmp）

· 确保能读技能目录
· 确保能写临时目录
· ⭐ 打包文件可读（不是 chmod 000）
```

**⑧ ⭐ 显式调用**（隔离技巧，见下节）

**⑨ 更新版本并查 changelog**

```
⭐ 技能的加载行为在不同版本间变过。
⭐ 旧版本可能不支持当前文档描述的行为方式。
```

---

## 2. ⭐ 第 4 项：description 是头号原因

```
⭐ 若技能能加载但从不触发 —— 问题就是 description。
⭐ ⭐ 模型在决定是否使用之前，只看得到每个技能的名字和描述，
   ⭐ 所以描述必须点名具体场景。
```

**强 vs 弱对照**（这份对照值得直接抄）：

```
❌ 弱（不会触发）
   description: Helps with spreadsheets

✅ 强（稳定触发）
   description: Create formatted .xlsx spreadsheets with formulas
                and charts. Use when the user asks for an Excel file,
                a spreadsheet, or a financial model.
```

**写法三条**：

```
① 说明技能做什么 + 何时用
② ⭐ 用第三人称
③ ⭐ 包含用户实际会打出来的那些词
```

> ⭐ 第 ③ 条与 `activation-rate.md` 的实测完全一致：
> **不是描述得更华丽，而是覆盖真实词汇。**

---

## 3. ⭐ 显式调用这个隔离技巧

```
⭐ 按名字显式调用（如 /excel-reports）

⭐ ⭐ 若显式调用能跑、自动触发不能
   = 技能安装正确，⭐ 要修的是 description（回到第 4 项）
```

> ⭐ 这一步是**最快的一次分诊**：
> 一步就把"文件层/加载层"的故障和"匹配层"的故障分开了。
> 与 `troubleshooting-manual.md` 的"指名调用"判据同源。

---

## 4. 兜底：从已知可用的模板重建

```
⭐ 拿一个已知能用的模板重建技能
⭐ 或照抄一个结构良好的官方技能（如 PDF 技能、MCP Builder）的 frontmatter

⭐ ⭐ 拿不准时，从一个已经能用的东西出发，⭐ 一次只改一处
```

> ⭐ "**一次只改一处**"是这条建议里真正的要点——
> 同时改多处，出问题就分不清是哪个引起的。

---

## 速查

```
□ ① 文件名 SKILL.md 全大写，且在自己目录里
□ ② ~/.claude/skills/ vs .claude/skills/ 别混（最常见路径错）
□ ③ ⭐ 重启会话（保守做法，永远有效）
□ ④ ⭐ description 点名具体场景 + 第三人称 + 用户真实用词（头号原因）
□ ⑤ frontmatter 合法：无 tab、无未转义尖括号/冒号、长度不超限
□ ⑥ 确认已启用，检查 disable-model-invocation
□ ⑦ ⭐ 打包脚本失败先查 /tmp 等目录权限与 chmod 000
□ ⑧ ⭐ 显式调用：能跑=装对了，修 description
□ ⑨ 版本过旧 → 更新并查 changelog

□ ⭐ 兜底：从已知可用模板重建，⭐ 一次只改一处
```

**一句话**：

> ⭐ **显式调用能跑、自动触发不能——
> 那技能就没装错，错的只是 description。**
