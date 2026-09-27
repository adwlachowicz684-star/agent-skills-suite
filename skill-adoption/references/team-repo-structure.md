# 团队技能库的仓库结构与 CI

> 一个人用技能是文件；十个人用三个 agent 就是架构问题。
> 这份给一套可复制的仓库结构 + 验证流水线。

## 目录

- [仓库结构](#仓库结构)
- [skill.yaml 与 profiles](#skillyaml-与-profiles)
- [语义化版本](#语义化版本)
- [CHANGELOG 的写法](#changelog-的写法)
- [验证流水线](#验证流水线)
- [发布流程](#发布流程)

## 仓库结构

```
team-skills/
├── skill.yaml                  # ⭐ 清单：profiles、agents、版本
├── README.md
├── CHANGELOG.md
├── .github/
│   └── workflows/
│       ├── validate.yml
│       └── release.yml
├── base/                       # 所有人都要的
│   ├── code-style.md
│   └── git-workflow.md
├── frontend/                   # 前端角色
│   ├── react-patterns.md
│   └── testing-frontend.md
├── backend/                    # 后端角色
│   ├── api-design.md
│   └── database-patterns.md
└── agent-overrides/            # ⭐ agent 专属差异
    ├── claude-code-specific.md
    └── copilot-hints.md
```

> ⭐ **`agent-overrides/` 这个目录是整套结构里最值钱的设计**。
> 见下节。

## skill.yaml 与 profiles

```yaml
name: team-skills
version: 2.1.0
description: "Team coding standards and workflows"
maintainer: "platform-team@example.com"
agents: [claude-code, copilot, cursor, gemini-cli]

profiles:
  frontend:
    skills:
      - base/code-style.md
      - base/git-workflow.md
      - frontend/react-patterns.md
      - frontend/testing-frontend.md
    agents: [claude-code, copilot, cursor]
  backend:
    skills:
      - base/code-style.md
      - base/git-workflow.md
      - backend/api-design.md
      - backend/database-patterns.md
    agents: [claude-code, copilot, cursor, gemini-cli]
  fullstack:
    extends: [frontend, backend]

agent_overrides:
  claude-code:
    append: agent-overrides/claude-code-specific.md
  copilot:
    append: agent-overrides/copilot-hints.md
```

**按角色安装**：

```bash
gh skill install team/team-skills --profile frontend
gh skill install team/team-skills --profile backend
```

> ⭐ **为什么需要 `agent_overrides`**：
> 同一个 agent 行为在不同客户端落地方式不同
> （比如 Claude Code 用 `PreToolUse` hook，Copilot 没有）。
> 用 append 把差异拼在公共内容后面，**公共部分只维护一份**。
>
> 呼应 `instruction-layering.md`（**`skill-crafting`**）那条反模式：
> ❌ 把同一份清单同时粘进多个地方——**三处必然漂移**。

## 语义化版本

> ⭐ **把技能改动当 API 改动对待。**

| 级别 | 含义 | 例子 |
|---|---|---|
| **MAJOR** | 重写或删除，**实质改变 AI 行为**；团队升级前应评审 | 从"允许宽松类型"改成"必须 strict" |
| **MINOR** | 新增技能，既有行为不变 | 加 `backend/database-patterns.md` |
| **PATCH** | 错别字、措辞改进，无功能变化 | 修一个拼写 |

呼应 `versioning-compat.md` 那条提醒：
⭐ **不是每次 description 改进都是安全的**——它会改变触发边界，属 MAJOR。

## CHANGELOG 的写法

> ⭐ **必须写清"哪些 agent 受影响"**——这是技能 CHANGELOG 与普通 CHANGELOG 的关键差异。

```markdown
[2.1.0] - 2026-04-15

Added backend/database-patterns.md: PostgreSQL jsonb handling guidelines
  Agents affected: Claude Code, Copilot, Cursor

Changed agent-overrides/claude-code-specific.md:
  Standard PreToolUse hook configuration
  Agents affected: Claude Code only

Changed base/code-style.md: TypeScript strict mode is now required
  Breaking change for all agents
  Migration: Add "strict": true to tsconfig.json
```

注意最后一条同时给了**影响范围**和**迁移动作**——两者缺一不可。

## 验证流水线

```yaml
# .github/workflows/validate.yml
name: Validate Skills
on:
  pull_request:
    paths: ['**.md', 'skill.yaml']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup gh skill
        run: gh extension install github-actions/gh-skills
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Validate structure
        run: gh skill validate
      - name: Check internal links
        run: gh skill lint --check-links
      - name: Dry-run for each agent
        run: |
          gh skill dry-run --agent claude-code
          gh skill dry-run --agent copilot
          gh skill dry-run --agent cursor
      - name: Enforce CHANGELOG update
        run: |
          if git diff --name-only origin/main | grep -q "\.md$"; then
            if ! git diff --name-only origin/main | grep -q "CHANGELOG.md"; then
              echo "❌ Skill files changed without CHANGELOG update"
              exit 1
            fi
          fi
```

**四个步骤各自的职责**：

```
1. validate      → 结构合规（对应 test-pyramid 第 1 层）
2. lint --check-links → ⭐ 内部链接是否还活着（搬家后最容易断）
3. dry-run --agent X  → ⭐ 逐个 agent 试跑（跨客户端差异）
4. CHANGELOG 强制     → ⭐ 改了 md 就必须记
```

> ⭐ 第 2 步特别值得抄：前面拆分十个技能时，
> 我们踩的正是"文件搬走了，引用还指着裸文件名"这个坑
> （那次修了 187 处）。**CI 里加这一步就不会再犯。**

呼应 `ci-cd-integration.md`（**`skill-governance`**）：
**Lint/Validate 阻断合并，Security Scan 只警告**。

## 发布流程

打 tag + 通知团队。要点：

```
□ ⭐ 每个正式版本对应一个 git tag——回滚就是切回上一个 tag
□ registry 保留最近几个版本，不要只保留最新一条
□ ⭐ 有依赖的技能回滚要成组
□ 破坏性变更单独通知，优先保留旧参数标为废弃
```

## 自查

- [ ] 公共内容与 agent 专属差异分开了吗？（`agent-overrides/`）
- [ ] profiles 覆盖了团队的主要角色吗？
- [ ] 版本号的 MAJOR/MINOR/PATCH 判定一致吗？
- [ ] CHANGELOG 每条都写了"受影响的 agent"吗？
- [ ] 破坏性变更给了迁移动作吗？
- [ ] CI 有 `--check-links` 吗？
- [ ] CI 对每个目标 agent 都 dry-run 了吗？
- [ ] 改 md 不更新 CHANGELOG 会被 CI 拦下吗？
