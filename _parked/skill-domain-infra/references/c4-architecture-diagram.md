# C4 架构图：四层抽象与红旗检查

> 架构图技能的价值不在"能画图"，
> 而在**强制正确的抽象层级**。这份讲它的强制机制。

## 目录

- [四层与受众](#四层与受众)
- [每层该显示和隐藏什么](#每层该显示和隐藏什么)
- [红旗：做之前先停](#红旗做之前先停)
- [工作流](#工作流)
- [输出要求](#输出要求)
- [为什么这类技能要写得"硬"](#为什么这类技能要写得硬)

## 四层与受众

| 层 | 名称 | 用途 | 受众 |
|---|---|---|---|
| 1 | **Context** | 系统在其环境中的位置 | ⭐ 所有人 |
| 2 | **Container** | 主要组成部分 | 技术干系人 |
| 3 | **Component** | 内部结构 | 开发者 |
| 4 | **Code** | 实现 | 开发者（⭐ 谨慎使用）|

## 每层该显示和隐藏什么

```
Level 1 Context
  显示：系统、用户、外部系统
  ⭐ 隐藏：内部细节、数据库、技术选型

Level 2 Container
  显示：应用、API、数据库、队列
  ⭐ 隐藏：内部结构、类

Level 3 Component
  显示：模块、服务、仓储
  ⭐ 隐藏：单个类、函数

Level 4 Code
  显示：类、接口、关键抽象
  ⭐ 只用：复杂或关键区域
```

> ⭐ **"隐藏什么"比"显示什么"更重要**——
> 大多数烂架构图不是画少了，是塞多了。

## 红旗：做之前先停

> ⭐ **这份技能最值得抄的部分：显式的 STOP 清单。**

如果你正要做以下任何一件事，**停下来重新考虑**：

```
🚩 还没画 context 图就画 container 图
🚩 在同一张图里混用 container 和 component
🚩 在 context 层展示实现细节
🚩 ⭐ 为非关键代码画 code 层图

STOP → 查相应层级的指南 → 再继续
```

> 呼应 `anti-rationalizations.md`（**`skill-crafting`**）与状态机：
> **红旗清单 = 防跳步的显式检查点**。
> 写成"STOP and reconsider"而不是"建议不要"，是有意加强语气。

## 工作流

```
1. 确定受众与目的
   ⭐ CHECKPOINT：从 Level 1 开始，除非已有更高层图

2. 识别当前层的所有参与者与系统

3. 用带标签的箭头定义关系

4. 加技术选型（Level 2+）

   ⭐ CHECKPOINT：验证没有混用抽象层级

5. 加描述以澄清
```

> ⭐ **两个 CHECKPOINT 是硬性插入点**——
> 呼应 `guidance-forms.md`（**`skill-crafting`**）：
> **漏掉必需元素 → 用模板里的 REQUIRED 槽位**，
> 这里用的是流程里的显式检查点，同一思路。

## 输出要求

图必须包含：

```
□ ⭐ 标题标明层级与系统
□ 所有相关元素，且都带描述
□ 带标签的关系
□ 技术选型（Level 2+）
□ ⭐ 清晰的边界用于分组
□ 图例（默认开启）
```

**变量默认值**：

```
DEFAULT_LEVEL  = context     # 从最外层开始
OUTPUT_FORMAT  = mermaid     # 也支持 structurizr / plantuml
INCLUDE_LEGEND = true
```

## 为什么这类技能要写得"硬"

架构图这类任务有三个特点，决定了技能必须强约束：

```
1. ⭐ 错误很"顺眼"
   混了层级的图看起来仍然是张图，不会报错

2. ⭐ 模型默认会画"最详细"的那张
   不给层级约束，它一定往 Level 3/4 跑

3. ⭐ 修正成本高
   画完再改抽象层级等于重画
```

对应写法（呼应 `guidance-forms.md` 的形态匹配）：

```
模型"明知故犯"往细节跑 → ⭐ 红旗清单 + STOP 措辞
输出形状（该显示/隐藏）  → ⭐ 每层的"隐藏"清单
漏掉元素（标题/图例）    → ⭐ 输出要求清单
```

## Mermaid 语法要点

```mermaid
C4Context
    title System Context Diagram
    Person(user, "User", "Description")
    System(system, "System", "Description")
    System_Ext(ext, "External", "Description")
    Rel(user, system, "Uses")

C4Container
    title Container Diagram
    Container(web, "Web App", "React", "UI")
    Container(api, "API", "Node.js", "Backend")
    ContainerDb(db, "Database", "PostgreSQL", "Storage")
    Rel(web, api, "Calls", "REST")
```

> ⭐ **一个很实用的细节**：技能明确说
> "从不使用有问题的 C4 Mermaid 插件"——
> 这是典型的 **Gotchas**（来自实际踩坑），
> 呼应 `skill-anatomy.md`（**`skill-authoring`**）的 Gotchas 最高信号原则。

## 与文档类技能的关系

```
documentation-skills.md（本篇所属）→ 文档写作的通用原则
本篇                              → ⭐ 架构图的抽象层级纪律
methodology-skills.md（domain-biz）→ 把成熟方法论编码成技能
```

## 自查

- [ ] 有从 Level 1 开始的强制检查点吗？
- [ ] 每层都写了"隐藏什么"吗？
- [ ] 红旗清单用了 STOP 措辞吗？
- [ ] 输出要求含标题、描述、带标签关系、边界、图例吗？
- [ ] 有 Gotchas 吗（如"不要用有问题的插件"）？
- [ ] 确定了受众与目的吗？
