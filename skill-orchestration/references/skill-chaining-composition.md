# 技能串联与组合：叠加加载、交接协议、五个坑

> 相关：《skill-orchestration》的 `composition.md` ·
> `collision-arbitration.md` · 《skill-crafting》的 `granularity-atomic-workflow.md`

---

## 目录

- [1. ⭐ 组合是"叠加"不是"覆盖"](#1--组合是叠加不是覆盖)
- [2. 三种组合模式](#2-三种组合模式)
- [3. ⭐ 冲突消解两条规则](#3--冲突消解两条规则)
- [4. ⭐ 交接协议](#4--交接协议)
- [5. ⭐ 嵌套三要点与五个坑](#5--嵌套三要点与五个坑)

---

## 1. ⭐ 组合是"叠加"不是"覆盖"

```
⭐ 按顺序加载多个技能
⭐ ⭐ 后加载的不会覆盖先加载的——它们是扩展上下文
⭐ 实现时同时应用所有已加载技能的约束
```

```yaml
skill: go-developer
skill: observability-instrumentation
# 或用逗号分隔
skill: go-developer,observability-instrumentation
```

> ⭐ **"所有活跃技能的约束同时生效"**——
> 这条跟"技能之间互相 import"是两回事：
> **叠加是约束并存，import 是代码依赖**（后者改一处崩一片）。

**常见组合示例**：

```
新建 Go HTTP 服务   → go-developer, observability-instrumentation
带数据库的 Go 服务 → go-developer, observability-instrumentation
CI/CD 流水线       → devops-automation, go-developer
```

---

## 2. 三种组合模式

| 模式 | 说明 | 例子 |
|---|---|---|
| **串行** | A 的输出 → B 的输入 | 搜索新闻 → 生成日报 |
| **并行** | 多个同时执行，结果合并 | 同时抓取多个 RSS 源 |
| **条件** | ⭐ 依中间结果决定是否执行下一个 | 检测到死链 → 触发修复技能 |

**"并行 + 串行"的真实编排**：

```
工程改造申请（输入文档）
   ↓ [主技能：工程改造申请审查]
   ├── [并行] 格式审查
   ├── [并行] 术语检查
   ├── [并行] 数据核对
   ↓ 汇总
   ↓ [串行] 风险评估（基于以上结果）
   ↓ [串行] 审查报告生成
   ↓ 审查报告（最终输出）
```

> ⭐ 注意顺序：**并行的三个先跑，汇总后才做串行两步**——
> 因为风险评估依赖前三者的结果。

**回退链**（另一种常用形态）：

```
主：  /docker-compose-migration  ← 最新方案
备选：/docker-compose-patterns   ← 主失败时的替代
```

---

## 3. ⭐ 冲突消解两条规则

```
① ⭐ 更具体的赢：
   聚焦单一技术的技能，胜过通用模式技能
   （如 tracing 问题上，observability-instrumentation > go-developer）

② ⭐ 纯风格问题（不影响正确性）后加载的赢

③ ⭐ 真的有歧义时：记一条 --decision 日志，
   说明遵循了哪条指引以及为什么
```

> ⭐ 第 ③ 条很关键——**没记下来的仲裁等于下次还要重新吵一遍**。

**护栏**：

```
· ⭐ 开始前加载全部所需技能——⭐ 不要在任务中途加载
· ⭐ 不要把技能内容合并进任务产出——技能是约束，不是内容
· ⭐ 若所需技能不存在：记 --blocker 并创建研究任务
```

---

## 4. ⭐ 交接协议

```
切换技能时：
① ANNOUNCE   "Now using <skill> for <purpose>"
② SUMMARIZE  前一个技能完成了什么
③ LOAD       只在需要时才加载下一个
④ PASS       在技能之间传递上下文
```

示例：

> "Using `github-actions-workflows`, I've set up the CI pipeline.
> Now loading `dockerfile-optimization` for the Docker build step..."

> ⭐ **交接失败是五个坑里最常见的一个**——
> 直接开始新技能而不说明上一个做了什么。

**Connected Skills 模式**（渐进式加载的推荐做法）：

```
技能正文列出 ## Connected Skills：
  dockerfile-optimization, helm-chart-development, prometheus-metrics

策略：
 1. 先加载 kubernetes-deployment
 2. 到 "Build container"  → 加载 dockerfile-optimization
 3. 到 "Deploy with Helm" → 加载 helm-chart-development
 4. 到 "Set up monitoring" → 加载 prometheus-metrics
```

> ⭐ **这正是"用到哪一节才加载哪个"**——
> 与 `reference-routing.md` 的一层深 + Router 是同一条原则在技能层的延伸。

---

## 5. ⭐ 嵌套三要点与五个坑

**嵌套模式**（主技能内调子技能）的三个工程要点：

```
① ⭐ 子技能复用 —— ⭐ 子技能必须设计成可独立调用
② 上下文共享   —— 主技能上下文传给子技能，避免重复
③ ⭐ 错误隔离   —— ⭐ 子技能失败不能拖垮主技能
```

> ⭐ 三点都做到，嵌套才可控。

**实现**：主技能 SKILL.md 引用子技能，子技能在主技能上下文中执行，主技能看到产出后继续。

**五个坑**：

| 坑 | 说明 |
|---|---|
| ⭐ **过早加载** | ⭐ 一开始就把所有阶段技能加载进来 = 浪费上下文 |
| ⭐ **交接失败** | 开始新技能时不说明上一个做了什么 |
| ⭐ **过度堆叠** | ⭐ 一条消息里 >5 个技能（有实现上限是 5） |
| Bundle vs Stack | ⭐ 同一组合用到 3 次以上 → 做成 bundle，别每次堆 |
| 验证 | 组合后要能验证整条链 |

**不该组合的情况**：

```
① 一个技能已完全覆盖任务
② ⭐ 技能显著重叠（冗余）
③ ⭐ 组合会超出上下文预算
```

---

## 速查

```
□ ⭐ 组合是叠加，不是覆盖（后加载的扩展而非替换）
□ 所有活跃技能的约束同时生效
□ ⭐ 技能之间不 import，走数据契约

三模式：串行 / 并行 / ⭐ 条件（依中间结果决定下一步）

冲突：
□ ⭐ 更具体的赢
□ ⭐ 纯风格后加载的赢
□ ⭐ 歧义时记 --decision 日志

护栏：
□ ⭐ 开始前加载全部所需技能（不中途加载）
□ ⭐ 技能是约束不是内容，别合并进产出
□ ⭐ 缺技能 → 记 --blocker + 创建研究任务

交接四步：
□ ANNOUNCE（正在用哪个、为什么）
□ SUMMARIZE（上一个完成了什么）
□ LOAD（按需才加载）
□ PASS（传递上下文）

嵌套三要点：
□ ⭐ 子技能可独立调用
□ 上下文共享
□ ⭐ 子技能失败不拖垮主技能

五坑：
□ ⭐ 过早加载
□ ⭐ 交接失败（最常见）
□ ⭐ 过度堆叠（>5）
□ ⭐ 同一组合 3+ 次 → 做 bundle
□ 组合后要验证整条链
```

**一句话**：

> ⭐ **技能是约束不是内容——组合时你叠加的是规则，
> 别把它们的正文搬进产出里。**
