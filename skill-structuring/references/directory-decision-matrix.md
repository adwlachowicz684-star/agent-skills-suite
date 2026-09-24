# 目录决策矩阵：每个文件该放哪

> 相关：《skill-structuring》的 `directory-contract.md` ·
> 《skill-crafting》的 `reference-routing.md`
> 前置：本技能其余文档讲"目录存在哪"，这份只讲"单个文件放哪个子目录"。

---

## 目录

- [1. ⭐ 决策矩阵](#1--决策矩阵)
- [2. ⭐ 一层深约束与例外](#2--一层深约束与例外)
- [3. ⭐ scripts 的两种截然不同的东西](#3--scripts-的两种截然不同的东西)
- [4. 三种真实结构样本](#4-三种真实结构样本)
- [5. 路径写法与排序](#5-路径写法与排序)

---

## 1. ⭐ 决策矩阵

| 文件特征 | 建议目录 |
|---|---|
| 二进制文件（图片、图标、字体） | `assets/` |
| ⭐ 文档模板（HTML / DOCX / LaTeX） | `assets/templates/` |
| 配置 schema（JSON / YAML） | `assets/` |
| ⭐ 业务规则文档（>100 行） | `references/` |
| API 文档、风格指南 | `references/` |
| ⭐ 可执行工具脚本 | `scripts/` |
| ⭐ 参考代码范例（不执行） | `scripts/` 或 `references/` |
| ⭐ 查找表（CSV / TSV） | ⭐ 数据用 `assets/`，说明放 `references/` |

**判据一句话**：

```
⭐ 会被"读进上下文"理解 → references/
⭐ 会被"按路径引用、零 token 成本" → assets/
⭐ 会被"执行、不进上下文" → scripts/
```

> ⭐ 最容易搞错的是**查找表**：一张 CSV 若是给 agent 查的数据 → `assets/`；
> 若是解释字段含义的说明 → `references/`。
> 判据是**它进不进上下文**。

---

## 2. ⭐ 一层深约束与例外

```
⭐ references/ 和 scripts/ 里的文件应当直接放在各自目录下，
   ⭐ 不要放进子目录（避免嵌套引用 references/subdir/file.md）
```

为什么：嵌套引用会让模型改用 `head -100` 之类的预览方式读取，
导致信息不完整——这和 `progressive-disclosure-official.md` 那条一致。

```
⭐ 例外：assets/ 允许子目录
   assets/templates/ · assets/icons/
   因为常要按类型组织多种资源
```

**另一个硬约束**：

```
⭐ 主 SKILL.md 保持在 500 行以内
   ——在"全面"与"上下文效率"之间取平衡
```

---

## 3. ⭐ scripts 的两种截然不同的东西

这是最容易被忽略的区分：

```
⭐ 可执行脚本（executable）
   → 自包含、有良好文档说明
   → agent 直接运行它

⭐ 参考脚本（reference script）
   → 作为范例供 agent 改编
   → agent 读它、照着写自己的版本
```

> ⭐ **两者都放在 `scripts/`，但语义完全不同**：
> 前者是工具，后者是教材。
> **在 SKILL.md 里必须写明是"运行它"还是"照它改写"**，否则模型会搞混。

这对应 `reference-routing.md` 那条"要结果一致 → 执行；要每次有新见解 → 读进来"
——同一条原则在 `scripts/` 内部的延伸。

---

## 4. 三种真实结构样本

**① 最小结构**（营销活动分析）

```
analyzing-marketing-campaign/
├── SKILL.md                          # 核心工作流
└── references/
    └── budget_reallocation_rules.md  # 确定性规则（100+ 行）
```

> 单文件 references，SKILL.md 专注流程步骤，规则细节分离。

**② 脚本密集结构**（PDF 处理）

```
pdf/
├── SKILL.md
├── forms.md              # ⭐ 表单专项（在根目录，非标准组织）
├── reference.md
└── scripts/
    ├── check_fillable_fields.py
    ├── convert_pdf_to_images.py
    ├── extract_form_field_info.py
    └── fill_pdf_form_with_annotations.py
```

> ⚠️ 注意 `forms.md` 在根目录——这是**早于严格标准的遗留组织方式**。
> ⭐ **不要模仿这个**：新增文档一律进 `references/`。

**③ 资源密集结构**（newsletter 设计）

```
designing-newsletters/
├── SKILL.md
├── references/
│   └── style-guide.md          # 品牌风格
└── assets/
    ├── header.png
    ├── icons/                  # ⭐ assets 下允许子目录
    └── templates/
        ├── newsletter.html
        └── layout.docx
```

> ⭐ 三个可选目录都用上，且**文档（references）与模板（assets）分离清晰**。

---

## 5. 路径写法与排序

```
⭐ 路径一律用正斜杠（/），即使在 Windows 上——保证跨平台兼容
⭐ 术语保持一致，降低 agent 的认知负荷
```

SKILL.md 正文里用相对路径指向资源，渐进式披露保证这些文件只在指令引用到时才加载。

---

## 速查

```
□ ⭐ 进上下文理解 → references/
□ ⭐ 按路径引用零成本 → assets/
□ ⭐ 执行不进上下文 → scripts/
□ 二进制/模板/schema → assets/（模板放 assets/templates/）
□ 规则文档 >100 行 → references/
□ ⭐ 查找表：数据用 assets/，说明用 references/
□ ⭐ 主 SKILL.md <500 行
□ ⭐ references/ scripts/ 保持一层深（assets/ 除外）
□ ⭐ scripts/ 里要写明"运行它"还是"照它改写"
□ ⭐ 路径用正斜杠
□ ⭐ 别模仿 pdf/ 遗留结构的根目录 md
```

**一句话**：

> ⭐ **判断一个文件放哪，只问一句：它进不进上下文？**
