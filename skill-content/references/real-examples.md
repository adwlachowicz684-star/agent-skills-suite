# 真实技能拆解

## 目录

- [六类真实技能](#六类真实技能)
- [五种设计模式](#五种设计模式)
- [四个最小模式](#四个最小模式)
- [最值得抄的一个范式](#最值得抄的一个范式)

---

## 六类真实技能

来自某企业脱敏后公开的六份技能，覆盖六种典型场景。

### ① 框架规范类：`server-common-go-standard`

**问题**：没有技能时，AI 是否遵守项目规范全靠开发者提醒。

```
server-common-go-standard/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── api-gateway-protobuf.md
    ├── bus-cron-workers.md
    ├── ci-deploy.md
    ├── config-observability.md
    ├── data-cache-clients.md
    ├── project-shape.md
    ├── runtime-registration.md
    └── verification.md
```

**流程**：先定位项目根（`go.mod`、`main.go`）→ 若存在则读 `AGENTS.md` →
**确认当前仓库仍与参考文件匹配后才应用规则**。

> ⭐ **设计要点：事实边界**——只记录经多项目验证的规则；
> **技能与活代码冲突时以活代码为准**。

### ② 业务能力类：`integrate-rank-service`

**目的**：引导复用内部公共排行服务，而不是重新实现排行逻辑。

```
references/ requirement-intake · service-boundary · config-model
            integration-playbook · expression-and-extension
            troubleshooting · cases/directional-pair-rank
```

**边界**：明确"何时用"（新榜/活动榜/方向对榜）和"何时不用"
（纯前端样式、一次性 SQL 排序、要求独立隔离的系统）。

**输出**：一份清单——缺失输入、复用可行性、维度支持、配置顺序、
代码入口、验证步骤、排错优先级。

> ⭐ **设计要点：`cases/` 目录存真实案例**，用具体案例说明抽象规则。

### ③ 工程流程类：`archery-ddl-workflow`

**目的**：产出能直接提交到 Archery 审核系统的 MySQL DDL，
避免"写完→被拒→再改"的循环。

**必填输入**：新建表还是改表、业务键、重试用段、状态列……
**五步流程**：从业务契约出发 → 设计最小列集 → 翻译成 Archery 友好的 SQL
（显式注释、默认值、排序规则、索引命名）→ 对照常见驳回原因自检 →
若影响线上写入则加回滚/风险说明。

**强制规则**：禁止 `IF EXISTS` / `IF NOT EXISTS`；
单列 id 主键（例外须批准）；索引命名规范。

> ⭐ **设计要点：把"审核系统的驳回原因"直接编码进技能**
> ——这就是踩坑章节（Gotchas）的价值。

### ④ 接口契约类：`interface-contract-docs`

**目的**：生成/补全/审计前后端契约文档，让前端拿到就能用。

**关键约束**：强制输出文件落在 `/docs/delivery/`，用规范的命名方案。

> ⭐ **设计要点：输出位置也是契约的一部分**。不确定"写到哪"是常见的失败点。

### ⑤ 测试评审类 / ⑥ 前端 D2C 类

同类思路：把评审维度清单化，把设计稿转代码的规则显式化。

---

## 五种设计模式

| 模式 | 解决什么 | 结构 |
|---|---|---|
| **Tool Wrapper** | 让 agent 成为某个库的专家，但**不把 API 文档硬编码进提示词** | 提到关键词才加载 `references/conventions.md` |
| **Generator** | 产出结构化文档 | `assets/` 放输出模板 + `references/` 放风格指南，填模板 |
| **Reviewer** | 把"查什么"和"怎么查"分开 | `references/review-checklist.md` 清单 + 严重度分级 + 说清 why + 给具体修法 |
| **Inversion** | **先访谈再产出** | 严格门禁："未完成所有阶段前不得开始设计" |
| **Pipeline** | 多步串联 | 串起上述模式 |

**Tool Wrapper 示例**：

```markdown
你是 FastAPI 开发专家。
## 核心约定
加载 `references/conventions.md` 获取完整的最佳实践清单。
## 审查代码时
1. 加载清单  2. 逐条比对  3. 每条违规引用具体规则并给出修法
```

> 关键：**文档留在 references/，只有命中关键词才加载**——零上下文成本直到被访问。

**Reviewer 的输出结构**（可直接抄）：

```markdown
**Summary**  整体质量评估
**Findings** 按严重度分组（error → warning → info）
**Score**    1–10 分 + 简短理由
**Top 3 Recommendations** 最有价值的改进
```

每条发现必须：标注行号 · 分级 · **说清为什么是问题** · 给出具体修法。

**Inversion 的门禁写法**：

```markdown
DO NOT start building or designing until all phases are complete.
## Phase 1 — 问题发现
- Q1: 这个项目为用户解决什么问题？
...
```

---

## 四个最小模式

### ① 最小可用技能（15 行就够）

```yaml
---
name: commit-message
description: 生成符合团队格式的 conventional commit 信息。
  在提交代码或用户要求创建 commit 时使用。
---
# Commit Message Format
使用 conventional commits，类型：
- feat: 用户可见的新功能
- fix: bug 修复
- refactor: 既不修复也不新增的改动
- docs / test
格式：type(scope): 小写摘要，72 字符内
非显而易见的改动加正文。适用时引用 issue："Closes #123"
```

> **不解释什么是 commit message——agent 知道。只加你团队独有的东西。**

### ② 渐进式披露

主文件只给工作流 + 指向细节的指针。参考文件**在被访问之前零成本**。

### ③ 输入输出示例

```markdown
## Example
**Input** (git log):
abc123 feat: add dark mode toggle
def456 fix: correct date parsing
**Output**:
## v2.4.0
### New
- 深色模式现已在 设置 > 外观 中提供
```

> 注意输出用的是**用户语言**（"深色模式现已提供"），不是开发者黑话
> （`feat: add dark mode toggle`）。这个转换必须靠示例才能锁住。

> **一个例子通常够，两个更好，三个以上通常是过度。**

### ④ 反馈循环

```markdown
1. 生成迁移文件
2. 检查生成的 SQL
3. 运行校验：`npx prisma validate`
4. **校验失败则修复后回到第 3 步**
5. 仅当校验通过才继续
```

> ⭐ **"回到第 3 步"是大多数技能作者忘记的关键指令。**
> 没有显式指令要求循环，agent 倾向于**校验一次就往下走，不管结果**。

`disable-model-invocation: true` —— 数据库迁移不希望被自动触发。

---

## 最值得抄的一个范式

一份交付给多个客户的 release-notes 技能：

```
release-notes/
├── SKILL.md              ← 流程（不变）
├── reference/
│   └── voice-guide.md    ← 只改这里（每个客户不同）
└── scripts/
    └── fetch-merged-prs.sh
```

> **逻辑在正文，品味在 reference，管道在 script。**
> 换个客户只换 voice-guide.md，**SKILL.md 一行不动**。

**这就是可复用资产生存下来的原因**：写一次逻辑，在客户已有的任何 agent 里跑。

**判断你的技能是否做到**：换一个项目/客户，你需要改 SKILL.md 吗？
需要 → 说明流程和数据还没分离（见 `skill-refining` 的 `splitting.md` 的"与数据分离"）。

---

## 自查

```
□ 是否把"审核/驳回原因"这类踩坑经验编码进去了？
□ 输出位置是否也是契约的一部分？
□ 是否有 cases/ 或具体案例说明抽象规则？
□ 是否用了 Tool Wrapper（库文档放 references 而非硬编码）？
□ 示例是否展示了"用户语言 vs 开发者黑话"的转换？
□ 循环是否有"回到第 N 步"的显式指令？
□ 换项目时是否需要改 SKILL.md？（需要就该分离数据）
```
