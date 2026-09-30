---
name: skill-structuring
description: 组织 Agent Skill 的物理结构——目录契约、frontmatter 字段与陷阱、references/assets/scripts 的分工与路由、渐进式披露、打包资源、发布前清理、结构类故障排查。用于技能加载失败、静默不生效、文件该放哪个目录、frontmatter 报错、引用链断、依赖没打包。
  Do NOT use for 从零创建的整体流程（用 skill-authoring）、正文措辞与指令形态（用 skill-crafting）、瘦身与拆分（用 skill-refining）、评估打分（用 skill-evaluating），也不用于 frontmatter 解析与加载故障排查（用 skill-loading）。
---

# 技能的物理结构

## 边界

- 用于：**目录与文件布局** · 三个子目录分工 · 打包资源 · 发布前清理 · 命名
- 不用于：整体创建流程 · 正文措辞 · 瘦身拆分 · 评估打分
- ⭐ **frontmatter 解析、加载机制、作用域、不生效排查 → 《skill-loading》**

## 核心原则

> ⭐ **技能是可读的——正文就是审计轨迹。脚本可以，二进制不行。**

三个子目录的分工，判据是动作而非内容类型：

```
scripts/     ⭐ EXECUTE    —— 要结果一致；执行，不占上下文
references/  ⭐ READ       —— 要每次有新见解；读进上下文，付 token
assets/      ⭐ COPY+FILL  —— 被当作输入或模板消费，零成本
```

## 何时不用本技能

- 想知道"这个工作流该不该做成技能" → `skill-selection` 的 `skill-boundaries/references/worth-skillifying.md`
- 想改指令措辞、禁令还是配方 → `skill-crafting` 的 `skill-crafting/references/guidance-forms.md`
- 想拆分已过大的技能 → `skill-refining` 的 `skill-refining/references/split-three-options.md`
- 想评估技能好不好用 → `skill-evaluating`

## 路由表（按需深读）
| `skill-structuring/references/directory-growth-path.md` | ⭐⭐⭐ 从1个文件起步；参考文档给链接+摘要不要全文复制 |
| `skill-structuring/references/frontmatter-body-consistency.md` | ⭐⭐⭐⭐⭐ description 承诺了正文没有；⭐⭐⭐⭐⭐ 缺失不报错因为没环节在等它；⭐⭐⭐⭐⭐ 从短的一侧检查 |
| `skill-structuring/references/reference-file-practices.md` | ⭐⭐ 一层深度 + 100行带目录 + 会被重复读取 |
| `skill-structuring/references/directory-decision-matrix.md` | ⭐ 决策矩阵：每个文件该放哪个子目录 |
| `skill-structuring/references/rename-alias-deprecation.md` | ⭐⭐⭐⭐⭐ 改名不会报错→静默降级；⭐⭐⭐⭐⭐ 旧名写进描述=零成本别名；⭐⭐⭐⭐ 弃用四段式（含新旧差异）|
| `skill-structuring/references/skill-directory-contract.md` | ⭐⭐⭐⭐⭐ 复制到新机器应立刻能用；⭐⭐⭐⭐⭐ 悬空引用=幻觉来源；⭐⭐⭐ config-example 里的真值也是泄露 |
| `skill-structuring/references/skill-documentation-beyond-body.md` | ⭐⭐⭐⭐⭐ 写在 README 里的安全约束 agent 读不到；⭐⭐⭐⭐⭐ 过时的限制比没有限制更有害 |
| `skill-structuring/references/naming-conventions.md` | ⭐ 命名约定：三重角色、硬规则、一致性 > 形态 |
| `skill-structuring` 的 `skill-structuring/references/directory-contract.md` | ⭐ 目录契约：三个子目录各装什么、assets 不是用来读的 |
| `skill-structuring` 的 `skill-structuring/references/resource-bundling.md` | ⭐ 打包资源：脚本标签、四条不要放、执行意图 |
| `skill-structuring` 的 `skill-structuring/references/references-vs-assets.md` | ⭐ references 进上下文 vs assets 零成本引用 |
| `skill-structuring` 的 `skill-structuring/references/reference-routing.md` | ⭐ 引用路由：Router + STOP 指令、一层深、长文件带 TOC |
| `skill-structuring` 的 `skill-structuring/references/reference-organization.md` | ⭐ 参考文件拆分阈值、三种组织方式、grep 模式 |
| `skill-structuring` 的 `skill-structuring/references/progressive-disclosure-official.md` | ⭐ 官方渐进式披露三模式：按域组织、条件式、避免嵌套 |
| `skill-structuring` 的 `skill-structuring/references/enterprise-layout.md` | 企业目录结构：按职能分区、分角色审查 |
| `skill-structuring` 的 `skill-structuring/references/what-not-to-ship.md` | ⭐ 发布前该删的：多余文件、密钥、时敏信息 |
| `skill-structuring` 的 `skill-structuring/references/git-workflow.md` | Git 工作流：Changelog 倒序、分工、触发词变更要通知 |
| `skill-structuring` 的 `skill-structuring/references/content-placement-flowchart.md` | ⭐ 内容放哪五问决策流 + 跨阶段参数快照 |
| `skill-structuring` 的 `skill-structuring/references/lint-tooling.md` | ⭐ Lint 工具横评：skillscheck / skill-tools 各管什么 |
| `skill-structuring/references/five-paragraph-skeleton.md` | ⭐⭐⭐⭐⭐ 正文五段排布：红线在首、验收在尾、两端重复 |

