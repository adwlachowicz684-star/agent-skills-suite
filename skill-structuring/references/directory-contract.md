# 目录契约：为什么是目录，不是单文件

> Skills 格式本可以是单个 Markdown、JSON manifest、或 Python 模块。
> **它是"带约定的目录"**——这个形状本身是有理由的。

## 目录

- [标准布局](#标准布局)
- [为什么是目录](#为什么是目录)
- [四个目录各装什么](#四个目录各装什么)
- [为什么 SKILL.md 是唯一必需](#为什么-skillmd-是唯一必需)
- [为什么不要编译产物](#为什么不要编译产物)
- [文件大小上限](#文件大小上限)
- [templates/ 还是 assets/](#templates-还是-assets)
- [常见坑](#常见坑)

---

## 标准布局

```
my-skill/
├── SKILL.md          # 必需：frontmatter + 指令
├── references/       # 可选：长文档，按需加载
│   ├── deep-dive.md
│   └── api-notes.md
├── scripts/          # 可选：可执行助手（Python / shell）
│   └── preflight.py
├── assets/           # 可选：模板、图片、示例数据、fixtures
│   └── example-output.png
└── templates/        # 可选：输出格式（部分实现；标准把它折进 assets/）
    └── config.yaml.j2
```

---

## 为什么是目录

| 理由 | 说明 |
|---|---|
| **真实工作流需要的不止指令** | 还需要示例输出、长参考、脚本。**跟 SKILL.md 捆在一起才能一起版本控制、一起检查。** |
| **避免漂移** | 另一种做法（指令一个文件、脚本放 `~/some/other/path`）**必然产生漂移** |
| **可组合、可共享、可信任** | 目录形状让"分享一个能力"这件事有了最小单位 |

---

## 四个目录各装什么

### `references/` — 按需读的文档

```
✅ 详细解释 · API 文档 · 风格指南
✅ 业务规则：决策树、分类逻辑、流程规则
✅ 查阅型信息：术语定义、代码映射、参考表
❌ 随机项目文件（那是噪音，不是参考）
```

**组织规范**：

```
□ 单个文件保持聚焦——便于 agent 识别相关性
□ 超过 100 行要加目录（让 agent 先看到全貌）
□ 只从 SKILL.md 一层深引用——避免 A→B→C 链套
```

> **例子**：`analyzing-marketing-campaign` 只有一个
> `references/budget_reallocation_rules.md`，
> SKILL.md 引用它——**核心指令保持在 500 行内，
> 同时能访问一套 100+ 行的确定性规则**。

### `scripts/` — 可执行助手

> 详见 `script-engineering.md`。这里只强调一条：

> ⚠️ **必须在 SKILL.md 里说清是"执行"还是"当参考读"。**

### `assets/` — 被消费的资源

> ⭐ **关键区分：`assets/` 里的文件不是用来当文档读的，
> 而是被当作输入或模板消费的。**

| 类型 | 例子 |
|---|---|
| **模板** | `templates/newsletter.html` · `layout.docx` |
| **图片** | `header.png` · `icons/` |
| **数据文件** | 查找表 · schema · JSON 配置 · CSV |

**引用方式**：用**相对路径**在 SKILL.md 里指明。

```markdown
以 assets/templates/newsletter.html 作为基础结构。
```

**组织**：

```
assets/
├── templates/     # 报告模板、slide 模板
├── configs/       # 运行时配置
└── data/          # 查找表、行业代码表
```

> 脚本用相对路径加载 assets。

### `templates/` — 输出格式

用模板标记占位：

```
// templates/component.tsx.template
export function {{ComponentName}}() { ... }
```

> ⚠️ 注意：`templates/` 是**部分实现的约定**——
> **agentskills.io 最小规范把它折进了 `assets/`**。
> 跨客户端分发时优先放 `assets/templates/`。

---

## 为什么 SKILL.md 是唯一必需

> **因为"最小可用的技能"就是指令本身。**

一个只说"当用户问 X，就做 Y 然后 Z"的技能**完全合法**。
**只有在技能长过了单个文件时，才加子目录。**

```
□ 从只有 SKILL.md 开始
□ 内容"挣得"它的位置时才加目录
□ 大多数技能永远不需要更多
```

---

## 为什么不要编译产物

> ⭐ **技能应当是可读的。技能的正文就是审计轨迹。**

```
□ 脚本可以（可读、可审查）
□ 二进制不行——安全扫描器无法推理它，审查者无法检查它
```

> 这条与安全章呼应：`scripts/` 目录即触发审查，
> 而**不透明的二进制让审查根本无法进行**。

---

## 文件大小上限

| 文件类型 | 建议上限 |
|---|---|
| **SKILL.md** | **500 行**（理想 100–150） |
| **references/** 每个文件 | **200 行**（>100 行要加目录） |
| **scripts/** 每个文件 | **300 行**（本技能自定 200） |
| **templates/** 每个文件 | **100 行** |

> 更大的文件能跑，但会挤压上下文窗口。

**命名规范**：

```
□ 目录名 = YAML name 字段（必须完全一致）
□ 全小写 + 连字符：pdf-processing
□ 目录名不要下划线
□ 简洁但具描述性（3–5 词）
□ 带领域/能力提示：mysql-nl2sql、langgraph-docs-query
□ SKILL.md 必须全大写；其余 md 小写连字符
```

---

## templates/ 还是 assets/

| 放哪 | 何时 |
|---|---|
| `assets/templates/` | **跨客户端分发**（符合最小规范） |
| `templates/` | 只在明确支持该约定的运行时内使用 |

> **默认选 `assets/templates/`。**

---

## 常见坑

### ❶ 把脚本放在根目录

```
❌ my-skill/SKILL.md + my-skill/analyze.py
✅ my-skill/SKILL.md + my-skill/scripts/analyze.py
```

> 运行时不会崩，但**读者和渐进式披露逻辑都期望脚本在 `scripts/`**。

### ❷ 把 references/ 当备份存储

> 参考应该是 **agent 按需加载的内容**。
> 随机项目文件是噪音——会稀释检索、浪费上下文。

### ❸ 自定义目录名

> **自定义名字破坏契约。**
> 用标准名，agent 才能不读文件也知道去哪找什么。

### ❹ 多技能仓库的扁平布局

分发多个技能时用扁平结构，**每个技能自包含、独立版本化**：

```
skills-repository/
├── README.md
├── pdf-processing/      # 自包含
│   ├── SKILL.md
│   └── scripts/
├── mysql-nl2sql/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── weather-forecast/
    └── SKILL.md          # 最小形态也是合法的
```

---

## 自查

```
□ 是否从只有 SKILL.md 开始（而非一上来就建全套目录）？
□ 每个目录是否都"挣得"了它的位置？
□ references/ 是否只装按需读的内容（无随机项目文件）？
□ assets/ 是否是被消费的资源（而非当文档读）？
□ 是否用了相对路径引用？
□ 是否有二进制/编译产物在技能里？
□ 是否用了标准目录名（无自定义名）？
□ SKILL.md 是否说清了脚本"执行"还是"参考"？
□ 文件大小是否都在上限内？
□ 目录名是否与 name 字段完全一致？
```
