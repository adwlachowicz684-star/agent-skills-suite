# API 设计类技能

> ⭐ **现代实践基线（2026-01）**：
> HTTP 语义与可缓存性（RFC 9110）· Problem Details 错误模型（RFC 9457）·
> OpenAPI 3.1+ · 契约优先 + 破坏性变更检测 · 显式版本与废弃 ·
> **默认可运维**（幂等性、限流、可观测、trace context）。

## 目录

- [默认执行清单](#默认执行清单)
- [风格选型决策树](#风格选型决策树)
- [速查表](#速查表)
- [契约优先的含义](#契约优先的含义)
- [错误模型](#错误模型)

---

## 默认执行清单

> ⭐ **这份清单可以直接当技能的骨架**：

```
□ ⭐ 先按约束选 API 风格（公开 vs 内部、性能、客户端查询灵活性）
□ ⭐ 先定义契约（OpenAPI / GraphQL schema / protobuf）
□ 定义错误模型（RFC 9457 + 稳定错误码 + trace ID）
□ ⭐ 定义 AuthN/AuthZ 边界（scope / role / tenancy）与威胁模型
□ ⭐ 为所有列表端点定义分页 / 过滤 / 排序
□ ⭐ 定义限流配额、幂等策略（尤其 POST）、重试与退避指引
□ 定义可观测性（W3C Trace Context、request ID、指标、日志）与 SLO
□ ⭐ 在 CI 里加契约测试 + 破坏性变更检查
□ 发布文档，含示例 + 迁移/废弃策略
```

---

## 风格选型决策树

> ⭐ **决策树是这类技能的核心——把选型从"凭感觉"变成查表**：

```
需要什么 API？
├─ 面向第三方的公开 API？
│   └─ ⭐ REST + OpenAPI（最广兼容）
├─ 内部微服务？
│   ├─ 需要高吞吐？ → ⭐ gRPC（二进制、快）
│   └─ 简单 CRUD？  → REST
├─ 客户端要灵活查询？ → GraphQL
├─ TypeScript 单体仓库？ → tRPC（端到端类型安全，无 codegen）
└─ ⭐ 给 AI agent 用？  → REST + MCP（机器可读、agent 体验）
```

> ⭐ 最后一条是新的：
> **为 agent 设计 API 和为人类设计 API 不是一回事**——
> 需要机器可读的描述与明确的 agent 体验考虑。

---

## 速查表

| 任务 | 模式/工具 | 关键要素 | 何时用 |
|---|---|---|---|
| **设计 REST** | RESTful | ⭐ 名词（不是动词）、HTTP 方法、正确状态码 | 资源型 API、CRUD |
| **版本化** | URL 版本 | `/api/v1/resource` · `/api/v2/resource` | 破坏性变更、客户端迁移 |
| **分页** | ⭐ 游标式 | `cursor=eyJpZCI6MTIzfQ&limit=20` | 实时数据、大集合 |
| **错误处理** | RFC 9457 | `type` · `title` · `status` · `detail` · `errors[]` | 一致的错误响应 |
| **认证** | JWT Bearer | `Authorization: Bearer <token>` | 无状态认证、微服务 |
| **限流** | 令牌桶 | `X-RateLimit-*` 头、429 | 防滥用、公平使用 |
| **文档** | OpenAPI 3.1 | Swagger UI、Redoc、代码示例 | 交互式文档、SDK 生成 |
| **灵活查询** | GraphQL | schema 优先、resolver、DataLoader | 客户端驱动的数据获取 |
| **高性能** | gRPC + Protobuf | 二进制协议、流式 | 内部微服务 |
| **TS 优先** | tRPC | 端到端类型安全、无 codegen | 单体仓库、内部工具 |
| **AI agent API** | REST + MCP | agent 体验、机器可读 | LLM/agent 消费 |

---

## 契约优先的含义

> ⭐ **契约优先 = 先写 OpenAPI/schema，再写代码**：

```
□ 契约是唯一的真源
□ 契约测试验证实现是否偏离契约
□ ⭐ 破坏性变更检查在 CI 里自动跑
   ——改了字段类型、删了端点，CI 直接拦下
```

> ⭐ 呼应 `data-engineering-skills.md` 的"先写数据契约，别先写代码"：
> **不同领域，同一个模式**——契约就是测试套件的规格说明。

---

## 错误模型

**RFC 9457 Problem Details 的字段**：

```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Account balance is 10.00, but 25.00 is required.",
  "instance": "/orders/123",
  "errors": [...]
}
```

> ⭐ 配套要求：**稳定错误码 + trace ID**。
> 呼应 `skill-governance` 的 `telemetry-schema.md` 的 traceId 埋点与
> `skill-crafting` 的 `error-handling.md` 的"响亮失败"：
> **错误要能被定位、被追踪、被分类**。

**幂等性**（尤其 POST）：

```
□ ⭐ 为写操作定义幂等键
□ 明确重试与退避指引（客户端该怎么重试）
□ ⭐ 呼应 error-handling.md 的熔断分类：
   系统级错误（超时、500）才触发熔断；
   业务级错误（余额不足）不触发
```

---

## 自查

```
□ 是否有默认执行清单（九项）？
□ ⭐ 是否有 API 风格选型决策树？
□ 是否区分了公开 API / 内部微服务 / agent 消费？
□ ⭐ 是否为"给 agent 用的 API"单列了考虑？
□ 是否用了 RFC 9457 错误模型？
□ ⭐ 是否所有列表端点都有分页/过滤/排序？
□ 是否为 POST 定义了幂等策略？
□ 是否定义了限流与重试退避？
□ 可观测性是否含 W3C Trace Context 与 request ID？
□ ⭐ CI 里是否有契约测试 + 破坏性变更检查？
□ 是否有迁移/废弃策略？
□ ⭐ 是否契约优先（而非代码写完再补文档）？
□ 分页是否用了游标式（而非 offset）？
□ 错误是否带稳定错误码与 trace ID？
```
