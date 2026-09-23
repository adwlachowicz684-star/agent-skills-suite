# 可组合模式：五种接线方式与调用链

> ⭐ **复杂工作流 = 一串简单的、各自测过的技能接起来。**
> 前提是每个技能只有一个职责。

## 目录

- [单一职责先行](#单一职责先行)
- [五种模式](#五种模式)
- [调用链：capture 与 on_error](#调用链capture-与-on_error)
- [错误传播](#错误传播)
- [标准数据格式](#标准数据格式)
- [共享尾巴：audit-log](#共享尾巴audit-log)

## 单一职责先行

```
✅ "获取 NAV 数据"          是一个技能
❌ "获取 NAV 数据 + 格式化 + 发送"   ⭐ 是三个技能
```

为什么必须先拆：

```
① 能独立测试
② 能被别的工作流复用
③ ⭐ 出问题时容易定位
```

## 五种模式

**① Pipeline（管道）**——顺序连接，每个转换上一个的输出

```
Input → [A] → [B] → [C] → Output
```

```
阶段 1：解析     用 extract-ast 把代码解析成 AST
阶段 2：分析     对 AST 跑 complexity-analyzer
阶段 3：检查风格 用 style-checker 处理原代码，带 AST 上下文
阶段 4：生成报告 用 report-generator 汇总前面所有输出
```

三条实现注意：

```
□ 前一阶段必须完成，后一阶段才能开始
□ ⭐ 早期阶段的错误会阻止后续阶段
□ 阶段之间要有错误处理；长管道考虑 checkpoint
```

**② Fan-out / Fan-in（扇出汇聚）**——分发给多个技能，再聚合

```
输出包含「按语言」与「聚合」两层结果
```

⚠️ **难点在汇聚不在并行**——详见 `fan-out-fan-in.md`。

**③ Decorator（装饰器）**——包住一个技能加能力，不改它本身

```
调用前：① 从输入哈希生成 cache key
        ② 查缓存
        ③ 命中且未过期 → 直接返回
        ④ 否则 → 走被包裹的技能

调用后：① 接住结果 ② 按 TTL 存缓存 ③ 返回
```

配置示例：

```json
{
  "wrappedSkill": "complexity-analyzer",
  "cacheTTL": 3600,
  "cacheInvalidateOn": ["file_modified", "manual"]
}
```

**④ Fallback（回退）**——按顺序试，直到成功

```
策略 1  语言专用解析器（最准）
策略 2  tree-sitter 通用语法
策略 3  正则兜底
策略 4  让 LLM 抽取结构（几乎总能成）
```

两条纪律：

```
□ 返回第一个成功的策略的结果
□ ⭐ 带上"用了哪个策略"的元数据
   ——否则下游不知道结果的可靠程度
```

**⑤ Filter（过滤）**——传给下游前先筛掉

```
1. 大小过滤     去掉超过 N 行的文件
2. 类型过滤     只保留指定类型
3. 模式过滤     排除匹配某些模式的文件
4. 内容过滤     排除生成代码 / 压缩代码
5. 新近过滤     只保留最近修改过的
```

## 调用链：capture 与 on_error

```
steps:
  - call: get-nav-data
    args:  { fund: "{{ inputs.fund_id }}", date: "..." }
    capture: nav_data          # ⭐ 给输出命名

  - call: format-nav-report
    args:  { data: "{{ nav_data }}", template: "weekly-summary" }
    capture: report_doc        # 引用上一步的输出

  - call: distribute-report
    args:  { document: "{{ report_doc }}", recipients: "..." }
```

要点：**每一步用 `capture` 给输出命名，后续步骤按名引用。**

⚠️ **并行步骤中任何一个失败且未标记为 optional → 整个技能失败。**

## 错误传播

默认：**任何步骤失败都向上传播，让调用者失败**。

可以覆盖：

```yaml
- call: get-external-price-feed
  capture: external_price
  on_error:
    strategy: fallback
    fallback_value: { price: null, source: "unavailable" }
    capture: external_price      # 用回退值覆写
```

四种策略：

| 策略 | 行为 |
|---|---|
| `fail` | 默认，向上传播 |
| `fallback` | 用定义的回退值继续 |
| `skip` | 跳过这一步继续；**捕获的变量为未设置** |
| `retry` | 重试到 `max_retries` 次，然后失败 |

⚠️ `skip` 那条要小心：**变量未设置，下游引用它会拿到空值**，
这比直接失败更危险。

## 标准数据格式

> ⭐ **跨技能用一致的数据格式，是组合的前提。**

```json
// 代码位置
{ "file": "path/to/file.ts",
  "line": 42, "column": 10,
  "endLine": 45, "endColumn": 3 }

// 问题
{ "id": "unique-issue-id",
  "severity": "error" | "warning" | "info",
  "category": "security" | "performance" | "style" | "bug",
  "message": "Human readable message",
  "location": { ... } }
```

没有标准格式，每个衔接点都要写一次转换——
而转换代码是最容易出错的部分。

## 共享尾巴：audit-log

三个常见模式，注意它们的结尾：

```
模式 1  监控告警
  check-condition → if stale/anomalous → format-alert
                  → send-notification → ⭐ audit-log

模式 2  报告生成
  fetch-data → validate-data → transform-data
             → format-report → distribute → ⭐ audit-log

模式 3  对账
  fetch-source-a → fetch-source-b → compare-values
                 → if-mismatch → create-exception-ticket
                 → ⭐ audit-log
```

> ⭐ **三个模式共享同一条尾巴：audit-log。**
> **每一个 agent 产出——告警、报告、对账异常——都应以审计条目结束。**
> **运营流程需要审计轨迹。**

## 三条设计纪律

**① 绝不硬编码环境值**

```
❌ catalog: "plexifact://prod/catalog"
✅ catalog: "{{ vault.data.catalog }}"
```

沙箱与生产之间任何不同的东西（URL、密钥、阈值）
都属于 `vault.json` 或知识文档。

**② 每个输入/输出字段都要有描述**

> ⭐ 这份文档是让 **六个月后的你自己** 也能用它的唯一东西。

**③ 有意地版本化**

```
输入/输出发生破坏性改变时 → 递增版本
```

> ⭐ agent 按名字引用技能；
> 如果某个 agent 是按 v1.0 写的，而输出 schema 在 2.0 变了，
> **那个 agent 需要更新**。

用 `deprecated` 标记正在被替换的技能，给调用者迁移时间，
而不是直接删掉。
