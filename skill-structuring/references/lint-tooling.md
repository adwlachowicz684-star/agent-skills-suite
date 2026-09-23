# Lint 工具横评：五个工具各管什么

> 相关：`skill-crafting` 的 `skill-structuring` 的 `frontmatter-pitfalls.md`（该查什么）·
> `skill-authoring` 的 `validation-escalation.md` ·
> 《skill-evaluating》的 `test-pyramid.md`（第 1 层）

---

## 目录

- [1. 五个工具与各自侧重](#1-五个工具与各自侧重)
- [2. skillscheck：八平台兼容](#2-skillscheck八平台兼容)
- [3. skill-tools：0-100 打分与路由](#3-skill-tools0-100-打分与路由)
- [4. 其余三个](#4-其余三个)
- [5. CI 接入](#5-ci-接入)
- [6. 选型建议](#6-选型建议)

---

## 1. 五个工具与各自侧重

| 工具 | 侧重 |
|---|---|
| **skillscheck** | ⭐ 八平台兼容 + 四类诊断 |
| **skill-tools** | ⭐ 0-100 打分 + 路由/冲突检测 |
| claude-skill-lint | 图分析：断链、孤儿、重名、依赖环 |
| agent-skills-lint | 跨 agent 校验 + 安装 + 索引生成 |
| skill-lint | spec 合规（含 GitHub Action） |
| agent-skill-linter | 发布就绪 + manifest + 自动修复 |

---

## 2. skillscheck：八平台兼容

覆盖 **Claude Code · OpenAI Codex · GitHub Copilot · Cursor · Gemini CLI ·
Roo Code · Swival · Windsurf**。

四类诊断：

| 类 | 查什么 |
|---|---|
| **Spec 合规** | frontmatter 存在与语法、必填字段、命名规则（小写/无首尾连字符/无连续连字符）、目录名一致性、正文长度与 token 数、`allowed-tools` 是否与已知工具名匹配、⭐ **跨技能重复检测** |
| **Quality** | 描述过短或缺 "use when" 提示、以用户为中心的措辞、关键词堆砌、⭐ **泄露的密钥**（AWS key、GitHub token、私钥、.env）、二进制文件、过大资源、根目录多余文件（README/LICENSE/Makefile）、⭐ **scripts/references/assets 里未被 SKILL.md 引用的孤儿文件**、遍历每个本地 markdown 链接（含锚点）验证目标存在、未闭合的代码栅栏 |
| **Progressive disclosure** | 参考文件 token 预算、引用树嵌套不过深 |
| **Agent 兼容** | 每个平台各自的配置文件（plugin.json、gemini-extension.json、openai.yaml 等）；⭐ **跨 agent 的 name/version/description 不一致** |

用法：

```bash
uvx skillscheck /path/to/skills-repo          # 自动探测
uvx skillscheck --agents claude,codex ./skills
uvx skillscheck --check spec,quality ./skills
uvx skillscheck --fix ./skills                # 安全机械修复
uvx skillscheck --format json ./skills        # CI
uvx skillscheck --strict ./skills             # 警告也当错误
```

`--fix` 能安全修的：小写化 name、合并连续连字符、**把目录重命名为与 name 一致**。

---

## 3. skill-tools：0-100 打分与路由

> 自称 "The ESLint + Lighthouse for Agent Skills"。

三件事：`validate`（20 项 spec）· `lint`（10 条质量规则）· `score`（0-100）。

**评分五维**：

| 维度 | 分值 | 看什么 |
|---|---|---|
| Description Quality | 30 | 长度、具体性、触发上下文 |
| Instruction Clarity | 25 | 代码块、步骤、错误处理 |
| Spec Compliance | 20 | name、description、tokens、行数 |
| Progressive Disclosure | 15 | 文件大小、是否用 references/scripts |
| Security | 10 | 无密钥、无硬编码路径 |

**10 条 lint 规则**（节选）：

```
description-specificity       warn  不用"manage/handle"这类泛动词
description-trigger-keywords  warn  有动作动词或 "Use when..."
no-hardcoded-paths            error 无 /Users/... 或 C:\ 路径
no-secrets                    error 无 API key、token、私钥
progressive-disclosure        warn  大文件应拆到 references/
```

### ⭐ 两个别处没有的功能

```bash
# 路由：给定 query 找最合适的技能（BM25）
skill-tools route "deploy my app" --skills ./skills/

# ⭐ 冲突检测
skill-tools route --conflicts --skills ./skills/
```

> `--conflicts` 直接回答 `namespace-collision.md` 里那件事——
> **不用靠人眼比对 description**。

还有 `watch`（保存即重查）、`init`（脚手架）、`to-prompt`（生成 XML 给系统提示词）、
`hook install`（装 git pre-commit）。

---

## 4. 其余三个

| 工具 | 独特价值 |
|---|---|
| **claude-skill-lint** | ⭐ **图分析**：断链、孤儿、⭐ **重名冲突**、⭐ **依赖环**、frontmatter schema |
| **agent-skills-lint** | 跨 agent 校验/安装/索引生成，按 flavor 用不同 schema |
| **skill-lint** | 针对 Claude.ai / Claude Code / agentskills.io 合规，含 GitHub Action |
| **agent-skill-linter** | 发布就绪（frontmatter + manifest）+ 自动修复 |

> ⭐ **依赖环检测**是 claude-skill-lint 独有的高价值项——
> `catalog-shape.md` 把循环依赖列为结构性反模式，而人眼很难发现。

---

## 5. CI 接入

```yaml
# skillscheck
- name: Lint skills
  run: uvx skillscheck ./skills --strict

# skill-tools（GitHub Action，SARIF 直连 Code Scanning）
- uses: skill-tools/skill-tools/action@v1
  with:
    path: './skills/'
    min-score: '70'
    fail-on: 'warning'
```

SARIF 输出可直接进 GitHub Code Scanning：

```bash
skill-tools check ./skills/ --format sarif > results.sarif
```

> ⭐ **`--min-score 70` 是很有用的门禁**——
> 它把"质量分"变成可执行的合并条件，而不是一个参考数字。

---

## 6. 选型建议

| 你要什么 | 用哪个 |
|---|---|
| 发布给多个平台 | ⭐ skillscheck |
| 要质量分 / 防合并劣质技能 | ⭐ skill-tools（--min-score） |
| 技能多了怕重名和依赖环 | claude-skill-lint |
| 只关心 spec 合规 | skill-lint |
| 发布前最后一道 | agent-skill-linter |

⚠️ 一条提醒（与 `security-audit-ops.md` 一致）：
**工具说 SAFE 不等于安全**。扫描器只覆盖已知模式，
隐藏在自然语言里的手法（如 `marketplace-security.md` 那个 HTML 注释案例）扫不出来。

---

## 速查

| 症状 | 工具 |
|---|---|
| 换个平台就不生效 | skillscheck --agents |
| 想设质量门禁 | skill-tools --min-score |
| 两个技能重名 | claude-skill-lint（图分析） |
| references 里有孤儿文件 | skillscheck（quality 类） |
| 密钥误提交 | skillscheck / skill-tools（都有） |
| 技能互相依赖成环 | claude-skill-lint |
