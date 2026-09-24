---
name: skill-authoring
description: 从零创建 Agent Skills（SKILL.md 技能包）。用于写新技能、把提示词 / 团队规范 / SOP / 既有文档沉淀成可复用技能，或选择工作流结构与约束强度、写 frontmatter 与示例、定输出契约。产出渐进式披露结构——SKILL.md 路由层 + references/ 详解 + scripts/ 确定性校验 + assets/ 模板。
  Do NOT use for 已有技能的优化瘦身与拆分（用 skill-refining）、评估打分与触发测试（用 skill-evaluating）、安全审计与合规（用 skill-governance）、多技能编排（用 skill-orchestration），也不用于写一次性提示词或 PPT/Word 等成品文件。
---

# 从零写一个 Agent Skill

## 边界

- 用于：**新建技能** · 把提示词/规范/SOP 沉淀成技能 · 选结构与定约束 · 写 frontmatter/示例/输出契约
- 不用于：已有技能的优化拆分 · 评估打分 · 安全审计 · 多技能编排 · 一次性提示词

## 核心原则

**技能不是说明文，是可执行流程。** 四要素缺一不可：

| 要素 | 解决什么 |
|---|---|
| **触发词** | 什么时候用 |
| **输入边界** | 拿什么做 |
| **步骤模板** | 怎么做 |
| **验收标准** | 做到什么程度 |

**上下文窗口是公共资源。** 写下每一段前先问：
*这段配得上它的 token 成本吗？模型已经知道什么？*

> ⭐ **先手写跑一遍，再封装**：重复做过 5 次以上、未来还做 10 次以上的事才值得做成技能。

## 路由表（按需深读，不要一次全读）
| `pushy-description.md` | ⭐ 描述要"稍微强势一点"（官方指引） |
| `seven-step-authoring.md` | ⭐ 七步写第一个技能，含最常被跳过的数据源验证 |
| `imperative-description.md` | ⭐ 祈使句+否定约束：650 次测试 100% 激活 |
| `description-rewrite-case.md` | ⭐ description 改写实录 30%→90% + 六条常见错误 |
| `data-source-validation.md` | ⭐ 数据源验证：技能会取到错的数据吗 |
| `degree-of-freedom.md` | ⭐ 自由度校准：窄桥给护栏，开阔地给方向 |
| `no-op-and-value.md` | ⭐ 每段都要回答：它配得上 token 成本吗 |

**起步**：

| 你要做的事 | 读 |
|---|---|
| **⭐ 三步实操手册** | `references/how-to-guide.md`（怎么做）· `references/creation-framework.md`（骨架与流程）· `references/what-not-to-do.md`（不能做） |
| **完整流程 / 六阶段** | `references/workflow.md` |
| ⭐ **跨模型测试矩阵：Haiku/Sonnet/Opus 三档** | `references/testing-matrix.md` |
| ⭐ **激活率实证：四档数据与一组矛盾证据** | `references/activation-rate.md` |
| ⭐ **description 四种写法模式与三个致命错误** | `references/description-patterns.md` |
| ⭐ **正文写作九条：可逐条检查的启发式** | `references/body-writing-rules.md` |
| ⭐ **验证与升级章节：把废话写成可判定条件** | `references/validation-escalation.md` |
| ⭐ **示例即契约：改技能时不能动的那些示例** | `references/examples-as-contract.md` |
| **看模板与真实范例** | `assets/SKILL_template.md` · `references/real-examples.md` |
| **判断该做成哪一类技能** | `references/skill-types.md`（Anthropic 九种类型） |
| ⭐ **六阶段创作流程 / 三个评估角色** | `references/authoring-workflow.md` |
| ⭐ **验证章节怎么写（含证据对照表）** | `references/verification-section.md` |
| ⭐ **正文该放什么：Gotchas / 模板 / 程序优于声明** | `references/skill-anatomy.md` |
| **写完后自查 / 反模式对照表** | `references/authoring-checklist.md` |

**写各部分**：

| 你要做的事 | 读 |
|---|---|
| 写或改 frontmatter | `references/frontmatter.md` |
| ⭐ **命名约定与 description 好坏对照** | `references/naming-description.md` |
| ⭐ 选工作流结构、定约束强度 | `references/patterns.md` |
| **措辞、语气、格式规范** | `references/writing-style.md` |
| **写示例 / 定验收** | `references/examples.md` |
| **把手头提示词 / SOP 转成技能** | `references/prompt-to-skill.md` · `references/prompt-migration.md` |

