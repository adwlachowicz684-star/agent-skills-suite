# 三种分发方式：Git / 插件市场 / 企业托管

> 相关：《skill-distribution》的 `enterprise-registry.md` ·
> `supply-chain-trust.md` · `marketplace-listing.md`

---

## 目录

- [1. 三种方式与优先级](#1-三种方式与优先级)
- [2. 方式一：提交到 Git 仓库](#2-方式一提交到-git-仓库)
- [3. 方式二：插件 + 市场](#3-方式二插件--市场)
- [4. ⭐ 方式三：企业托管设置（最高优先级）](#4--方式三企业托管设置最高优先级)
- [5. 平台差异](#5-平台差异)
- [6. 安装与验证](#6-安装与验证)

---

## 1. 三种方式与优先级

| 方式 | 范围 | 适合 |
|---|---|---|
| **Git 提交** | 单项目 | 团队编码标准、项目专属流程 |
| **插件市场** | 跨项目 | 不止服务本团队、对社区有用 |
| ⭐ **企业托管设置** | 全组织 | ⭐ 强制标准、安全要求、合规流程 |

> ⭐ **企业技能优先级最高——
> 同名时它覆盖个人、项目、插件技能。**

---

## 2. 方式一：提交到 Git 仓库

放在 `.claude/skills/`，**任何克隆仓库的人自动获得**，无需额外安装。

```bash
git add .claude/skills/
git commit -m "Add team code review skill"
git push
```

> 你推送更新，团队下次 pull 就拿到。
> `.claude/` 目录里的 agents、hooks、skills、settings **全部随 Git 共享**。

适合：**团队编码标准 · 项目专属工作流 · 引用你们代码库结构的技能**。

---

## 3. 方式二：插件 + 市场

插件是**分发容器**，可同时捆绑 Skills、斜杠命令、agents 和 MCP server。

```
my-plugin/
├── .claude-plugin/plugin.json
├── skills/proposal-writing/SKILL.md
├── agents/
└── hooks/hooks.json
```

```bash
/plugin marketplace add owner/repo
/plugin install skill-name@marketplace-name
```

市场来源可以是：GitHub 仓库、GitLab URL、本地路径、或 marketplace.json 的 HTTP URL。

**命名空间**：插件内的技能名为 `/plugin-name:skill-name`，
所以**多个团队的插件可以共存而不冲突**。

团队零配置方案（`.claude/settings.json`）：

```json
{
  "extraKnownMarketplaces": {
    "team-tools": { "source": { "source": "github", "repo": "your-org/claude-plugins" } }
  },
  "enabledPlugins": { "code-review@team-tools": true }
}
```

> ⭐ 这提供版本化、易更新，且跨所有项目生效。

---

## 4. ⭐ 方式三：企业托管设置（最高优先级）

管理员通过托管设置在**全组织范围**部署技能。

```json
"strictKnownMarketplaces": [
  { "source": "github", "repo": "acme-corp/approved-plugins" },
  { "source": "npm", "package": "@acme-corp/compliance-plugins" }
]
```

> ⭐ 适用场景的关键词是 **"必须"**——
> 必须在全组织保持一致的标准、安全要求、合规工作流、编码实践。

两条部署路径：

| 路径 | 机制 | 保障 |
|---|---|---|
| **MDM 托管** | 通过 JAMF/Intune/Mosyle/Kandji，或 macOS plist / Windows 注册表下发 | ⭐ **OS 级，用户与项目设置都无法覆盖** |
| **服务端托管** | 每次启动 + 每小时轮询推送策略 | 无需 MDM，但无 OS 级强制 |

---

## 5. 平台差异

| 能力 | Claude Code | Claude.ai |
|---|---|---|
| 安装 | 文件系统 | ZIP 上传 |
| 版本控制 | ✅ | ❌ |
| 团队共享 | Git + 市场 | 仅个人 |
| 插件生态 | ✅ | ❌ |
| 网络访问 | 完整 | 受限 |

---

## 6. 安装与验证

```bash
mkdir -p .claude/skills/my-skill      # 项目级（随代码走）
mkdir -p ~/.claude/skills/my-skill    # 个人级（所有项目）
```

> ⭐ **技能在启动时加载——改完必须重启 Claude Code**。

```bash
claude doctor     # 应在 Loaded Skills 下看到你的技能，带绿色对勾
```

不加载时的四项检查：

```
① 文件路径是否在预期位置
② SKILL.md 是否有合法 YAML frontmatter
③ name 是否只用小写字母、数字、连字符
④ ⭐ 改完有没有重启
```

不被使用时：

```
① description 写得更具体（何时用）
② 加触发短语 "when user asks to..."
③ ⭐ 在提示词里显式提及该技能的用途
```

---

## 速查

| 需求 | 方式 |
|---|---|
| 单项目团队标准 | ⭐ Git 提交 `.claude/skills/` |
| 跨项目/对外 | 插件 + 市场 |
| 全组织强制 | ⭐ 企业托管设置（优先级最高） |
| 最强保障 | MDM 托管（OS 级，不可覆盖） |
| 改完不生效 | ⭐ 重启 + `claude doctor` |
| 多团队插件共存 | `/plugin:skill` 命名空间 |
