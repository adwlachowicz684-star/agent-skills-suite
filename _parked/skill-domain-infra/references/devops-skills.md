# 运维 / SRE 类技能

> ⭐ **运维领域的技能有个共同形态**：
> **把"排查手册"变成"可执行流程"**——
> 从"救火式运维"升级到"可靠性工程"。

## 目录

- [四类运维技能的分工](#四类运维技能的分工)
- [关键实践清单（可直接抄）](#关键实践清单可直接抄)
- [SRE 核心：SLI / SLO / Error Budget](#sre-核心sli--slo--error-budget)
- [渐进式放权：先只读](#渐进式放权先只读)
- [不该自动做的事](#不该自动做的事)

---

## 四类运维技能的分工

| 类型 | 覆盖 | 典型触发 |
|---|---|---|
| **容器化 / K8s** | Dockerfile、Compose、K8s 资源、Helm、排障 | "Pod 一直 CrashLoopBackOff" |
| **IaC** | Terraform / Pulumi / Ansible / Packer | "帮我设计多环境目录结构" |
| **CI/CD** | 流水线设计、缓存、安全扫描、OIDC/secrets | "流水线太慢 / 失败了" |
| **可观测性** | Metrics / Logs / Traces、告警、Dashboard | "服务响应变慢了" |
| **SRE** | SLI/SLO、error budget、事故管理、混沌工程、去重复劳动 | "怎么减少发布导致的故障" |

> ⭐ **按域拆分而非一个"DevOps 大技能"**——
> 呼应 `skill-refining` 的 `splitting.md` 与 `skill-authoring` 的 `skill-types.md` 的九种类型。

---

## 关键实践清单（可直接抄）

> 这类清单就是运维技能的主体——**全是 Gotchas**。

**容器化**：

```
□ 多阶段构建减少镜像体积
□ ⭐ 非 root 用户运行容器
□ 镜像安全扫描（Trivy）
□ 资源限制 requests/limits
□ 健康检查 liveness / readiness / startup probes
□ ⭐ 优雅关闭（preStop hook、SIGTERM 处理）
□ Pod 反亲和性、拓扑分布约束
```

**IaC**：

```
□ ⭐ 状态文件远程存储 + 锁（S3+DynamoDB / Terraform Cloud）
□ 模块化设计，避免重复代码
□ ⭐ 敏感信息用变量 / Secrets Manager，绝不硬编码
□ ⭐ terraform plan 必须人工审查后再 apply
□ 基础设施变更走 PR 审查流程
```

**可观测性**（三类方法学）：

```
USE 方法   每个资源：使用率 / 饱和度 / 错误
RED 方法   每个服务：速率 / 错误 / 时长
四个黄金信号  延迟 · 流量 · 错误 · 饱和度
```

```
□ ⭐ 告警规则避免"告警疲劳"——每个告警必须 actionable
□ Dashboard 分层：服务级 → 系统级 → 业务级
```

> ⭐ **"每个告警必须 actionable"** 这条最值得记住——
> 不能行动的告警等于噪音，而噪音会让人忽略真正的告警。

---

## SRE 核心：SLI / SLO / Error Budget

```
SLI  可量化的服务质量指标
     延迟（P99）· 吞吐量（QPS）· 错误率（5xx 占比）

SLO  目标阈值（如月度 P99 延迟达标 99.95%）

Error Budget  SLO 允许的不可用时间
     ⭐ 99.9% SLO → 月度预算 = 43.2 分钟
```

**决策流**：

```
定义 SLI → 设定 SLO → 计算 Error Budget → 监控消耗
  → ⭐ 决策（发布 / 冻结）→ 复盘优化
```

> ⭐ **"Error Budget 耗尽 → 冻结发布，专注稳定性"**
> 这条把一个模糊的运维争论变成了可计算的规则——
> 正是 `skill-crafting` 的 `guidance-forms.md` 说的 `if <可观察谓词> then`。

---

## 渐进式放权：先只读

> ⭐ **这是运维技能最重要的编排原则**：

```
阶段 1  只读查询（状态检查、日志分析、Grafana 读盘）
        ↓ 确认稳定
阶段 2  低风险写操作（调整资源配置、触发滚动更新）
        ↓
阶段 3  更高权限（需行为审计）
```

```
□ ⭐ 在开放 Agent 操作生产环境之前，务必配置行为审计
□ 从监控开始：先建立可观测性，再逐步接入自动化运维
□ 多云场景优先用统一技能（跨平台工具）
```

**一个典型的自动化闭环**（展示了技能组合）：

```
用户："线上服务响应变慢了"
Agent: → 查 Grafana 仪表盘发现 P99 延迟飙升
      → 检查 K8s Pod 发现内存接近 limit
      → ⭐ 自动调整 resources 并触发滚动更新
```

> 注意最后一步——**这是阶段 2/3 的权限**，不是一开始就该给的。

---

## 不该自动做的事

> ⭐ **运维技能必须有明确的"停手"清单**：

```
□ ⭐ terraform apply —— plan 必须人工审查
□ ⭐ 生产环境的破坏性操作（删除、回滚到未知状态）
□ ⭐ 密钥与凭据的处理——用 Secrets Manager / Vault，
    ⭐ SOPS 加密存入 Git，用 IRSA / workload identity
□ 跨环境的批量操作（无分批、无回滚计划）
□ ⭐ 没有 runbook 就执行的事故处置
```

**几个常见挑战与对应方案**（可直接进技能）：

| 问题 | 方案 |
|---|---|
| 基础设施漂移 | ⭐ 自动漂移检测 · CI 里跑 `terraform plan` · 生产只读访问 · 维护 state 完整性 |
| 凭据泄露 | 云原生密钥管理器 / SOPS / IRSA |
| 云成本失控 | 标签策略 · 成本分配标签 · 预算告警 · 右-sizing · spot 实例 · 自动伸缩 |
| K8s 配置复杂 | Helm 模板化 · Kustomize 管环境差异 · GitOps · operator |

**部署策略**（写进技能供选择）：

```
蓝绿 / 金丝雀 / GitOps（ArgoCD / Flux）
Sync Policy：自动 / 手动 · Prune · Self-Heal
```

---

## 自查

```
□ 是否按域拆成多个技能（而非一个 DevOps 大技能）？
□ 容器实践是否含"非 root 运行"与"优雅关闭"？
□ IaC 是否要求 plan 人工审查后才 apply？
□ 是否明确"敏感信息不硬编码"？
□ 是否有 USE / RED / 四个黄金信号的方法学？
□ ⭐ 是否写了"每个告警必须 actionable"（防告警疲劳）？
□ SRE 部分是否含 Error Budget 的计算与冻结规则？
□ ⭐ 是否采用渐进式放权（先只读）？
□ 是否配置了行为审计（开放生产权限前）？
□ ⭐ 是否列出了"不该自动做"的清单（apply / 破坏性 / 密钥）？
□ 是否给出了部署策略选项（蓝绿 / 金丝雀 / GitOps）？
□ 是否覆盖了常见挑战（漂移 / 凭据 / 成本 / 复杂度）？
□ 是否有 runbook 要求（无 runbook 不处置事故）？
```