**已写完之后**（交给姊妹技能）：

| 后续动作 | 用哪个技能 |
|---|---|
| 优化 / 瘦身 / 拆分 / 翻译 / 发布 | **`skill-refining`** |
| 评估打分 / 触发测试 / 排错 | **`skill-evaluating`** |
| 正文构件细节（形态、目录、脚本、验证） | **`skill-crafting`** |

## 强制工作流（MANDATORY）

1. **先手工跑一遍任务**，记录反复提供的上下文与模型踩的坑——**那就是技能内容**。没跑过就写 = 凭空想象。
2. **定边界**：先写"不做什么"，再写"做什么"。
3. **分类基线失败**：跳步？形状不对？漏元素？依条件而定？→ 决定写法（见 **`skill-crafting`** 的 `guidance-forms.md`）。
4. **选模式**：按 `references/patterns.md` 的决策树定结构。
5. **定自由度**：脆弱易错 → 精确脚本；开放多变 → 文本指令。
6. **写 `SKILL.md`**（路由层，目标 100–150 行，硬上限 500）。
7. **长内容拆进 `references/`**：一层深度，超 100 行的文件加目录。
8. **确定性逻辑放进 `scripts/`**：校验、格式化、计算不交给模型即兴发挥。
9. **跑校验**：`python scripts/validate_skill.py <路径>`，**零错误才继续**。
10. **做触发测试**：`python scripts/gen_eval_set.py` 生成 20 条（10 正/10 负），每条跑 3 次。
11. **配对对照测回归**：同一任务跑「有技能」和「无技能」两遍。
12. **量成本**：`python scripts/estimate_tokens.py <路径>`。

## 输出契约

```
<skill-name>/
├── SKILL.md            # 必需：路由层
├── references/*.md     # 按需加载的详解
├── scripts/*           # 确定性逻辑，须可执行
└── assets/*            # 模板、示例
```

汇报时必须给出：**目录树 · description 全文 · 触发测试结论 · validate 结果**。

## Critical Rules

- `name` 必须 kebab-case、≤64 字符、**与目录名完全一致**——不一致会**静默失败**（扫得到但不加载）
- `description` 第三人称、≤1024 字符、含真实触发词、**必须含 Do NOT**、**不写工作流摘要**（写了模型就照摘要做，跳过正文）
- 禁令要**带理由**；单行 ≤28 词；禁用"尽量""酌情""合适即可"——对模型等于没有约束
- ❌ **给规则加"除非""如有需要"**——例外条款会重新打开谈判空间，且无法限定作用域
- 示例代码：宁可让照抄**响亮失败**，不要**静默误导**
- 引用保持**一层深度**，禁止 A → B → C 链
- 不解释模型已知的概念（PDF、HTTP、JSON 是什么）
- **不写硬编码密钥/内网地址/项目专属路径**——换成机器就断
- **删除 / push / 部署必须设人工确认门槛**
- **循环必须设最大次数**——见过循环 200 次烧光 token 的生产事故
- 校验步骤**分必做与按需**——过度验证是最大单一成本源

## 常见借口（遇到就照此回应）

| Agent 说 | 回应 |
|---|---|
| "这个技能很简单，不用先手工跑" | 每个技能都要先跑过。简单不是豁免。 |
| "先写完再测触发" | 没测过触发的技能等于没写。步骤 10 不可省。 |
| "validate 的警告可以忽略" | 零错误才继续。警告也是信号。 |
| "这一步用户已经做过了" | 用命令验证，不要凭印象。 |
| "多写几条禁令更保险" | 禁令只在防明知故犯时有效。形状问题用配方，否则反噬。 |
| "这个技能相关，肯定有帮助" | **"看起来相关"正是主要风险源**。 |

其余见 **`skill-crafting`** 的 `references/anti-rationalizations.md`。

## 脚本

```bash
python scripts/init_skill.py my-skill            # 生成脚手架
python scripts/validate_skill.py ./my-skill      # 校验（零错误才交付）
python scripts/gen_eval_set.py "技能用途一句话"   # 生成触发测试集
python scripts/estimate_tokens.py ./my-skill     # 估算 token 与预算占比
```
