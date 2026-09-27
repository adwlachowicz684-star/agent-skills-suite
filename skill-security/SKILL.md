---
name: skill-security
description: Agent Skills 的安全——安装前审计（15 向量 + ToxicSkills 13.4%）、提示注入与隐藏 Unicode 注入防御、allowed-tools 最小权限与 Bash 作用域、沙箱与运行时控制、Hooks 协同与退出码三档、供应链信任与 marketplace 风险、PII 处理、审批门与 kill switch、事件响应。用于装第三方技能前的审查、权限设计、注入防御与安全事故处理。
  Do NOT use for 技能库的生命周期与退役（用 skill-governance）、可观测性与遥测 Schema（用 skill-evaluating）、CI 门禁的测试设计（用 skill-evaluating），也不用于通用网络安全咨询。
---

# 技能安全

## 边界

- 用于：**安装前审计** · **注入防御** · **权限与沙箱** · **运行时控制** · **供应链** · **PII** · **事故响应**
- 不用于：生命周期与退役 · 遥测设计 · 测试设计

## 核心原则

> ⭐⭐⭐⭐⭐ **技能只是指令——而指令不是访问控制。**

```
□ ⭐⭐⭐⭐⭐ 技能里声明的权限 = 意图
   ⭐ 权限规则 / MCP server 参数 / 沙箱 = 强制执行
□ ⭐⭐⭐⭐ Markdown 指令不是访问控制
   "/deploy 技能没有 disable-model-invocation: true
    = Claude 可以因为'代码看起来就绪了'就决定部署。灾难性。"
□ ⭐⭐⭐⭐⭐ 签名验的是身份，不是善意
```

> ⭐⭐⭐⭐⭐ **技能的 description 每个会话都会被加载进上下文。
> 足够长的 description 里嵌一段注入指令，就能操纵 Claude 的行为——
> 即使你从未调用过它。**

## 何时不用本技能

- 退役流程、库存治理、SLO → `skill-governance`
- 遥测 Schema、trace 调试 → `skill-evaluating`

## 路由表（按需深读）
| `toxicskills-13-4-percent.md` | ⭐⭐⭐⭐⭐ 13.4% 严重问题；⭐⭐⭐⭐⭐ description 注入即使不调用也中招；42% 是注入 |
| `unicode-injection-defense.md` | ⭐⭐⭐⭐⭐ 隐藏 Unicode：⭐⭐⭐⭐ 人类审查对它完全失效，必须机器检测 |
| `hooks-skill-cooperation.md` | ⭐⭐⭐⭐ 退出码三档；沉默≠批准；⭐⭐⭐⭐⭐ 阻断消息要可行动（否则试九次） |
| `hooks-rewrite-reinject.md` | ⭐⭐⭐⭐ modifyInput 就地改写；compact 重注入（压缩可订阅）；子代理内也跑 |
| `allowed-tools-least-privilege.md` | ⭐⭐⭐⭐ 最小权限四面红旗（bash+curl 是经典危险组合） |
| `allowed-tools-reference.md` | ⭐⭐⭐ 完整工具表 + `Bash(prefix:*)` 作用域；⭐⭐⭐ 忘了写 Skill 就调不动别的技能 |
| `pre-install-security-audit.md` | ⭐⭐⭐ 15 向量判决规则；⭐⭐⭐ 签名验身份不验善意 |
| `injection-audit.md` | ⭐⭐⭐ 提示注入审计：六类红旗与徽章制 |
| `injection-defense.md` | ⭐⭐⭐ 注入防御与不可信内容边界 |
| `sandbox-execution.md` | ⭐⭐⭐ 沙箱与执行隔离 |
| `runtime-controls.md` | ⭐⭐⭐ 运行时控制与强制层 |
| `supply-chain-audit.md` | ⭐⭐⭐ 供应链审计：像对待代码依赖一样对待技能 |
| `marketplace-security.md` | ⭐⭐⭐ 市场与第三方来源风险 |
| `pii-data-handling.md` | ⭐⭐⭐ PII 处理与数据边界 |
| `approval-gates.md` | ⭐⭐⭐ 审批门设计 |
| `kill-switch.md` | ⭐⭐⭐ kill switch 与紧急停用 |
| `agent-incident-response.md` | ⭐⭐⭐ 安全事件响应 |
| `least-privilege.md` | ⭐⭐ 最小权限一般原则 |
| `hook-risk.md` | ⭐⭐ Hook 自身风险 |
| `compliance-audit.md` | ⭐⭐ 合规审计留痕 |
| `security-review.md` | ⭐⭐ 安全评审清单 |
| `security-audit-ops.md` | ⭐⭐ 安全审计运维 |
| `access-review.md` | ⭐⭐ 访问评审 |
| `audit.md` | ⭐⭐ 审计基础 |

## Critical Rules

- ⭐⭐⭐⭐⭐ **有副作用的技能 MUST 设 `disable-model-invocation: true`**（deploy / commit / send / delete / migrate / push）
- ⭐⭐⭐⭐ **能用具体工具就别用 bash**（`git` 而非 `bash -c "git log"`）；粒度 `Bash(python:scripts/*)` 远好于裸 `Bash`
- ⭐⭐⭐⭐ `bash` + `curl` 是经典危险组合——既能执行命令又能外传数据
- ⭐⭐⭐⭐⭐ **安全说明写在 README = 不存在**（不在加载链里）——必须写进正文流程
- ⭐⭐⭐ 不要在错误或输出里回显密钥、token、完整 URL（只留后四位）
- ⭐⭐⭐⭐ 阻断消息必须给出替代方案——**不给它，模型会把同一条命令试九次**
- ⭐⭐⭐ 隐藏 Unicode 必须机器检测；PostToolUse hook 在模型看到输出之前拦截
- ⭐⭐⭐⭐ 依赖 pin 到 commit hash，不跟踪分支；`scripts/` 里有 `package.json` 就跑 `npm audit`

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "技能里写了'只读'" | ⭐⭐⭐⭐⭐ 声明不会把一个可写 Token 变成只读。 |
| "我读了 SKILL.md，没问题" | ⭐⭐⭐⭐ 隐藏 Unicode 让人类审查完全失效；且插件还能跑 hooks、连 MCP。 |
| "装了但从不调用它" | ⭐⭐⭐⭐⭐ description 常驻上下文，注入不需要被调用。 |
| "这个仓库有 500 star" | ⭐⭐⭐ 三大注册中心的防线是"至少 2 个 star"。 |
| "阻断一下就够了" | ⭐⭐⭐⭐ 阻断消息没给替代方案，它会再试九次。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 结构与副作用字段校验 |
| `scripts/estimate_tokens.py <dir>` | 成本基线 |

## 参考

- 相关技能：《skill-governance》（生命周期、退役、SLO）·《skill-evaluating》（遥测与 trace）·
  《skill-adoption》的 `team-admission-criteria.md`（安全说明落地）
