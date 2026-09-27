# 团队协作：版本、分发与治理

## 目录

- [三条硬规则](#三条硬规则)
- [四种分发渠道](#四种分发渠道)
- [工具型 vs 领域型](#工具型-vs-领域型)
- [SemVer 怎么用](#semver-怎么用)
- [CHANGELOG 不是 git log](#changelog-不是-git-log)
- [PR 纪律](#pr-纪律)
- [命名与入口](#命名与入口)
- [CI 集成](#ci-集成)

---

## 三条硬规则

### ① 提交到版本控制

> **对团队最重要的决定**：把 `.claude/skills/`（或等价目录）提交进源码仓库。
> 这保证每个开发者 clone 后自动拥有同一套技能。

```gitignore
# 显式加白名单，避免被通用规则忽略掉
!.claude/skills/
```

**立刻获得三件事**：

| 能力 | 说明 |
|---|---|
| **历史可追溯** | 谁在什么时候改了哪条规则 |
| **可回滚** | 某次改动让触发变差 → `git revert` 回去 |
| **可 diff** | 全是文本，改动一目了然 |

> 对比一下：如果技能是埋在某个工具 GUI 里的配置项，**这三件事一件都做不到**。
> 这正是"纯文本 + git"组合的核心价值。

### ② 技能文件是生产代码

> 它**直接决定 agent 在生产中的行为**。
> 它值得和其他代码同等对待：**版本化、评审、记录每次变更。**

### ③ 不要在提交之外编辑

所有更新走 PR，**没有例外**。

---

## 四种分发渠道

| 渠道 | 适用 | 优点 | 缺点 |
|---|---|---|---|
| **项目内嵌** | 项目专属流程（部署、迁移、审查规则） | 零配置，随项目走，天然版本同步 | 只对当前项目生效 |
| **Git 仓库** | 开源技能、小团队、快速原型 | 零额外依赖，任何平台都能用 | 需手动安装 |
| **Git submodule** | 团队通用技能 | 统一管理、版本控制 | Git 新手易搞混 |
| **企业托管** | 需统一管控、有合规要求 | 管理员推送全组织，**用户无法覆盖** | 需企业版 |

**推荐组合**：

```
项目专用技能  → 项目仓库 .claude/skills/
个人通用技能  → 个人 ~/.claude/skills/
团队通用技能  → 独立 shared 仓库 + git submodule
```

### 跨客户端约定路径

> Agent Skills 规范推荐了一个跨客户端约定路径——**`.agents/skills/`**
> - 项目级：`/.agents/skills/`
> - 用户级：`~/.agents/skills/`
>
> **遵循此约定的技能可被多个不同客户端自动发现。**
> 已有 **30+ 款产品**支持，包括 Claude Code、GitHub Copilot、Cursor、VS Code、
> Gemini CLI、OpenCode、Junie 等。

> 实践建议：**权威源放 `.agents/skills/`**，给只认自家路径的客户端加符号链接。

### 私有市场：一个 git 仓库 + 一个清单文件

不需要中心化服务端——**安装即 clone**。

```json
{
  "name": "team-skills",
  "description": "团队内部技能市场",
  "owner": { "name": "DevTools Team" },
  "plugins": [
    { "name": "code-review",
      "source": "./plugins/code-review",
      "version": "1.2.0",
      "keywords": ["review", "security"] },
    { "name": "api-doc-generator",
      "source": { "source": "github", "repo": "your-org/api-doc-skill" },
      "version": "2.0.0" }
  ]
}
```

**三种来源**：相对路径 `./plugins/x` · GitHub 仓库 `{source: github, repo}` · Git URL `{source: url, url}`

**内网 GitLab 也能当技能源**（`npx skills` 支持 Git SSH URL）——
不需要公共市场，不需要私有 npm registry，**利用现有权限体系和 SSH 认证就够了**。

---

## 工具型 vs 领域型

一个非常实用的分类法——**它直接影响权限边界和更新频率**：

| | **工具型** | **领域型** |
|---|---|---|
| 解决什么 | 通用工程问题（迁移校验、代码审查、测试生成） | 特定业务模块（订单、支付、认证、网关） |
| 谁维护 | 架构组统一维护 | 对应业务的开发者 |
| 更新频率 | **低**，与业务无关 | **高**，随业务演进 |
| **`allowed-tools`** | Bash + Edit（要"动手"） | **仅 Read/Grep/Glob**（只"阅读"） |

```yaml
# 工具型：需要执行与修改
name: db-migration
allowed-tools: Bash(sql-lint:*) Read Grep Glob Edit

# 领域型：只分析，不动手
name: order-service
allowed-tools: Read Grep Glob
```

> ⭐ **权限边界越清晰，agent 产生幻觉操作的概率越低。**
>
> 领域型技能只给它读权限——它就不可能顺手改掉你的订单服务代码。

---

## SemVer 怎么用

技能开始被多项目、多人引用时，就该引入语义化版本。

| 级别 | 对技能而言意味着 |
|---|---|
| **MAJOR** (2.0.0) | **破坏性变更**：改了触发语义、删了被脚本依赖的字段、改了输出格式——老的调用方需要适配 |
| **MINOR** (1.3.0) | **向后兼容地加能力**：新增 reference、扩展触发词、加可选脚本 |
| **PATCH** (1.2.1) | **修字**：typo、措辞优化、脚本 bug 修复，**不改行为契约** |

```bash
git tag -a v1.3.0 -m "blog-publish: 新增 SEO 标题硬规则 reference"
git push origin v1.3.0
```

> **submodule 引用时钉到 tag 而非游动的 main**——
> 升级就变成"从 v1.3.0 到 v1.4.0"这种**可读、可评审的动作**。

**在 frontmatter 里也记版本**：

```yaml
metadata:
  author: your-team
  version: "1.3.0"
```

---

## CHANGELOG 不是 git log

> **git 历史记录了"改了什么"，
> 但"为什么改、改了之后触发效果有没有变好"需要单独留痕。**

```markdown
# Changelog

## [1.3.0] - 2026-06-26
### Added
- blog-publish: 接入 SEO 标题硬规则 reference，标题生成前强制过清单
### Changed
- commit: description 补充"存一下""归档"等触发词，提升命中率

## [1.2.1] - 2026-06-20
### Fixed
- code-review: 修正 checklist 里一处误导性表述
```

> **这件事在 agent 语境下尤其重要**——技能改动的效果（触发率变化）
> 在 git log 里是看不出来的。

---

## PR 纪律

### 提交信息：写清 why

```
❌ "update skills"                    ← 六周后毫无用处
✅ "Add guardrail: never use deprecated v1 API endpoints
    — agent was generating invalid calls after migration"
```

> 后者告诉你一切。**要求团队解释 why，不只是 what。**
> 一份有良好提交历史的技能文件是**自解释的**——
> 每个行为都能追溯到引入它的那个决定。

### PR 描述必须回答三个问题

```
1. 你观察到了什么行为，促使你做这个改动？
2. 这次更新改了技能文件里的什么？
3. 提交前你是怎么测试更新后的技能的？
```

> 这不只是代码评审机制，**它是沟通工具**。
> 它迫使贡献者在改动前想清楚，也给评审者和未来的读者完整图景。

### 评审 = 真的跑一遍

> **批准 PR 前，必须带着更新后的技能跑任务，验证输出符合预期行为。**
> 一个人觉得对、但没别人测过的技能更新，是一种负债。

### 让 agent 帮你提炼

如果是一段来回对话导致了这次更新，
**让 agent 把对话蒸馏成最终的技能更新，再开 PR**——
PR 应该反映**干净的结论**，不是**到达结论的混乱路径**。

---

## 命名与入口

### 前缀避免冲突

```
acme-react-standards/
acme-api-conventions/
```

**分类命名**：

| 类型 | 模式 | 例子 |
|---|---|---|
| 通用工具 | 单个名词 | `pdf`、`git`、`docker` |
| 工作流 | 动宾/领域 | `ci-cd`、`code-review` |
| 业务领域 | 服务名 | `order-service`、`payment-gateway` |

### 建一个 meta-skill

> 创建一个叫 **`project-conventions/`** 的元技能，
> **描述所有其他技能以及何时使用它们**。

这给新成员**一个入口**就能理解团队的 AI 工作流。
在开发者上手指南里也列一份技能清单。

---

## CI 集成

**非交互安装**（CI 环境用 `-y` 跳过提示）：

```yaml
- name: Install Skills
  run: npx openskills install git@github.com:your-org/team-skills.git -y
- name: Verify
  run: npx openskills list
```

**定时自动更新**：

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'   # 每周日
jobs:
  update:
    steps:
      - run: npx openskills update -y
      - run: |
          git diff --staged --quiet || git commit -m "Update skills"
```

**在 CI 里钉固定稳定版本**，生产环境不要跟着 main 走。

---

## 自查

```
□ 技能目录是否已提交到版本控制？
□ .gitignore 是否显式加了白名单？
□ 是否用了 SemVer 并在 frontmatter 记版本？
□ 是否有 CHANGELOG（记录 why，不只是 what）？
□ 提交信息是否解释了为什么改？
□ PR 描述是否回答了三个问题？
□ 评审者是否真的跑了任务验证？
□ 是否区分了工具型/领域型的权限边界？
□ 是否用了 .agents/skills/ 跨客户端约定路径？
□ 新成员是否有单一入口了解所有技能？
□ CI 里是否钉了固定版本？
```
