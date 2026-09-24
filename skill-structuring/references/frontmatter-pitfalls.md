# Frontmatter 为什么会静默失败：两阶段解析

> 相关：`skill-structuring` 的 `frontmatter-fields.md`（字段规范，对着填）·
> 《skill-description》的 `frontmatter.md`（写法）·
> 《skill-evaluating》的 `troubleshooting-manual.md`（排查顺序）

---

## 目录

- [1. 根因：加载器是两阶段解析](#1-根因加载器是两阶段解析)
- [2. 完整雷区表](#2-完整雷区表)
- [3. 跨平台大小写：只在 CI 阶段暴露](#3-跨平台大小写只在-ci-阶段暴露)
- [4. 编码与编辑器](#4-编码与编辑器)
- [5. 三层防御](#5-三层防御)
- [6. 排查顺序](#6-排查顺序)

---

## 1. 根因：加载器是两阶段解析

这是理解"为什么它不报错"的关键：

```
第一阶段（扫目录）  读文件、注册名字
                    ⭐ 这一步很宽容 —— 只要文件存在就标记 loaded

第二阶段（真调用）  严格 YAML 解析 + 字段校验
                    ⭐ 只有到这一步才真正校验
```

> ⭐ **第一阶段的 "loaded" 只代表文件存在，不代表能跑。**

所以你会在技能列表里看到它，但一到调用就失败——
**日志里往往只有一句 "skill not found"**，没有任何提示指向真正的语法错误。

**这解释了前面反复出现的一条经验**：
改了 frontmatter 字段后必须重启客户端（甚至开新会话），
因为注册发生在启动阶段。见《skill-evaluating》的 `reload-debug.md`。

---

## 2. 完整雷区表

| 雷区 | 错误示例 | 正确示例 |
|---|---|---|
| 文件名 | `skill.md` / `Skill.md` / `SKILLS.md` | ⭐ **`SKILL.md`（全大写）** |
| 路径 | `~/.claude/skills/MySkill/SKILL.md` | `~/.claude/skills/my-skill/SKILL.md`（kebab-case） |
| 缺 `---` | 直接写 `name: foo` | ⭐ **前后各一行 `---`，且 `---` 必须是文件第 0 字节** |
| YAML 缩进 | Tab 缩进 | ⭐ **2 空格** |
| 字段拼写 | `descripton:` | `description:` |
| 字段值类型 | `enabled: yes` | `enabled: true` |
| 嵌套结构 | `tools: [a, b]` | ⭐ **块序列写法**（多数系统要求） |
| 特殊字符 | `name: foo:bar` | ⭐ **需要引号包裹** |
| 字符串未加引号 | `name: Data Analysis` | `name: "Data Analysis"`（部分解析器静默失败） |
| 单值数组 | `tags: data` | `tags: ["data"]` |
| `description` 超长 | 超过 1024 字符 | 部分平台有硬限制 |
| 目录内多个 SKILL.md | 一个目录放多个技能 | ⭐ **一个目录只能有一个**，多技能用多目录 |

> ⭐ **`---` 前不能有空行**：必须是文件的第一个字节。
> 这是从 Word/WPS 或某些编辑器复制内容时最容易引入的问题。

---

## 3. 跨平台大小写：只在 CI 阶段暴露

```
Linux / macOS  文件系统大小写敏感
Windows        默认不敏感
```

后果很具体：

```
开发者本机（macOS/Windows）写 MySkill/SKILL.md → 一切正常
推到 Linux 服务器            → ⭐ 成了完全不同的目录名 → 找不到
```

> ⭐ **本地测试一切正常，CI/CD 阶段才暴露。**

**唯一可靠的防御是规范 + 静态检查**，不能靠"我本地能跑"。

配套规则（已在 `naming-convention.md`）：
**全小写 kebab-case，只用小写字母、数字、单个连字符。**

```
❌ Terraform-Plan（大写）
❌ terraform--plan（连续连字符）
❌ terraform plan（空格）
✅ terraform-plan-review
```

---

## 4. 编码与编辑器

| 要求 | 说明 |
|---|---|
| ⭐ **UTF-8 无 BOM** | GBK 或带 BOM 的 UTF-8 会导致解析失败 |
| ⭐ **不能用 Word / WPS 保存** | 必须用纯文本编辑器（VS Code 右下角可看编码） |
| 换行符 | LF 推荐（跨平台），CRLF 通常可接受 |

**自检动作**：用 VS Code 打开，看右下角编码显示是否为 UTF-8。

---

## 5. 三层防御

不要靠人眼检查——这些错误**不会报有意义的错**。

### L1：从官方模板起手，别手写

最小可用模板（用于隔离问题）：

```yaml
---
name: "test-skill"
description: "Simple test"
---

## Instructions
Say "test skill loaded" when activated.
```

> ⭐ **如果最小技能能加载、复杂的不能，问题在内容，不在环境。**
> 这是最快的二分定位法。

### L2：CI 阶段拦住

```bash
# skill-lint.sh：YAML 语法 + 字段白名单
npx skills-ref validate ./skills/*/
yamllint skills/*/SKILL.md
```

必备断言：

- `name` 存在且与目录名**完全一致**（含大小写）
- `description` 存在且非空
- `---` 在文件第 0 字节
- 无 Tab 缩进
- 文件名为 `SKILL.md`
- 编码为 UTF-8 无 BOM

### L3：写进代码评审 checklist

统一命名规范（kebab-case 全小写）**必须是评审项**，
不能只是"建议"——因为违反它**在本地不会报错**。

---

## 6. 排查顺序

按成本从低到高：

```
① 文件名是不是 SKILL.md（全大写）
② --- 是不是在第 0 字节、前后各一行
③ 编码是不是 UTF-8 无 BOM
④ name 是否等于目录名
⑤ 有没有 Tab 缩进 / 字段拼写错误
⑥ 平台缓存：改了先重启会话清缓存
⑦ 权限：目标目录是否有读权限（chmod 644）
```

> ⚠️ 第 ⑥ 条有个真实教训：改了技能里的参数默认值，
> 执行时**用的还是旧值**——平台缓存了技能描述。
> ⭐ **凡是改了 SKILL.md，第一件事就是重启会话并清缓存。**

---

## 速查

| 症状 | 先查 |
|---|---|
| 技能列表里根本没有 | 路径 / 文件名 / 编码 |
| 列表里有但调用失败 | `---` 位置 / YAML 语法 / name≠目录名 |
| 本地能跑、CI 失败 | ⭐ 大小写 |
| 改了值不生效 | ⭐ 缓存，重启会话 |
| 权限看着对还是不加载 | 换目录试，或 `chmod 644` |