**布局与打包**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 三个子目录各装什么 | `skill-structuring` 的 `skill-structuring/references/directory-contract.md` |
| ⭐ 内容放哪（五问决策流） | `skill-structuring` 的 `skill-structuring/references/content-placement-flowchart.md` |
| ⭐ 打包资源、四条不要放 | `skill-structuring` 的 `skill-structuring/references/resource-bundling.md` |
| 企业目录结构 | `skill-structuring` 的 `skill-structuring/references/enterprise-layout.md` |

## Critical Rules

**frontmatter**：

- ⭐ **`---` 必须在文件第 0 字节**——从 Word 复制最容易引入不可见字符
- Tab 缩进、`enabled: yes`、单值写成标量（多数系统要块序列）都会**静默失败**
- ⭐ **第一阶段的 "loaded" 只代表文件存在，不代表能跑**——两阶段解析
- 改完 SKILL.md 第一件事是重启会话清缓存；平台会缓存技能描述

**目录**：

- ⭐ **未被引用的 asset 是噪音**——会稀释检索
- ⭐ 相对链接只保持一层深；脚本按路径调用，不链接进上下文
- ❌ 不放：README、CHANGELOG、安装说明、时敏信息（技能本身就该是那些内容）

**跨平台**：

- ⭐ **name 不得含 "claude" / "anthropic"**——其他端能加载，Claude 拒收
- ⭐ 中性位置 `.agents/skills/` 做单一真源，其余 symlink
- ⭐ `allowed-tools` 在部分端不生效——安全约束要各端实测

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "技能在列表里，所以加载成功了" | loaded ≠ 能跑。两阶段解析，第二阶段才严格校验。 |
| "我本地能跑就行" | 大小写敏感性在 macOS/Windows 与 Linux 不同——只能靠规范 + 静态检查防。 |
| "改了 description 就生效了" | 平台缓存技能描述，改完要重启会话。 |
| "多放几个参考文件总有用到的时候" | 未被引用的资源是噪音，会稀释检索。 |
| "扫描器说 SAFE 就够了" | SAFE ≠ 安全。先确认扫描器实际启用了几个引擎。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 校验（含孤儿资产、引用链套检测）
python scripts/validate_skill.py ./my-skill --strict   # 警告也当错误
python scripts/estimate_tokens.py ./my-skill     # 估算正文与 references 成本
```
