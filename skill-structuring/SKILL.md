---
name: skill-structuring
description: 组织 Agent Skill 的物理结构——目录契约、frontmatter 字段与陷阱、references/assets/scripts 的分工与路由、渐进式披露、打包资源、发布前清理、结构类故障排查。用于技能加载失败、静默不生效、文件该放哪个目录、frontmatter 报错、引用链断、依赖没打包。
  Do NOT use for 从零创建的整体流程（用 skill-authoring）、正文措辞与指令形态（用 skill-crafting）、瘦身与拆分（用 skill-refining）、评估打分（用 skill-evaluating）。
---

# 技能的物理结构

## 边界

- 用于：**目录与文件布局** · frontmatter 字段与陷阱 · 三层渐进式披露 · 资源打包 · 结构类故障排查
- 不用于：整体创建流程 · 正文措辞与指令形态 · 瘦身拆分 · 评估打分

## 核心原则

> ⭐ **技能是可读的——正文就是审计轨迹。脚本可以，二进制不行。**

三个子目录的分工，判据是动作而非内容类型：

```
scripts/     ⭐ EXECUTE    —— 要结果一致；执行，不占上下文
references/  ⭐ READ       —— 要每次有新见解；读进上下文，付 token
assets/      ⭐ COPY+FILL  —— 被当作输入或模板消费，零成本
```

## 何时不用本技能

- 想知道"这个工作流该不该做成技能" → `skill-selection` 的 `worth-skillifying.md`
- 想改指令措辞、禁令还是配方 → `skill-crafting` 的 `guidance-forms.md`
- 想拆分已过大的技能 → `skill-refining` 的 `split-three-options.md`
- 想评估技能好不好用 → `skill-evaluating`

## 路由表（按需深读）
| `invocation-control-fields.md` | ⭐ 谁能调用：两个 frontmatter 声明字段 |
| `argument-substitution.md` | ⭐⭐ 参数替换：占位符与会损坏代码的替换陷阱 |
| `nine-checks-not-working.md` | ⭐ 九项排查清单 + 显式调用隔离技巧 |
| `directory-decision-matrix.md` | ⭐ 决策矩阵：每个文件该放哪个子目录 |
| `naming-conventions.md` | ⭐ 命名约定：三重角色、硬规则、一致性 > 形态 |
| `skill-structuring` 的 `directory-contract.md` | ⭐ 目录契约：三个子目录各装什么、assets 不是用来读的 |
| `skill-structuring` 的 `resource-bundling.md` | ⭐ 打包资源：脚本标签、四条不要放、执行意图 |
| `skill-structuring` 的 `references-vs-assets.md` | ⭐ references 进上下文 vs assets 零成本引用 |
| `skill-structuring` 的 `reference-routing.md` | ⭐ 引用路由：Router + STOP 指令、一层深、长文件带 TOC |
| `skill-structuring` 的 `reference-organization.md` | ⭐ 参考文件拆分阈值、三种组织方式、grep 模式 |
| `skill-structuring` 的 `progressive-disclosure-official.md` | ⭐ 官方渐进式披露三模式：按域组织、条件式、避免嵌套 |
| `skill-structuring` 的 `frontmatter-fields.md` | ⭐ Frontmatter 字段速查与 YAML 六个陷阱 |
| `skill-structuring` 的 `frontmatter-pitfalls.md` | ⭐ 静默失败根因：两阶段解析 + 完整雷区表 |
| `skill-structuring` 的 `metadata-fields.md` | ⭐ 四必需字段 + 六元数据 + 六章节 + 每步 Expected/On failure |
| `skill-structuring` 的 `enterprise-layout.md` | 企业目录结构：按职能分区、分角色审查 |
| `skill-structuring` 的 `what-not-to-ship.md` | ⭐ 发布前该删的：多余文件、密钥、时敏信息 |
| `skill-structuring` 的 `git-workflow.md` | Git 工作流：Changelog 倒序、分工、触发词变更要通知 |
| `skill-structuring` 的 `content-placement-flowchart.md` | ⭐ 内容放哪五问决策流 + 跨阶段参数快照 |
| `skill-structuring` 的 `lint-tooling.md` | ⭐ Lint 工具横评：skillscheck / skill-tools 各管什么 |
| `skill-structuring` 的 `five-minute-diagnosis.md` | ⭐ 五分钟诊断八步：model pin、缓存、大小写 |
| `skill-structuring` 的 `verbose-debug.md` | ⭐ Verbose 调试：trace-compare 循环、grep 断言 |

**布局与打包**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 三个子目录各装什么 | `skill-structuring` 的 `directory-contract.md` |
| ⭐ 内容放哪（五问决策流） | `skill-structuring` 的 `content-placement-flowchart.md` |
| ⭐ 打包资源、四条不要放 | `skill-structuring` 的 `resource-bundling.md` |
| 企业目录结构 | `skill-structuring` 的 `enterprise-layout.md` |

**frontmatter**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 字段速查与 YAML 六个陷阱 | `skill-structuring` 的 `frontmatter-fields.md` |
| ⭐ 静默失败根因与雷区表 | `skill-structuring` 的 `frontmatter-pitfalls.md` |
| ⭐ 四必需 + 六元数据 + 六章节 | `skill-structuring` 的 `metadata-fields.md` |

**加载与引用**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 官方渐进式披露三模式 | `skill-structuring` 的 `progressive-disclosure-official.md` |
| ⭐ references vs assets | `skill-structuring` 的 `references-vs-assets.md` |
| ⭐ 引用路由与 Router 指令 | `skill-structuring` 的 `reference-routing.md` |
| ⭐ 参考文件怎么拆 | `skill-structuring` 的 `reference-organization.md` |

**排查与清理**：

| 你要做的事 | 读 |
|---|---|
| ⭐ 五分钟诊断八步 | `skill-structuring` 的 `five-minute-diagnosis.md` |
| ⭐ trace-compare 调试 | `skill-structuring` 的 `verbose-debug.md` |
| ⭐ Lint 工具横评 | `skill-structuring` 的 `lint-tooling.md` |
| ⭐ 发布前该删什么 | `skill-structuring` 的 `what-not-to-ship.md` |
| Git 工作流与 Changelog | `skill-structuring` 的 `git-workflow.md` |

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
