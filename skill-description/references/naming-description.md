# 命名与 description 的官方规范

> 官方 spec 里最容易做错、也最容易补救的两处。
> 都给了明确的"好/坏"对照。

## 目录

- [name 的硬性约束](#name-的硬性约束)
- [命名约定：动名词形式](#命名约定动名词形式)
- [description 的硬性约束](#description-的硬性约束)
- [第三人称](#第三人称)
- [好/坏对照](#好坏对照)
- [为什么要写得这么具体](#为什么要写得这么具体)

## name 的硬性约束

```
□ 最长 64 字符
□ ⭐ 只能含小写字母、数字、连字符
□ 不能含 XML 标签
□ 不能含保留字
□ ⭐ 必须与目录名完全一致（不一致会静默失败）
```

## 命名约定：动名词形式

> ⭐ **官方推荐用动名词（verb + -ing），
> 因为这清楚描述了技能提供的活动或能力。**

**推荐（动名词）**：

```
processing-pdfs
analyzing-spreadsheets
managing-databases
testing-code
writing-documentation
```

**可接受替代**：

```
名词短语：   pdf-processing、spreadsheet-analysis
动作导向：   process-pdfs、analyze-spreadsheets
```

**避免**：

```
❌ 含糊：    helper、utils、tools
❌ 过于通用：documents、data、files
❌ 保留字
❌ ⭐ 同一技能库里模式不一致
```

**一致性带来的四个好处**：

```
□ 在文档和对话中引用更容易
□ ⭐ 一眼看出技能干什么
□ 组织和检索多个技能更容易
□ 技能库显得专业、 cohesive
```

> ⭐ 呼应 `troubleshooting-manual.md`（**`skill-evaluating`**）的
> "避免通用名"：
> ❌ review / test / deploy
> ✅ frontend-code-review / react-component-test / aws-deployment

## description 的硬性约束

```
□ 非空
□ 最长 1024 字符
□ 不能含 XML 标签
□ ⭐ 应同时描述"做什么"和"何时用"
```

## 第三人称

> ⭐ **始终用第三人称。**
> description 会被注入系统提示，
> ⭐ **人称不一致会导致发现（discovery）问题**。

```
✅ "Processes Excel files and generates reports"

❌ "I can help you process Excel files"      （第一人称）
❌ "You can use this to process Excel files" （第二人称）
```

## 好/坏对照

**✅ 有效的例子**：

```yaml
# PDF
description: Extract text and tables from PDF files, fill forms, merge
  documents. Use when working with PDF files or when the user mentions
  PDFs, forms, or document extraction.

# Excel
description: Analyze Excel spreadsheets, create pivot tables, generate
  charts. Use when analyzing Excel files, spreadsheets, tabular data,
  or .xlsx files.

# Git commit
description: Generate descriptive commit messages by analyzing git diffs.
  Use when the user asks for help writing commit messages or reviewing
  staged changes.
```

**❌ 含糊的例子**：

```yaml
description: Helps with documents
description: Processes data
description: Does stuff with files
```

**共同结构**：

```
[做什么：具体动作 + 对象]
+ [何时用：Use when ... 触发词与上下文]
```

## 为什么要写得这么具体

> ⭐ **agent 要从可能 100+ 个技能里选出正确的那个
> ——你的 description 必须提供足够信息让它判断。**

```
description  → 提供"该不该选它"的充分信息
SKILL.md 正文 → 提供实现细节
```

**分工很明确**：

```
□ description 是路由契约（唯一选路依据）
□ 正文是实现细节（选中后才读）
□ ⭐ 把实现细节写进 description = 浪费宝贵的路由预算
```

呼应 SKILL.md 主文件的规则：
**description 不写工作流摘要**（写了模型就照摘要做，跳过正文）。

## 中文场景的补充

呼应 `i18n.md`（**`skill-refining`**）：

```
□ ⭐ name 不翻译（它是标识符，必须 kebab-case）
□ ⭐ description 必须翻译（它是路由依据）
□ ⭐ 中文日常表达太丰富——把所有同事会说的说法都写进去
□ 中文触发词比英文精确（"写 commit" 无歧义）
```

## 自查

- [ ] `name` ≤64 字符、纯 kebab-case、与目录名一致？
- [ ] 用了动名词形式吗？全库模式一致吗？
- [ ] 避免了 helper/utils/data/files 这类通用名吗？
- [ ] `description` 是第三人称吗？
- [ ] 同时写了"做什么"和"何时用"吗？
- [ ] 含了具体触发词吗？
- [ ] 没把工作流摘要写进去吗？
- [ ] 中文场景：description 覆盖多种说法了吗？
