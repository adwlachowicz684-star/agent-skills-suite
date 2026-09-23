# 遥测 Schema：记什么、别记什么

> ⭐ **你的日志管道本身就会成为泄露源。**
> 目标不是"选对厂商"，而是**有一套团队遵守的契约**——
> 换后端时不用重写整个调试故事。

## 目录

- [经典可观测 vs Agent 可观测](#经典可观测-vs-agent-可观测)
- [六类 Span](#六类-span)
- [最小可行契约](#最小可行契约)
- [什么不该记（以及记什么代替）](#什么不该记以及记什么代替)
- [OTel GenAI 语义约定](#otel-genai-语义约定)
- [采样与治理标签](#采样与治理标签)

---

## 经典可观测 vs Agent 可观测

```
经典服务可观测回答：
  "为什么这个请求慢" · "为什么这个请求失败"

Agent 可观测还要回答：
  ⭐ "agent 为什么做出这个决定"
  ⭐ "我们能重放这条 trace 并得到同样的答案吗"
```

> **可重放性（deterministic replay）是硬性要求**，不是加分项。

---

## 六类 Span

**① 会话与请求元数据**（每次 agent 调用的 root span，也是索引其他一切的入口）

```
session_id · tenant_id · acting_user · agent_config_id · agent_version
prompt_template_version · policy_version · model_id · model_version
start_time · end_time · total_cost · total_tokens · outcome
```

**② 推理 Span**——模型产出的思考、计划、反思

```
ReAct 的 thought · Plan-and-Execute 的 plan · Reflexion 的 critique
每次记录：输入 prompt token、输出 completion、token 计数、耗时
```

> ⭐ **这是 agent 特有的遥测——经典可观测没有对应物。**

**③ 工具调用 Span**

```
tool name · version · input hash · input classification
授权决定与理由 · 执行时间 · output hash · output classification
校验决定与理由 · 副作用摘要
```

> **工具 Span 嵌套在推理 Span 之下**——
> 这样 trace 能显示"模型想到 X，于是调用了 Y"。

**④ 记忆操作 Span**

```
哪一层 · 哪个命名空间 · 查询或写入内容 · 分类 · 来源 ·
检索 top-k 或写入策略决定
```

> **记忆投毒检测跑在这些 span 上——数据必须在这里，才检测得到。**

**⑤ 人工决策 Span**

```
投递到审阅队列的请求 · 等待时长 · 审阅者身份 · 决定 · 理由 ·
决策耗时 · 由此产生的 agent 动作
```

> ⭐ **这是人工监督主张的审计证据**（呼应 `compliance-audit.md` 的 Article 14）。

**⑥ 策略与安全 Span**

```
策略引擎评估 · 净化器调用 · 护栏绊线 · kill-switch 检查
```

> ⭐ **这些 span 证明防御层真的跑过了**——
> 这对调试和**监管举证**都重要。

---

## 最小可行契约

> 可直接抄进内部文档让团队遵守。

| 层级 | 何时发出 | 必填字段 | 可选字段 | 脱敏规则 |
|---|---|---|---|---|
| **Run**（trace 根） | 运行开始+结束 | `run_id` `trace_id` `tenant_id` `environment` `agent.name` `agent.version` `start_ts` `end_ts` `status` | `user_id` `session_id` `request_id` `deployment.sha` | **不存原始用户文本**，只存稳定 ID 与哈希 |
| **Step span** | 每个逻辑步骤 | `run_id` `span_id` `parent_span_id` `step.type` `start_ts` `end_ts` `status` | `retry.count` `loop.iteration` `policy.decision` | 默认**仅元数据** |
| **LLM span** | 每次模型调用 | `gen_ai.request.model` `gen_ai.operation.name` `tokens.in` `tokens.out` `latency_ms` | `temperature` `top_p` `cache.hit` | **属性里不放 prompt**；内容走 opt-in blob |
| **Tool span** | 每次工具执行 | `tool.name` `tool.status` `latency_ms` | `tool.error_class` `tool.cost_usd` | **字段白名单**，其余全部脱敏 |
| **Retrieval span** | 每次检索 | `retrieval.source` `retrieval.count` `latency_ms` | `vector_db` `reranker` `top_k` | **不记录文档正文**，只记 doc ID + 哈希 |
| **Content blob** | 仅调试/审批时 | `blob_id` `run_id` `blob.type` `ttl_hours` `kms_key_id` | `content_sha256` `redaction.summary` | **加密 + TTL + 严格 ACL**，没有"永久日志" |

**几个具体取值建议**：

```
ttl_hours     生产环境内容 blob 默认 24 小时
top_k         一定要记——见过 RAG 回归就是 top_k 从 5 悄悄变成 20 引起的
loop.iteration agent 能循环就必须有计数器；
               迭代上限 8–12 对多数工作流是合理默认值
```

---

## 什么不该记（以及记什么代替）

> ⚠️ **这是多数团队搞砸的地方。**

| ❌ 不要记 | ✅ 记什么代替 |
|---|---|
| 系统提示词原文 | `prompt_template_id` + `prompt_template_version` |
| 思维链 / 私有推理 | `prompt_hash`（**确定性归一化后**渲染 prompt 的哈希） |
| 默认记原始用户内容 | `input_classification`（public / internal / restricted） |
| 默认记原始工具载荷（尤其可能含凭据的） | `tool.payload_schema_version` + 白名单字段 |

> ⭐ **目标：让 prompt 可 diff，但不可读。**

**绝对不能记**：

```
□ 原始凭据、访问令牌、私钥
□ 完整卡号
□ 从用户存储里无限制拉取的原始文档
□ 需要证明来源时——存哈希与不可变文档 ID，不存正文
```

---

## OTel GenAI 语义约定

> CNCF OpenTelemetry 的 GenAI 语义约定（2024–2026 趋于成熟）
> 标准化了跨框架的属性名。

**标准词汇**：

```
gen_ai.system                      模型系统（OpenAI / Anthropic / Vertex / Bedrock）
gen_ai.request.model · gen_ai.response.model
gen_ai.request.max_tokens
gen_ai.usage.input_tokens · gen_ai.usage.output_tokens
gen_ai.operation.name              chat / completion / embedding / tool call
gen_ai.prompt · gen_ai.completion  事件形式的内容（受采样与隐私规则约束）
```

**Agent 特有扩展**（尚未标准化但实践中稳定下来）：

```
agent.id · agent.version · agent.loop_type
agent.tool.name · agent.tool.version · agent.tool.risk_class
agent.memory.layer · agent.memory.namespace
agent.policy.decision · agent.policy.version
agent.hitl.reviewer · agent.hitl.decision
agent.kill_switch.triggered · agent.kill_switch.reason
```

> **采用 GenAI 约定能覆盖的部分，其余用 agent 特有属性补齐。**
> OTel 是**发出格式**，后端决定如何可视化与查询。

**Span 映射**：

```
Root:      agent.run {agent.name}
Plan:      plan
LLM:       {gen_ai.operation.name} {gen_ai.request.model}
Tool:      execute_tool {tool.name}
Retrieval: retrieval {retrieval.source}
```

**分布式 trace 的要点**：

```
□ 一个 agent run = 一条 trace
□ trace 上下文要穿过函数调用、微服务跳转、异步队列
□ 工具要作为 peer 创建子 span 并向下游转发上下文
□ 工具改变状态时，记录带 idempotency_key 与 side_effect_id 的事件，
  并链到授权它的那个 agent span
□ planner 扇出并行工具调用时，创建并行子 span 并用 span link 捕获 join
□ 并发控制决策（排队、加锁、背压）直接记在 trace 里
□ 缓存命中/未命中、模型路由选择、策略版本与覆盖原因——记成属性
```

---

## 采样与治理标签

**按结果采样**：

```
失败        100%
成功        N%
新策略版本   100%（新鲜度）
按租户重要性 分层
罕见的失败类别保持全保真，便于快速定位
```

**治理标签**（让保留期与区域锁成为可实现的开关）：

```
data_classification · retention_class · legal_hold_flag · dpa_scope
```

> ⭐ **日志纪律是生产特性**：
> 潦草的日志要么泄露隐私，要么让你两眼一抹黑——
> **两者都会卡住安全与法务的审批。**
> 所以要在**构建期**就设计好日志 schema，
> 让脱敏与保留成为**开关**，而不是半夜的临时重构。

**四类指标**（用于提前预测失败，而不是等用户抱怨）：

```
性能    P50/P95/P99 推理延迟 · 单任务平均轮次 · 工具调用平均耗时 · TTFT
成本    单任务 token · 缓存命中占比 · 按维度分摊费用 · 异常高消耗占比
可靠性  任务完成率 · 工具调用失败率 · 重试次数 · 无限循环检出率 · 上下文超限次数
行为    平均工具调用次数 · 工具调用分布 · 幻觉样本占比 · 人工负反馈率 · 思考轮次分布
```

---

## 自查

```
□ 是否有 per-agent identity（动作可归因）？
□ Run 层是否记录了 prompt_template_version 与 policy_version？
□ 推理 span 是否覆盖了"为什么做出这个决定"？
□ 工具 span 是否嵌套在推理 span 之下？
□ 是否记录了 top_k 与 loop.iteration？
□ 属性里是否有 prompt 原文（应改为哈希 + 模板版本）？
□ 内容 blob 是否有 TTL 与加密（默认 24h）？
□ 是否只记了 doc ID 与哈希而非文档正文？
□ 是否采用了 OTel GenAI 约定以便跨后端移植？
□ trace 上下文是否穿过了队列与微服务？
□ 是否按结果采样（失败 100%）？
□ 是否有 data_classification / retention_class 等治理标签？
□ 是否能在事后确定性地重放一条 trace？
```
