# 团队约定与 PR 评审清单

> 相关：《skill-distribution》的 `team-sharing.md` ·
> `adoption-metrics.md` · 《skill-governance》的 `retirement-pipeline.md`

---

## 目录

- [1. ⭐ 四条原则与检查清单](#1--四条原则与检查清单)
- [2. ⭐ 技能等级分层（混合水平团队）](#2--技能等级分层混合水平团队)
- [3. ⭐ 提交约定与 PR 结构](#3--提交约定与-pr-结构)
- [4. ⭐ 评审标签与反馈写法](#4--评审标签与反馈写法)
- [5. 落地方式](#5-落地方式)

---

## 1. ⭐ 四条原则与检查清单

```
原则 1：能力扩展都用 SKILL.md 写
        ⭐ 不要用平台专属格式（LangChain Python / OpenAI JSON / Semantic Kernel C#）
        ⭐ 2025-02 Agent Skills 协议确认后，这些正在变成"历史包袱"

原则 2：⭐ 渐进式披露是核心
        章节控制在 200 行内，超过 300 行拆 references/
        ⭐ 三层叠加形成 token 经济性：
           frontmatter 50 tokens + 章节 2K + 附录按需
        ⭐ 三个度量：加载率 5-15% / 命中率 70-90% / 维护成本 1-2

原则 3：⭐ 危险操作双保险
        ⭐ 低频高风险操作（rollback / db-migrate / force-push）
           ⭐ 必须配 disable-model-invocation: true + Hook 二次拦截
        ⭐ 单层防御不够，双保险才能兜底

原则 4：⭐ 进 git + 配 PR review
        ⭐ 技能是工程资产，不是个人草稿
        所有修改进 git，所有变更 PR review
        → 保证团队用的技能一致、可追溯、可回滚
```

**PR review 模板**（四项，任何一项不合格打回）：

```
1. [ ] 能力扩展都用 SKILL.md 写（没用平台专属格式）
2. [ ] 章节 200 行内、超过拆 references/（加载率 5-15%）
3. [ ] 危险操作加 disable + Hook 双保险
4. [ ] 进 git + 配 PR review
```

---

## 2. ⭐ 技能等级分层（混合水平团队）

按"允许做什么 / 需要什么证据 / 什么时候停"三要素分层：

| 等级 | 允许的工作 | 必需的证据 | ⭐ 停止条件 |
|---|---|---|---|
| **L1 机械性改动** | 重命名、格式化、依赖安全的重构、文档更新、简单测试 | 既有测试命令 + 一个针对性检查 | ⭐ 行为变化不清晰 / agent 无法解释的失败测试 / 触碰安全敏感代码 |
| **L2 有界产品改动** | 既有模式下的小功能、带复现的 bug 修复、API client 更新、组件行为变更 | ⭐ 修复前有失败测试或复现，修复后测试通过，行为变化需评审说明 | 新架构 / 新外部依赖 / 数据迁移 / 鉴权变更 / 支付变更 |
| **L3 架构敏感改动** | 规划、方案对比、测试脚手架、迁移草稿、风险清单 | ⭐ 实施前设计说明经资深评审批准 | 生产数据访问 / 凭据处理 / 公开 API 契约变更 / 跨服务发布 |

> ⭐ **"停止条件"这一列是最有价值的部分**——
> 多数规范只写"允许做什么"，**不写"做到什么程度必须停"**，
> 于是 agent 会一路冲进它不该碰的区域。

**验证循环**：

```
· 编辑前先读相关的 AGENTS.md
· ⭐ 在 PR 描述里声明意图的技能等级
· 做最小的自洽改动
· 跑仓库检查：npm test / npm run lint / npm run typecheck
· ⭐ 粘贴命令结果，或说明为什么某条跑不了
· ⭐ 不要隐藏失败的检查——总结失败并说明下一步需要人做什么决定
```

**MCP 边界**（示例）：

```
GitHub    只读 issue 与 PR；只在当前仓库建分支与 PR
Jira/Linear  只读
数据库    staging 只读，除非维护者临时授权
Slack     只读已关联的工程频道，⭐ 不自动发帖
Secrets   ⭐ 绝不请求、打印、存储或转换
```

---

## 3. ⭐ 提交约定与 PR 结构

**Conventional Commits**：

```
<type>(<scope>): <description>
```

type：`feat` · `fix` · `docs` · `test` · `refactor` · `chore`

scope 建议：`auth` · `search` · `publish` · `review` · `namespace` ·
`governance` · `deploy` · `ci` · `frontend` · `scanner`

示例：

```
fix(auth): resolve session cookie conflict in device flow
feat(publish): support security scan before review submission
docs(skill-protocol): add nested SKILL.md discovery rules
test(search): verify jieba analysis with Chinese skill descriptions
refactor(storage): simplify LocalFile path normalization
```

**Pre-PR Checklist**：

```
□ make test-backend-app      后端测试通过
□ make typecheck-web         前端类型检查通过
□ ⭐ 若 API 变更：跑过 make generate-api，且生成的 schema.d.ts 已提交
□ make staging               冒烟测试通过
□ ⭐ 遵循既有模块边界与依赖方向
□ 为新行为补充/更新测试
□ ⭐ API、鉴权流程、部署或运维工作流变更时，更新设计文档
```

**PR 正文五段**：

```
What    改了什么
Why     动机（链接 issue）
How     关键实现细节（⭐ 尤其是不显然的决策）
Testing 怎么验证它能工作
Impact  ⭐ 破坏性变更、迁移说明、发布注意事项
```

---

## 4. ⭐ 评审标签与反馈写法

**四类标签**（让每条意见的阻断级别一目了然）：

```
Nitpick     小建议，不阻断
Question    需要澄清
Suggestion  建议性改进
Issue       ⭐ 合并前必须处理
```

**评审惯例**：

```
· ⭐ 建议改动约定时，引用具体的 AGENTS.md 规则
· 后端代码：检查依赖方向是否违反整洁架构
· 前端代码：检查 API 变更后 OpenAPI 类型是否重新生成
· ⭐ 不要为风格bike-shedding（交给 linter）
· 优先功能与安全性，考虑技术债权衡
```

**好反馈 vs 坏反馈**：

```
✅ "Great use of the factory pattern here! This makes the code much
    more testable. Consider extracting the validation logic into a
    separate validator class for even better separation of concerns."
✅ "Question: What happens if the API returns a 429? Should we
    implement exponential backoff here?"
✅ "Suggestion: Instead of nested if statements, consider early returns."

❌ "This is wrong."
❌ "Why didn't you use X pattern?"
❌ "This code is terrible."
❌ 不打招呼直接重写整段
```

**PR 体积**：

```
>500 行 → ⭐ 要求拆成更小的 PR
          （难以彻底评审，bug 溜过去的概率更高）
```

**自审清单**（提交前）：

```
□ 用新鲜的眼睛重读改动
□ 本地跑测试
□ 检查测试覆盖
□ ⭐ 移除调试语句
□ 更新文档
□ 描述性提交信息
□ PR 描述清晰
□ 考虑评审者的视角
```

**团队定制项**（按你们情况加）：

```
技术特定检查（React hooks 规则、async/await 模式）
业务逻辑校验（定价计算、数据转换）
合规要求（GDPR / HIPAA / SOX）
公司编码标准
性能基线（API 响应 <200ms）
```

---

## 5. 落地方式

> ⭐ **采用要轻量**：

```
① 技术负责人提出第一版规则
② ⭐ 两位高频评审者编辑它
③ ⭐ 团队在三个真实 PR 上试用后，才叫它"标准"
④ ⭐ 根版本放 AGENTS.md
⑤ ⭐ 更严格的本地版本放在高风险代码旁
   （services/billing/AGENTS.md · infra/AGENTS.md · packages/auth/AGENTS.md）
```

**让约定活下来的那条评审规则**：

> ⭐ **agent 参与编写的 PR，在评审者能找到
> 声明的技能等级、改动文件、验证输出、以及用到的 MCP 访问之前，不能被批准。**
>
> ⭐ 如果 PR 没声明技能等级和验证证据，
> 评审者先要这些，**而不是先讨论代码本身**。

**技能交接（当重复工作流稳定后）**，提议做成可复用技能时要含：

```
name · description · inputs ·
exact steps · verification commands · ⭐ known failure modes
```

> ⭐ **"已知失败模式"这一项最常被漏**，
> 但它正是 `skill-types.md` 说的 Gotchas，也是技能价值最高的部分。

---

## 速查

```
四原则：
□ SKILL.md 写能力扩展，不用平台专属格式
□ ⭐ 章节 200 行内，>300 拆 references/
□ ⭐ 危险操作：disable + Hook 双保险
□ ⭐ 进 git + PR review（工程资产，不是个人草稿）

三度量：加载率 5-15% / 命中率 70-90% / 维护成本 1-2

等级分层：
□ L1 机械（重命名/格式化）
□ L2 有界（小功能/带复现的修复）
□ L3 架构敏感（需设计说明经资深批准）
□ ⭐ 每级都要写"停止条件"

PR：
□ conventional commits（type + scope）
□ ⭐ API 变更要提交生成的 schema.d.ts
□ 五段：What/Why/How/Testing/⭐Impact
□ ⭐ >500 行要求拆
□ ⭐ 自审要移除调试语句

评审：
□ 四标签：Nitpick/Question/Suggestion/⭐Issue
□ ⭐ 引用具体 AGENTS.md 规则
□ ⭐ 不为风格 bike-shedding
□ ⭐ 反馈给替代方案，不只说"错"

落地：
□ ⭐ 负责人起草 → 两位评审者编辑 → 三个真实 PR 试用
□ ⭐ 根版放 AGENTS.md，严格版放高风险目录旁
□ ⭐ 未声明技能等级+验证证据的 agent PR 不予批准
□ ⭐ 技能交接要含 known failure modes
```

**一句话**：

> ⭐ **规范只写"允许做什么"是不够的——
> 必须写"做到什么程度必须停下来"。**
