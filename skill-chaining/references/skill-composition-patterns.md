# 多技能组合：五种模式与冲突解决

> ⭐ **一句话**：
> 单个技能有用，**多个技能智能组合是指数级强大**——
> 但糟糕的组合会制造冲突、矛盾与混乱。

## 目录

- [两条组合原则](#两条组合原则)
- [三种常见组合模式](#三种常见组合模式)
- [冲突：怎么发现、怎么解](#冲突怎么发现怎么解)
- [相关性测试：什么时候该删掉一个技能](#相关性测试什么时候该删掉一个技能)
- [预设与数量](#预设与数量)

---

## 两条组合原则

**① 单一职责**

```
✅ typescript-strict.md   TypeScript 规则
✅ testing-strategy.md    测试策略
✅ api-conventions.md     API 约定
✅ security-rules.md      安全规则
❌ ⭐ 一个 500 行的 mega-skill 覆盖一切
```

**② ⭐ 不矛盾原则**

```
冲突示例
  Skill A："服务层一律用 class"
  Skill B："一律用纯函数"
→ agent 会在两种写法间摇摆

解法：⭐ 定义清晰的优先级——高层级技能优先
```

> ⭐ 呼应 `composition.md` 与 `skill-refining` 的 `architecture-layering.md`：
> **组合的前提是职责不重叠**，重叠就要么定优先级要么合并。

---

## 三种常见组合模式

**① 全栈式**（Full Stack）

```
## Foundation
@company-standards.md
## Backend
@node-fastify.md · @prisma-database.md · @api-rest-conventions.md
## Frontend
@react-nextjs.md · @tailwind-styling.md · @accessibility.md
## Quality
@testing-vitest.md · @security-owasp.md · @documentation-jsdoc.md
```

**② 专家式**（Specialist）——针对一个深入领域

```
# API Security Specialist
@api-design.md · @authentication-jwt.md · @rate-limiting.md
@input-validation.md · @cors-policy.md · @error-handling.md
```

**③ 工作流式**（Workflow）——覆盖完整流程

```
# Development Workflow
@git-conventions.md · @branch-strategy.md · @code-review-process.md
@ci-cd-pipeline.md · @deployment-checklist.md
```

**并行组合**（另一种形态）：

```
用户："全面分析苹果公司"
  Skill A（财务分析）  营收、利润数据
  Skill B（舆情分析）  新闻、社媒情绪
  Skill C（技术面）    股价、技术指标
→ 三个技能并行执行，汇总后生成综合报告
```

> ⭐ **并行组合的关键**：三个技能**输出互不依赖**，
> 汇总时才需要契约——呼应 `composition.md` 的 I/O 契约。

---

## 冲突：怎么发现、怎么解

**⚠️ 冲突的四个信号**：

```
□ ⭐ agent 在两种做法之间犹豫
□ ⭐ 生成的代码前后不一致
□ ⭐ 出现 lint / 类型错误
□ 同一个问题换个问法答案就变
```

**三种解法**：

**方法 1：显式优先级**（写在主 CLAUDE.md 里）

```markdown
## Rule Priority
In case of conflict between skills:
1. security-rules.md always takes priority
2. company-standards.md next
3. Project skills last
```

**方法 2：合并**

```
两个技能重叠 → 创建一个合并技能，消解歧义

# Unified Style（取代 style-backend.md 与 style-frontend.md）
- 变量 camelCase（前后端统一）
- 类与组件 PascalCase
- 文件 kebab-case
```

> ⭐ 呼应 `skill-distribution` 的 `team-sharing.md` 与 troubleshooting 的"技能偷窃"：
> **重叠要么定优先级，要么合并——不能放着不管**。

**方法 3：限定作用域**

```markdown
## Application Context
- api-conventions.md  ⭐ 只适用于 /src/api
- component-rules.md  ⭐ 只适用于 /src/components
```

> ⭐ **方法 3 最优雅**——它让冲突根本不发生。
> 呼应 `skill-crafting` 的 `claude-md-vs-skill.md` 的 `paths:` 规则与
> `skill-refining` 的 `discovery-ux.md` 的按作用域划分。

---

## 相关性测试：什么时候该删掉一个技能

> ⭐ **对组合里的每一个技能问一句**：
> **"如果我删掉这个技能，产出质量会变吗？"**
> **不会 → 删掉。**

```
□ 移除技能之间的冗余
□ 在不损失清晰度的前提下压缩指令
□ ⭐ 移除与当前工作无关的技能
```

> ⭐ 这几乎与 `skill-refining` 的 `pruning.md` 的 no-op 测试是同一句话——
> 说明**"删掉看有没有变化"是跨场景通用的判断法**。

---

## 预设与数量

**按工作类型做预设**（开发者按当前任务激活对应预设）：

```
# preset-api.md
@base.md · @api-design.md · @database.md · @security.md · @testing.md

# preset-frontend.md
@base.md · @react.md · @tailwind.md · @accessibility.md · @testing.md

# preset-devops.md
@base.md · @docker.md · @ci-cd.md · @monitoring.md
```

> ⭐ **预设是管控技能数量的实用手段**——
> 呼应 `skill-governance` 的 `scale-effects.md`：候选池越大精确率越低，
> **按需激活预设比全部常驻好得多**。

**⭐ 数量建议**：

```
⭐ 实践中 5–8 个技能是大多数项目的甜蜜点
   超过之后收益递减
```

```
□ 从 2–3 个开始，逐步添加，持续观察冲突
□ ⭐ 目标不是拥有最多技能，而是拥有对当前上下文正确的组合
```

---

## 自查

```
□ 是否遵循单一职责（无 500 行 mega-skill）？
□ ⭐ 是否检查过技能之间的矛盾（如 class vs 纯函数）？
□ 组合模式是否匹配场景（全栈/专家/工作流/并行）？
□ 并行组合时各技能输出是否互不依赖、有汇总契约？
□ ⭐ 是否知道冲突的四个信号（犹豫/不一致/lint错误/答案飘）？
□ 是否设了显式优先级（安全规则最高）？
□ ⭐ 重叠技能是否合并或限定作用域（而非放着不管）？
□ 是否优先用"限定作用域"从根上避免冲突？
□ ⭐ 是否做过 no-op 测试（删掉看质量变不变）？
□ 是否做了预设（按需激活而非全部常驻）？
□ ⭐ 数量是否控制在 5–8 个？
□ 是否从 2–3 个起步、逐步添加？
□ 是否持续观察冲突信号？
□ 是否移除了与当前工作无关的技能？
```
