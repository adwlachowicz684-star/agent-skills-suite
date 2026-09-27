# 事件驱动架构：决策表与代价清单

> 事件驱动最容易被"为了未来-proofing"而过度采用。
> 这份给一张决策表和一份**诚实的代价清单**。

## 目录

- [两种拓扑](#两种拓扑)
- [Broker 三方对比](#broker-三方对比)
- [决策表](#决策表)
- [收益与代价对照](#收益与代价对照)
- [常见陷阱](#常见陷阱)
- [Outbox 模式](#outbox-模式)

## 两种拓扑

**Broker 拓扑（编排式 / choreography）**：

```
OrderSvc --OrderPlaced--> [Broker]
   [Broker] --> PaymentSvc --PaymentCaptured--> [Broker]
   [Broker] --> InventorySvc --InventoryReserved--> [Broker]
   [Broker] --> ShippingSvc
```

**Mediator 拓扑（编排式 / orchestration）**：

```
Client --> OrderSagaMediator
   --CapturePayment cmd-->  PaymentSvc
   --ReserveInventory cmd--> InventorySvc
   --Ship cmd-->            ShippingSvc
   各服务回事件给 Mediator
```

> ⭐ **编排式的好处**：saga 状态在一个地方可见。
> 下表会说明什么时候这个好处变得必要。

## Broker 三方对比

| 属性 | Kafka | RabbitMQ | SNS+SQS |
|---|---|---|---|
| 模型 | ⭐ 分布式日志 | 智能 broker、笨消费者 | 发布订阅扇出 + 队列 |
| 顺序 | 每分区内 | 每队列 | ⭐ 仅 FIFO 队列 |
| 保留 | 可配置（天 → 永久） | 确认即删 | 最多 14 天 |
| **重放** | ⭐ 是——重置 offset | 否 | 有限（DLQ + redrive） |
| 吞吐上限 | 极高（百万/秒） | 高（~10 万/秒/队列） | 高，透明扩展 |
| 运维负担 | ⭐ 高（KRaft、分区、ISR） | 中 | 零（托管） |
| 杀手特性 | 可重放日志、多消费者 | ⭐ 路由灵活、逐消息 ack | "在 AWS 上就是能用" |
| **它隐藏的失败模式** | ⭐ 消费者慢 → lag 无声增长 | 队列深度增长（有告警） | DLQ 堆积，必须自己监控 |

> ⭐ **最后一行是这张表最有价值的部分**——
> 每款工具都有"它让你看不见的失败"，
> 选型时要挑一个**你能接受其盲区**的。

## 决策表

| 场景 | 选择 | 为什么 |
|---|---|---|
| 需要同步响应（鉴权、风控） | ⭐ **RPC，不是事件** | 调用方本来就要阻塞；事件只增加延迟和复杂度 |
| 多消费者、同样数据、不同 SLA | 事件通知或 ECS | 解耦收益随消费者数量增长 |
| 审计/合规是硬要求 | 事件溯源 | ⭐ 日志即真相，审计员看日志 |
| ⭐ 只是想"用 Kafka 未来-proof" | **别** | ⭐ Postgres LISTEN/NOTIFY 或队列能解决 80%，直到你真的需要扩展 |
| 2–3 个服务、简单流程 | 直接调用 + 重试 | broker 是杀鸡用牛刀，排障更难 |
| ⭐ 5+ 服务、复杂流程且需补偿 | EDA + 编排器 | 编排式会崩；saga 状态必须可观测 |
| 异构集成（遗留 + 新） | EDA + broker | ⭐ broker 就是集成缝，协议转换放边缘 |
| 同团队、同代码库、进程内事件 | 领域事件 / mediator | ⭐ 不要为进程内 pub/sub 引入网络 |
| 需要重放（分析或恢复） | Kafka / Pulsar / Kinesis | 队列型 broker 不能重放 |
| 路由依赖消息内容 | RabbitMQ topic/headers | ⭐ Kafka 没有逐消息路由原语 |
| 在 AWS 上、中等规模、要托管 | SNS+SQS 或 EventBridge | 运维负担最低 |

> ⭐ **"只是想未来-proof 就上 Kafka → 别"** 这一行
> 与 `code-simplifier.md` 的"何时不该简化"是同一类设计：
> **显式拦截一个高频错误动机**。

## 收益与代价对照

| 收益 | ⭐ 代价 |
|---|---|
| 时间解耦——消费者挂了不影响生产者 | 最终一致性的表面积变大；"读己所写"变成一个项目 |
| 身份解耦——加新消费者不用改生产者 | ⭐ schema 变成公共契约；版本化是永久的 |
| 天然缓冲突发负载 | ⭐ 背压/消费延迟成为新的性能瓶颈 |
| 内建审计日志（尤其事件溯源） | 存储与重放成本；⭐ 事故中重放本身就是另一场战争 |
| 大规模水平扩展（分区、分片） | ⭐ 每分区有序 ≠ 全局有序；需要协同分区 |
| 故障隔离——坏消费者不拖垮生产者 | ⭐ 故障被隐藏；必须显式配 DLQ + 监控 + 对账任务 |
| 易接流处理（Flink、Kafka Streams） | broker 的运维负担是真实的（尤其 Kafka） |

> ⭐ **这张表是"程序优于声明"的典范**——
> 它不告诉你要不要上 EDA，它给你**每一项的账单**。

## 常见陷阱

**跨 topic 的顺序假设**：

```
topic A 的 PaymentCaptured 与 topic B 的 OrderShipped
⭐ 你不能假设谁先到——除非你做了协同分区或显式版本化
```

**EDA 会藏住本会被直接调用暴露的 bug**：

```
□ 静默分歧 bug
□ ⭐ 重试风暴
□ ⭐ schema 演进的坟场
```

**它制造了一类你无法单测的 bug**：

```
□ 最终一致性相关的缺陷
□ ⭐ 需要在集成层才能复现
```

## Outbox 模式

> ⭐ **"outbox 模式不可协商"**。

问题：写数据库和发消息是两个动作，无法原子。

```
❌ BEGIN; INSERT order; COMMIT; PUBLISH event;
   ——中途崩溃 → 订单存在但事件没发

✅ BEGIN; INSERT order; INSERT outbox_event; COMMIT;
   ——后台进程读 outbox 再发
```

呼应 `data-pipeline-skills.md` 的
**"从第一天就设计成可安全重跑"**——同一条可靠性纪律。

## 自查

- [ ] 真的需要异步吗？还是同步调用就能解决？
- [ ] 想过"读己所写"会变成一个问题吗？
- [ ] 知道所选 broker 隐藏了哪类失败吗？
- [ ] 跨 topic 顺序做了协同分区或版本化吗？
- [ ] 用了 outbox 模式吗？
- [ ] 配了 DLQ + 监控 + 对账吗？
- [ ] 服务数 <5 的话，是不是 broker 过重了？
