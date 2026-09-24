# references 与 assets：一字之差，成本差一个数量级

> 相关：`skill-crafting` 的 `skill-structuring` 的 `directory-contract.md`（四目录职责）·
> `skill-structuring` 的 `resource-bundling.md`（打包四不要）·
> 《skill-refining》的 `budget-truncation.md`（预算）

---

## 目录

- [1. 核心区别：进不进上下文](#1-核心区别进不进上下文)
- [2. 一个 10KB 文件的两种命运](#2-一个-10kb-文件的两种命运)
- [3. 各自该装什么](#3-各自该装什么)
- [4. 大文件的处理](#4-大文件的处理)
- [5. 路径一律用占位符](#5-路径一律用占位符)
- [6. ⭐ 禁止的目录与文件](#6--禁止的目录与文件)

---

## 1. 核心区别：进不进上下文

| 目录 | 加载方式 | 上下文成本 |
|---|---|---|
| **references/** | ⭐ 通过 Read 工具**读进上下文** | ⭐ **占用 token** |
| **assets/** | ⭐ **只按路径引用**，内容不读入 | ⭐ **零成本** |

```
references/  = 文本知识，会被读进来
assets/      = 静态资源，Claude 只知道路径
```

assets 的典型用法：

```
复制模板到新位置
在模板里填充占位符
在输出中引用其路径
```

> ⭐ **但绝不把文件内容加载进来。**

---

## 2. 一个 10KB 文件的两种命运

```
同样 10KB 的 Markdown  放在 references/  → 加载后消耗上下文容量
同样 10KB 的 HTML 模板 放在 assets/      → ⭐ 不消耗任何上下文容量
```

**判断问题只有一个**：

> **Claude 需要"理解"它的内容，还是只需要"使用"它？**

```
理解（读进上下文）  → references/
使用（按路径引用）  → assets/
```

- API 规范、决策表、领域知识、详细流程 → references/（要理解）
- 报告模板、图片、字体、样板代码、示例文档 → assets/（只使用）

---

## 3. 各自该装什么

**references/**（会被读进上下文）：

```
数据库 schema · API 文档 · 领域知识 · 公司政策 · 详细工作流指南
NDA 模板 · 财务科目定义 · 术语表
```

**assets/**（不进上下文）：

```
品牌素材（logo.png）· PPT 模板（slides.pptx）
HTML/React 样板 · 字体 · 最终输出要用的样例文档
```

**scripts/**：

```
同一段代码被反复重写时，或需要确定性可靠时
例：scripts/rotate_pdf.py
⭐ 好处：省 token、确定性强、⭐ 可不加载进上下文就执行
```

> ⚠️ 一条常被忽略的：
> **脚本仍可能需要被 Claude 读取**，用于打补丁或做环境适配。
> 所以"脚本不占上下文"只在"直接执行"时成立。

---

## 4. 大文件的处理

> ⭐ **超过 1 万词的文件，在 SKILL.md 里给出 grep 搜索模式。**

否则模型要么读全文（撑爆上下文），要么找不到内容。

```markdown
## 查错误码
grep -n "^### E1" references/error-codes.md
```

配套原则（与 `skill-structuring` 的 `reference-routing.md` 一致）：**引用一层深，不链套**。

---

## 5. 路径一律用占位符

> ⭐ **永远不要写死绝对路径。**

```
❌ /Users/alice/project/templates/report.md
✅ {baseDir}/assets/report-template.md
```

换机器、换用户就断——这与 《skill-scripting》`script-engineering.md`、
`error-handling.md` 里反复出现的规则是同一条。

---

## 6. ⭐ 禁止的目录与文件

**明确不要创建的**：

```
README.md · INSTALLATION_GUIDE.md · QUICK_REFERENCE.md · CHANGELOG.md
```

> ⭐ **技能只应包含 AI agent 完成工作所需的信息。**
> 它不应包含关于"创建过程"的辅助上下文、安装测试步骤、**面向用户的文档**。

理由很实在：**额外的文档文件只会增加混乱**——
它们会被当成候选参考资料，稀释检索。

> ⚠️ 这与 `enterprise-registry.md` 里"README 写安装步骤"不冲突：
> 那份 README 在**仓库根**，用于人类分发；
> 这里禁止的是**技能目录内**的多余文档。

同理：`skillscheck` 会把技能根目录出现 README/LICENSE/Makefile 判为问题，
把 scripts/references/assets 里**未被 SKILL.md 引用的孤儿文件**也判为问题。

---

## 速查

| 要放的东西 | 放哪 |
|---|---|
| API 文档 / schema / 决策表 | references/ |
| 报告模板 / 图片 / 字体 | assets/（零成本） |
| 反复重写的确定性逻辑 | scripts/ |
| >1 万词的大文件 | references/ + ⭐ 在正文给 grep 模式 |
| README / CHANGELOG | ⭐ 不放 |
