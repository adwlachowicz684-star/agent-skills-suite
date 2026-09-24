# 骨架与创建流程

> ⭐ **一句话本质**：
> Agent Skills 不是"另一种提示词模板"，而是**带发现元数据的文件系统知识包**。

## 目录

- [三层骨架](#三层骨架)
- [目录布局](#目录布局)
- [六阶段创建流程](#六阶段创建流程)
- [最小可交付骨架](#最小可交付骨架)
- [上线前 Checklist](#上线前-checklist)

---

## 三层骨架

```
L1  元数据（name + description）
    ⭐ 启动时加载，约 100 tokens/技能
    → 用廉价的元数据换"可发现性"

L2  正文（SKILL.md 的 markdown 主体）
    ⭐ 触发后才注入，程序性知识

L3  附加资源（references/ · scripts/ · assets/）
    ⭐ 留在磁盘上，按需加载，不占基础上下文
```

> ⭐ **这三层就是"渐进式披露"的全部**。
> 之前 `skill-refining` 的 `context-budget.md` 里那个 34K tokens 的节省，
> 就来自严格区分 L1/L2/L3。

**正文写作的两条纪律**：

```
□ ⭐ 正文只写领域专有知识，不写常识
□ 复杂内容拆到 references/，用相对路径引用
□ 单文件不超过 300 行，SKILL.md 不超过 500 行
```

---

## 目录布局

```
my-skill/
├── SKILL.md              ⭐ 必需，文件名全大写
├── references/           详解文档，按需加载
│   ├── api.md
│   └── troubleshooting.md
├── scripts/              确定性逻辑，执行不占上下文
│   └── validate.py
└── assets/               模板与静态资源，被消费而非被读取
    └── template.docx
```

**三个子目录的分工**（容易混淆）：

| 目录 | 内容 | 加载方式 |
|---|---|---|
| `references/` | 文档，按需**读进上下文** | 占 token |
| `scripts/` | 可执行代码，**执行**不读 | ⭐ 不占上下文 |
| `assets/` | 模板/素材，**作为输入或模板消费** | 不自动读 |

> ⭐ **判断依据**：
> 希望每次结果完全一致 → `scripts/`；
> 希望每次有新见解 → 让模型读 `references/` 自己想。

**引用写法**（每个子文件引用都要写清三件事）：

```markdown
For security reviews, see `references/security.md`.
```

```
□ ⭐ 何时读
□ 为何读
□ 读完产出什么
```

> 呼应 `skill-refining` 的 `splitting.md`：**一层引用深度**——
> references 里不要再链向其他 md。

---

## 六阶段创建流程

### 阶段 1 需求定义

```
□ 识别任务（例："从 PDF 提取财务数据，输出 CSV"）
□ ⭐ 定义成功标准
□ 定义触发条件
□ 定义边界情况
□ 判断粒度：太宽要拆，太窄要合
```

**粒度判断**（最常见的第一个错）：

```
❌ 太宽  一个 general-research 技能想同时覆盖
          web 搜索、arXiv、PubMed、数据集
         → 工具和上下文太多，把 agent 搞糊涂
❌ 太窄  arxiv-search-physics 和 arxiv-search-cs 分开
         → ⭐ "技能膨胀"，反而更难找到对的那个
✅ 正好  一个 arxiv-search，单一专注能力
```

### 阶段 2 命名

```
□ kebab-case：csv-analyzer，不是 CsvAnalyzer 或 csv_analyzer
□ 描述性且面向动作：api-client · data-fetcher
□ ⭐ 避免通用名：skill1、tool-a、my-skill-v2
□ ⭐ 避开保留词（claude / anthropic 等）
□ ≤64 字符
```

### 阶段 3 写 description

```
□ 聚焦具体能力、激活触发、上下文
□ ⭐ 写成 "Use when the user asks to..." + 3–5 个触发短语
□ 强示例："Extract tables from a PDF and convert to CSV"
□ ⭐ 排除边界也要声明
□ 避免模糊措辞
```

### 阶段 4 写正文

```
□ 用标题、列表、代码块组织
□ ⭐ 分步工作流 · 输入/输出预期 · 错误处理
□ 编号列表拆解步骤
□ 明确输入与预期输出
□ 附示例
```

### 阶段 5 安装

```
个人    ~/.claude/skills/
项目    .claude/skills/（提交进仓库，同事自动获得）
API     POST /v1/skills（带 beta 头）
UI      Settings → Features
```

```
□ ⭐ 装完必须重启 agent——技能在启动时注册
□ 改了 SKILL.md 不重启 = 没改
```

### 阶段 6 测试与验证

**三场景测试矩阵**：

```
① 正常运行   典型请求
② 边界情况   不完整/畸形输入、缺数据、歧义指令
③ ⭐ 超出范围  技能应当忽略的任务
```

**额外的四类验证**：触发验证 · 输出一致性 · ⭐ 非专家可用性（同事盲测）· 文档准确性。
具体测法（5+5 触发测试、真实项目验证）见 `how-to-guide.md`。

---

## 最小可交付骨架

> ⭐ **可直接复制的最小结构**：

```yaml
---
name: my-skill
description: A brief description of what this skill does and when to use it.
  Include keywords that someone might say when they need this skill.
---
```

```markdown
# My Skill

## Overview
Describe what this skill helps with.

## Instructions
### Step 1: Do the first thing
### Step 2: Do the next thing

## Examples
### Example Input
"Help me with X"
### Example Output
Here's what the agent should produce...

## Avoid
- Don't ...
```

**一个完整真例**（含边界声明）：

```yaml
---
name: code-review
description: Reviews code for bugs, security issues, and improvements.
  Not for reviewing documentation or design mockups.
---
```

```
1. **Critical** — 合并前必须修
2. **Important** — 应尽快修
3. **Suggestion** — 锦上添花

含行号与具体代码引用
```

> ⭐ 注意 description 里的 `Not for ...`——
> 呼应 `skill-crafting` 的 `guidance-forms.md`：**"NOT for X → 用 Y 代替"是最强的路由提示**。

---

## 上线前 Checklist

> ⭐ **全部打勾才发布。** 这是可直接当交付门禁用的表。

**结构合规**

```
□ 目录名 = name，小写连字符，≤64 字符
□ SKILL.md 全大写；frontmatter 的 name/description 非空
□ SKILL.md ≤500 行；无超过 300 行的单文件
□ ⭐ 每个子文件引用都写了"何时读 + 为何读 + 读完产出什么"
```

**触发可靠**

```
□ description 含 WHAT + WHEN + 触发词枚举（含口语说法）
□ 排除边界已声明
□ ⭐ 10 正例全部触发，5 反例全部不触发
```

**安全**

```
□ allowed-tools 已配置且最小化
□ 易混淆的禁用接口已点名
□ ⭐ 危险接口有 hooks 硬阻断（不止靠提示词约束）
```

**健壮性**

```
□ ⭐ 确定性逻辑全部脚本化；脚本输出 JSON、退出码规范
□ 跨阶段参数走 snapshot，每阶段有门卡
□ 读取失败静默降级
```

**可运营**

```
□ 功能走查覆盖异常场景（边界值、工具不可用、诱导越权）
□ ⭐ 有/无技能的 token 与成功率对比数据已留档
□ 埋点字段含 traceId、skillVersion、phase、status
□ version 按 semver 打号，仓库可回溯
```

**精简版发布清单**（个人/团队都适用）：
文件路径与命名正确 · frontmatter 合法 YAML · 触发描述含场景/输入/输出与排除场景
· ⭐ 脚本在干净环境手动跑无报错 · 输出可被下游直接使用
· ⭐ 无绝对路径无密钥 · 权限最小化 · ⭐ 至少两个项目或会话验证通过
· 记录了版本、变更内容与运行依赖。

---

## 自查

```
□ 是否理解 L1/L2/L3 三层的分工与 token 差异？
□ 是否区分了 references/ 与 scripts/ 的用途？
□ 每个子文件引用是否写了"何时读/为何读/产出什么"？
□ 粒度判断：是否既不宽到混淆、也不窄到膨胀？
□ 命名是否 kebab-case 且避开保留词？
□ description 是否有 3–5 个触发短语 + 排除边界？
□ 六阶段流程是否走完（尤其"安装后重启"）？
□ 三场景测试矩阵是否跑过（含"超出范围"）？
□ 是否有同事盲测（非专家可用性）？
□ 上线清单是否全部打勾？
□ ⭐ 是否有"有/无技能"的对比数据留档？
□ 是否按 semver 打了版本号？
```
