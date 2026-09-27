---
name: skill-patterns
description: >
  通用的技能设计原则、反模式与结构模式。用于决定一个技能该用什么结构
  （A–E 五模式、六层模型、五类设计范式、SOLID 映射、I/O 契约四原则）、
  识别反模式（九类/七类/六类反模式与常见错误清单）、处理冲突优先级与
  多技能组合架构。
  Do NOT use for 按具体业务领域写技能（用 skill-domains）、完整可抄的源码
  （用 skill-gallery）、从零写第一个技能（用 skill-authoring）、正文构件写法
  （用 skill-crafting）、评估与治理（用 skill-evaluating / skill-governance）。
---

# 技能设计范式库

> 定位：**跨领域通用的设计原则、结构模式与反模式**。
> 每份讲骨架、结构、反模式——**不绑定具体业务领域**。
> ⭐ **要按某个具体职能/行业写技能 → 《skill-domains》**
> 要找「怎么从零写一个技能」→ 《skill-authoring》

## 边界

- 用于：**结构模式** · **设计原则** · **反模式** · **冲突优先级** · **组合架构**
- ⭐ 用于：**测试、文档、评审、重构、客服、合规等具体领域** → 《skill-domains》
- 不用于：从零写第一个技能 · 正文构件写法 · 评估与治理

## 强制工作流

1. **确认任务类型**——用户要做的技能属于哪一类？
2. **读对应范式**（下面路由表；不确定就读 `methodology-skills`）
3. ⭐ **重点看三个部分**：骨架 · 必编码项 · 反模式
4. **套用判定表**——把「模型自己猜」变成「查表」
5. **补 Gotchas**——你团队踩过的坑，这是技能最有价值的部分
6. **跑 `validate_skill.py`**，然后跑 5+5 触发测试

## 路由表
| `enterprise-three-layer-skeleton.md` | ⭐⭐★★★ 三层骨架；★前置指纹(规划期排除)；元描述=意图+前置+后置 |
| `skill-anatomy-antipatterns.md` | ⭐⭐ description 触发/正文教；绝不在 description 总结工作流 |
| `six-pitfalls-selfcheck.md` | ⭐⭐★★★ 沉积（打架的旧值）；★空转/重复；★禁令改写顺序 |
| `six-anti-patterns-pitfalls.md` | ⭐⭐⭐ 六反模式症状→药方 + 六条安全红线 |
| `common-mistakes-checklist.md` | ⭐ 常见错误清单：描述/正文/结构/输出/维护五层 |
| `anti-patterns-catalog.md` | ⭐ 五类反模式总目（含模型已知信息、嵌套引用） |
| `anti-pattern-section.md` | ⭐⭐ 反模式章节写法 |
| `reusability-over-specification.md` | ⭐⭐⭐⭐⭐ 先探测不先写（第五个同构场景）；⭐⭐⭐⭐⭐ 三层拆分通用/领域/项目；⭐⭐⭐⭐⭐ 改一个词测试 |
| `four-design-principles-io-contract.md` | ⭐⭐⭐⭐ 四项原则；★★无状态此前未列为原则 + schema.yaml 数据契约 |
| `conflict-precedence-four-types.md` | ⭐⭐⭐ 四层优先级(事实是约束/技能是指导)+四种冲突类型 |
| `shared-service-skill.md` | ⭐⭐⭐ 共享服务技能：总是返回有效输出或明确错误 |
| `seven-anti-patterns-scale.md` | ⭐⭐ 规模化七反模式；⭐⭐⭐ Markdown 指令不是访问控制 |
| `skill-families-nine.md` | ⭐⭐ 九类技能；跨类最难用好，一类做到底 |
| `self-containment-rewrite.md` | ⭐⭐⭐⭐⭐ 三招迁移序列；⭐⭐⭐⭐⭐ 拆分判据：重写需要几份文档；⭐⭐⭐⭐⭐ 抽一个出来的诊断法 |
| `skills-are-programs.md` | ⭐⭐⭐⭐ 技能即程序，运行时是 LLM；⭐⭐⭐⭐⭐ 1024 字符决定存不存在；不该存在的四类文件 |
| `solid-for-skills.md` | ⭐ 软件设计原则迁移：SOLID 映射、两张图、组合代价 |
| `why-six-layers.md` | ⭐ 六层结构：目标/输入/流程/格式/自检/FAQ |
| `skill-overrides-audit.md` | ⭐ 同名覆盖与冲突：三级命名空间、审计、my- 前缀 |
| `skeleton-template.md` | ⭐ 可直接抄的骨架（六必含小节 + 触发调优） |
| `instruction-craft.md` | ⭐ 正文写作：祈使句、钉死格式、讲为什么 |
| `context-budget-math.md` | ⭐ 预算算术：96% 从哪来、压缩会驱逐技能 |
| `team-registry-governance.md` | ⭐ 团队分发：manifest、pin、owner、hub-and-spoke |
| `structure-modes-abcde.md` | ⭐ 五种结构模式 A–E（含各自行数目标） |
| `six-step-creation.md` | ⭐ 六步创建法 + 五阶段学习路径 |
| `publish-checklist-20.md` | ⭐ 发布前 20 项（0–2 分制，28 分才发） |
| `golden-rules-failure-modes.md` | ⭐ 黄金规则：每条失败模式配一条机械规则 |
| `feedback-loop-design.md` | ⭐ 反馈环：做→检查→修，规则升级为代码 |
| `ten-common-mistakes.md` | ⭐ 十条常见错误与四条最该记住的 |
| `skill-type-testing.md` | ⭐ 按类型选测法（Pattern 测 near-miss、Discipline 加压力） |
| `review-checklist.md` | ⭐ 十项自检 + 反转测试 + 只记三条 |
| `nine-anti-patterns.md` | ⭐ 九个反模式：症状 / 根因 / 修法 |
| `meta-skill-factory.md` | ⭐ 元技能：让 agent 自己写技能（含人在环路） |
| `knowledge-delta-checklist.md` | ⭐ 知识增量清单：该有的是模型不知道的 |
| `five-design-patterns.md` | ⭐⭐ 五种设计模式 + 选型决策树（Tool Wrapper 起步） |

| 文档 | 内容 |
|---|---|

## 通用规律（跨范式）

读任何一份前先看这四条，它们是所有范式的共性：

1. ⭐ **把「模型自己猜」变成「查表」**——判定表是最有效的编码形式
   （公式选择表、图表选择表、味道→手法表、框架选型表，都是这个）
2. ⭐ **确定性部分交给脚本**——能算的别让模型生成
   （Changelog、版本号、覆盖率、打分）
3. ⭐ **Gotchas 是最高信号**——来自真实踩坑，几乎不可能通过
   no-op 测试，修剪时永远别动它
4. ⭐ **写明「不做/不该用」**——没有边界的技能会被用错场景

## 何时不用（边界）

- ❌ **Do NOT** 用本技能查找领域技术知识本身——
  如「SQL 该不该建索引」「饼图最多几块」「Unity 的 Awake/Start 区别」。
  本技能讲的是**这类技能怎么设计**，不是领域答案。
- ❌ **Do NOT** 用本技能从零创建第一个技能——去 `skill-authoring`。
- ❌ **Do NOT** 用本技能查正文构件写法（形态、目录、脚本、验证）——
  去 `skill-crafting`。
- ❌ **Do NOT** 用本技能做评估、治理、安全合规——
  去 `skill-evaluating` / `skill-governance`。
- ❌ **Do NOT** 直接照抄范式而跳过第 5 步——
  **没有你团队 Gotchas 的技能是通用废话**。
