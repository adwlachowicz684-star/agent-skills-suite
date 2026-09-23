# 可观测性工具选型：Langfuse vs LangSmith

> 前面 `telemetry-schema.md` 讲"记什么字段"，
> 这份讲"用什么记"——两者的差异会反过来影响你的架构。

## 目录

- [能力对比](#能力对比)
- [部署与数据驻留（最大差异）](#部署与数据驻留最大差异)
- [成本模型](#成本模型)
- [延迟与吞吐](#延迟与吞吐)
- [接入方式](#接入方式)
- [怎么选](#怎么选)
- [对技能观测的三条建议](#对技能观测的三条建议)

## 能力对比

| 维度 | LangSmith | Langfuse |
|---|---|---|
| **追踪模型** | 每次运行是 run 树上的节点；嵌套 chain/tool/retriever 成为子 run | "observations"——span / generation / event，根节点带显式 session 与 user ID |
| **上下文传递** | 用 context variables 构建层级 | `@observe` 通过 contextvars 建立父子链接，**async 循环与线程池下仍正确** |
| **LangChain 元数据** | run 对象自带（如 prompt template hash） | 不自动推断，需自己加 |
| **评估** | ⭐ 一等公民的 datasets + `evaluate()` runner | datasets + scorecards，UI 可标注生产 trace；eval SDK 较新 |
| **反馈** | `client.create_feedback(run_id, ...)` 精确落到 run | `/feedback` 语义类似 |
| **提示管理** | Hub 按名运行时拉取版本化 prompt | 版本化可取，但协作（评论、分阶段发布）较轻 |

> **差异的性质**：LangSmith 更成熟，Langfuse 覆盖相近但更年轻。
> 真正的分水岭不在功能，在下两节。

## 部署与数据驻留（最大差异）

```
Langfuse：⭐ MIT 许可，docker-compose + Postgres 或 ClickHouse
          ⭐ trace 永不离开你的 VPC
          自托管免费——只付自己的计算与存储

LangSmith：闭源 SaaS，⭐ 无自托管版本
          企业合同可约定数据驻留，但默认是 LangChain 的云
```

> ⭐ **如果你的 trace 里有不能出内网的 prompt 或用户数据，
> 这一条就直接决定了选型**——不用再看其他维度。

呼应 `telemetry-schema.md` 那条：
**日志管道本身就会成为泄露源；目标是"让 prompt 可 diff，但不可读"**。
自托管把这条风险的暴露面从"第三方 SaaS"缩回"你自己的 VPC"。

## 成本模型

```
LangSmith：按 traced runs 计费 + 席位许可
   ⭐ 一个 agent turn 调用 retriever + 3 个工具 + 最终 LLM
     = 轻易生成 10–20 个 run，每个在低档位都是计费单位
   免费额度在生产量级下很快耗尽

Langfuse：自托管免费；托管云按摄入事件计费
   ⭐ 因为采样可控，你可以把低价值 span 降到零成本
```

**核心差异一句话**：

> ⭐ **LangSmith 惩罚细粒度 span；Langfuse 允许你节流它们。**

两家都不公布按 token 的单价，都按 trace 对象计量——
**真正的杠杆是埋点深度**。

**算一笔自己的账**：

```
每 turn 的 span 数 × 每日 turn 数 × 单价
⭐ "每 turn 的 span 数"是唯一你真正可控的变量
```

## 延迟与吞吐

```
两者埋点开销都是非阻塞的，单 span 批处理开销亚毫秒
——不在请求路径上
```

差别在**摄入端点**：

```
Langfuse 自托管：单 Postgres 节点超过每秒几千次写入会丢或排队，需扩 DB
LangSmith 云：吸收突发，但按项目限速
```

一句很实在的提醒：

> ⭐ **没有任何厂商基准能扛住一个 50 工具的 agent 循环
> ——你每 turn 的 span 数是唯一重要的数字。**

## 接入方式

```python
# LangSmith
from langsmith import traceable

@traceable(name="retrieve_docs")
def retrieve(query: str):
    return vector_store.search(query)

# Langfuse
from langfuse.decorators import observe

@observe(name="retrieve_docs")
def retrieve(query: str):
    return vector_store.search(query)
```

**一个选型细节**：

> ⭐ **Langfuse 的 TypeScript 装饰器与 Python 语义完全一致**
> ——agent 跑在 Node 上时这点很重要。
> LangSmith 支持 JS，但 Python 的故事更深。

**框架无关性**：Langfuse 支持任何支持 OTel 埋点的语言/框架，
并有 100+ 集成（含 Claude Code、OpenClaw、Cursor、n8n、Dify 等）。

## 怎么选

```
有数据驻留要求 / 不能出内网        → Langfuse（自托管）
已经是 LangChain 深度用户          → LangSmith（元数据开箱即用）
agent 跑在 Node/TS                 → Langfuse（TS SDK 对等）
要精细埋点且量大                    → Langfuse（可节流）
预算敏感 / 想先零成本起步           → Langfuse（自托管免费）
要最成熟的 datasets + evaluate()    → LangSmith
```

> **两者都能抓 trace、span、token 数。**
> 差别在部署模型、成本结构和多步 LLM 工作流的现实处理——
> 这个差别**大到足以影响你的架构**。

## 对技能观测的三条建议

**① 先确定埋点深度，再选工具**

```
你要回答的是"技能有没有被用到、用了多少次、花了多少"
→ 不需要每个工具调用都成一个 span
→ 每技能 1–3 个 span 就够，成本立刻降一个数量级
```

**② 用生产数据，不只靠测试集**

```
可观测平台的真正价值是：
  用生产 trace 发现行为 → 修 → 再验证
这个循环比离线测试集更能反映真实使用
```

**③ 技能层面的指标要能回答三问**

```
□ 这个技能被调用了多少次？（呼应 /skill-doctor）
□ 它占了多少上下文？（每个加载的技能每轮都在付费）
□ 它有没有让结果变好？（需要 A/B，见 skill-lift-eval.md）
```

## 自查

- [ ] 有数据驻留要求吗？（决定选型）
- [ ] 算过"每 turn span 数 × 日 turn 数"吗？
- [ ] 埋点深度是必要的，还是默认全埋？
- [ ] 用的是生产 trace 还是只有测试集？
- [ ] 能回答"被调用多少次 / 占多少上下文 / 有没有变好"三问吗？
