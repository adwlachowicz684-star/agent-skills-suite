# 企业目录结构：按职责分区，让不同角色各审各的

> 相关：`skill-crafting` 的 `skill-structuring` 的 `directory-contract.md`（标准布局）·
> `structure/references-vs-assets.md`（两目录区别）·
> 《skill-distribution》的 `enterprise-registry.md`

---

## 目录

- [1. 完整结构](#1-完整结构)
- [2. ⭐ 分区的真正价值：分角色审查](#2--分区的真正价值分角色审查)
- [3. 五个收益](#3-五个收益)
- [4. 铁律：别把所有东西塞进 SKILL.md](#4-铁律别把所有东西塞进-skillmd)

---

## 1. 完整结构

```
skill-name/
├── SKILL.md              # 指令：引导 agent
├── scripts/              # 可执行逻辑
│   ├── validate_input.py
│   ├── transform_data.py
│   └── generate_report.py
├── resources/            # 结构化知识（机器可读）
│   ├── business_rules.md
│   ├── data_schema.json
│   └── terminology.md
├── references/           # 文档型知识（人/模型读）
│   ├── sop-production-reporting.md
│   └── compliance-policy.md
├── assets/               # 输出中要用的资源
│   ├── report-template.docx
│   ├── dashboard-layout.png
│   └── brand-guidelines.pdf
├── examples/             # 输入/输出样例
│   ├── sample-input.json
│   └── sample-output.md
├── tests/                # 测试用例
│   ├── test_cases.md
│   └── expected_outputs/
└── README.md             # 面向人类的分发说明（仓库根，非技能内）
```

---

## 2. ⭐ 分区的真正价值：分角色审查

这是企业场景里最被低估的收益：

| 目录 | 谁来审 |
|---|---|
| `scripts/` | 工程 |
| `references/`（合规政策） | ⭐ 法务 |
| `assets/`（品牌素材） | ⭐ 品牌团队 |
| `resources/`（业务规则） | 业务负责人 |

> ⭐ **目录结构让"审查"可以按职能切分**——
> 法务不需要读脚本，工程不需要审品牌规范。
>
> 如果全塞在一个 SKILL.md 里，**每次改动都要所有角色一起过**。

---

## 3. 五个收益

| 收益 | 说明 |
|---|---|
| **可靠性** | agent 知道去哪找指令、代码、示例、模板 |
| **可治理** | 团队按职能审文件 |
| **安全** | ⭐ 敏感文件可隔离、可限权、**可从 agent 访问范围中排除** |
| **可维护** | SOP 变了只改对应文件，不用编辑长系统提示词 |
| **可扩展** | 多个技能复用同一结构/命名/审查流程 |

第三条在企业里尤其关键——**分区是最小权限的物理前提**。

---

## 4. 铁律：别把所有东西塞进 SKILL.md

> ⭐ **SKILL.md 应该引导 agent，而不是变成一个知识垃圾场。**

```
✅ SKILL.md    → 指令 + 路由（薄）
❌ SKILL.md    → 全部规则 + schema + 模板 + 示例（厚）
```

规范的建议是：主文件保持精简，
把更深的内容放进 `scripts/`、`references/`、`assets/`。

**判据**（与 `skill-structuring` 的 `references-vs-assets.md` 同源）：
这段内容是需要被"理解"还是只被"使用"？
理解 → references/；使用 → assets/；执行 → scripts/。

---

## 速查

| 内容 | 位置 |
|---|---|
| 干什么、何时干 | SKILL.md |
| 确定性计算/转换 | scripts/ |
| 结构化业务规则 | resources/ |
| 合规/政策文档 | references/（法务审） |
| 输出模板/品牌素材 | assets/（零上下文成本） |
| 输入输出样例 | examples/ |
| 测试用例 | tests/ |
| 人类安装说明 | 仓库根 README（不在技能内） |
