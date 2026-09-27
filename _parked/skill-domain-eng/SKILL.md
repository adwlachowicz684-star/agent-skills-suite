---
name: skill-domain-eng
description: 软件开发与代码类领域 Agent Skills 的实例库——代码质量、代码审查、代码简化、重构、测试、测试框架、调试与恢复、构建错误解决、前端/UI、移动端、CLI 设计、API 设计、API 文档生成、文档写作、变更日志、Git/PR 工作流、依赖升级、国际化实现、遗留迁移、输出控制、状态持久化、提示注入审计。用于按领域参考现成写法，或把本领域的工程规范沉淀成技能。
  Do NOT use for 基础设施与数据类领域（用 skill-domain-infra）、业务运营类领域（用 skill-domain-biz）、技能本身的写法与流程（用 skill-authoring）、评估打分（用 skill-evaluating），也不用于直接产出工程交付物。
---

# 工程技术领域实例库

## 边界

- 用于：**按工程领域参考现成写法** · **把本领域规范沉淀成技能**
- 不用于：业务运营领域 · 技能写法本身 · 评估打分 · 直接产出交付物

## 核心原则

> ⭐ **这些实例共同的价值**：
> **把"模型会写但写得像所有人"的领域，变成按你们的标准写。**

```
□ 前端是"模型会写但写得像所有人"的重灾区
□ ⭐ 引擎/框架技能属于"强偏好 + 中等能力增益"
   ——模型会写脚本，但"必须静态类型、信号怎么挂"要写进技能
□ ⭐ 框架专属的硬性约定正是最容易漏的部分
```

> ⭐ **最有价值的内容永远是 Gotchas**——来自实际踩过的坑。
> 例：*"subscriptions 表是 append-only 的，要找 version 最高的那行，
> 不是最新 created_at 的那行。"*

## 路由表（按需深读，一次只读一份）
| `unity-refactor-skill.md` | ⭐ 重构技能实例：默认范围=最近改动、八条规则 |
| `unity-csharp-standards.md` | ⭐ Unity C# 规范：m_/c_/s_ 前缀、假 null、Awake 缓存 |
| `save-system-skill.md` | ⭐ 存档系统：数据/逻辑分离、迁移三规则 |
| `godot-signal-practices.md` | ⭐ Godot 信号：向上发信号向下调方法、避免冒泡 |
| `game-state-machine.md` | ⭐ 游戏状态机：switch 起点、状态表、暂停坑 |
| `systematic-debugging-skill.md` | ⭐ systematic-debugging 样本：四阶段、三次修复规则 |
| `gamedev-skill-routing.md` | ⭐ 游戏技能库路由：三维正交、指纹识别、降级路径 |
| `five-starter-skills.md` | ⭐ 五个立刻能做的起步技能（含完整源码） |
| `code-review-skill-instance.md` | ⭐ 代码审查实例：八步、三档判词、三条硬规则 |
| `refactoring-skills.md` | ⭐ 重构类：味道→手法对照表、先补测试再动 |
| `api-doc-generation.md` | API 文档生成：五步 + 输出模板 + 防腐烂 |
| `debugging-skills.md` | ⭐ 四个调试模式：日志/二分/假设检验/自动验证 |
| `output-control.md` | 输出控制：模板、长度、机器可解析 |
| `state-persistence.md` | ⭐ 状态持久化：${CLAUDE_PLUGIN_DATA}、跨会话读写 |
| `injection-audit.md` | ⭐ 提示注入审计：六类红旗与徽章制 |

**研发流程**：

| 领域 | 读 |
|---|---|
| 测试类（框架检测/边界覆盖/金字塔） | `references/testing-skills.md` |
| 文档类（七阶段结构、为用户写） | `references/documentation-skills.md` |
| ⭐ Git 提交 / PR 工作流（三技能循环） | `references/git-pr-workflow.md` |
| ⭐ 调试五步分诊 / 错误恢复 | `references/debugging-recovery.md` |
| 遗留迁移（绞杀者、特征化测试） | `references/legacy-modernization.md` |

**代码与架构**：

| 领域 | 读 |
|---|---|
| ⭐ 多语言代码质量（TS/Python/Go/Rust） | `references/code-quality-skills.md` |
| **测试框架选型（Vitest/Playwright/Pytest/Pact）** | `references/testing-frameworks.md` |
| ⭐ **Agent 兼容 CLI 设计约定** | `references/cli-design-skills.md` |
| API 设计（REST/GraphQL/gRPC） | `references/api-design-skills.md` |

**界面与端**：

| 领域 | 读 |
|---|---|
| ⭐ **AI 代码评审的信任层（可评论不可合并）** | `references/code-review-automation.md` |
| ⭐ **i18n 五阶段落地与零硬编码验收** | `references/i18n-implementation.md` |
| **变更日志与发布说明（Conventional Commits）** | `references/changelog-release-notes.md` |
| ⭐ **代码简化：脚本驱动 + 何时不该简化** | `references/code-simplifier.md` |
| ⭐ **构建错误定位：禁止猜测式修改** | `references/build-error-resolution.md` |
| 移动端（RN/Flutter/iOS/Android） | `references/mobile-dev-skills.md` |

**数据与运维**：

| 领域 | 读 |
|---|---|
| ⭐ **代码评审信任层：file:line、如何确认、分级** | `references/code-review-trust.md` |
| ⭐ **依赖升级：难点在证明没弄坏、MAJOR 必须留人** | `references/dependency-upgrade.md` |

## Critical Rules

**抄实例的要点**：

- ⭐ **Gotchas 优先抄**——那是唯一无法从通用知识推断的部分
- 具体数值比抽象原则有用（微交互 150–300ms · 饼图最多 5–7 块 · 圈复杂度 ≤10）
- ⭐ **跨库/跨语言方言差异必须显式列出**（UPSERT、结构化日志）
- ⚠️ 会过时的具体示例是维护负债——**宁可不写死代码，只写规则和约束**

**工程领域的通用红线**：

- ⭐ **先测量再优化**——"瓶颈在哪"必须测量，不能讨论（实测：以为是数据库，实际是 CDN 下载占 90%）
- 改进 **<5% 就回滚**——复杂度不值
- ⭐ **安全迁移四步法**（加列允许空 → 回填 → NOT NULL → 默认值）+ 回滚计划
- ⭐ **大表直接 ALTER 会锁表**——用 expand-contract
- ⭐ **ML 默认泄漏安全**——只在训练集上拟合变换；"指标好得不像真的"是需诊断的症状
- ⭐ **不在 main 上提交**；修之前先加回归测试；全部推完才重新请求评审
- 财务/生产类：**模型可以组织数字，不能生成数字**
- ⭐ 复杂投诉/破坏性操作：先整理事实，再交人；不自动回复

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "这个领域模型本来就会" | 会写 ≠ 按你们的标准写。看 Gotchas 那一节。 |
| "多给几个示例更好学" | ⭐ 一两份干净范例远胜几十个杂乱例子。 |
| "优化一下肯定更快" | 先测量。实测里以为是数据库的瓶颈，其实是 CDN。 |
| "迁移脚本跑通就行" | 每一步都要有回滚，且必须带验证查询。 |
| "模型指标很好，直接用" | ⭐ "好得不像真的"本身就是要诊断的症状。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 校验
python scripts/estimate_tokens.py ./my-skill     # 估算成本
```
