# 领域分类法：当技能多到需要检索

> 一个网络安全技能库有 754 个技能、26 个域。
> 它证明了两件事：**领域分类法能规模化**，以及**元数据标签决定检索质量**。

## 目录

- [26 个域的规模分布](#26-个域的规模分布)
- [规模化检索的算术](#规模化检索的算术)
- [frontmatter 里的领域元数据](#frontmatter-里的领域元数据)
- [正文的五个固定章节](#正文的五个固定章节)
- [对通用技能的启示](#对通用技能的启示)

## 26 个域的规模分布

| 域 | 数量 | 域 | 数量 |
|---|---|---|---|
| 云安全 | 60 | 事件响应 | 25 |
| 威胁狩猎 | 55 | 红队 | 24 |
| 威胁情报 | 50 | 渗透测试 | 23 |
| Web 应用安全 | 42 | 终端安全 | 17 |
| 网络安全 | 40 | DevSecOps | 17 |
| 恶意软件分析 | 39 | 钓鱼防御 | 16 |
| 数字取证 | 37 | 密码学 | 14 |
| 安全运营 | 36 | 零信任架构 | 13 |
| 身份与访问管理 | 35 | 移动安全 | 12 |
| SOC 运营 | 33 | 勒索软件防御 | 7 |
| 容器安全 | 30 | 合规与治理 | 5 |
| OT/ICS 安全 | 28 | 欺骗技术 | 2 |
| API 安全 | 28 | | |
| 漏洞管理 | 25 | **合计** | **754** |

> ⭐ **分布本身就是信息**：云安全和威胁狩猎各占 60/55，
> 而欺骗技术只有 2 个。**头部域值得细分，长尾域该合并。**

## 规模化检索的算术

官方给出的成本模型：

```
扫描阶段：每个技能只读 frontmatter，约 30 tokens
执行阶段：完整加载 500–2,000 tokens

754 个技能 × 30 tokens ≈ 22,620 tokens
⭐ 单次扫描全部技能，不撑爆上下文窗口
```

**实际检索过程**：

```
用户："分析这个内存转储，找凭证窃取的迹象"

1. 扫描 754 个技能的 frontmatter（~30 tokens each）
2. 按 tags / description / domain 匹配，识别出 12 个相关
3. ⭐ 只加载 top 3 的完整内容：
   · performing-memory-forensics-with-volatility3
   · hunting-for-credential-dumping-lsass
   · analyzing-windows-event-logs-for-credential-access
4. 按 Workflow 章节逐步执行
5. 用 Verification 章节验证结果，映射到 ATT&CK T1003
```

> ⭐ **30 : 2000 = 1:67 的成本比**——
> 这就是渐进式披露在规模化场景下的全部价值。

呼应 `scale-effects.md`（**`skill-governance`**）：
1,236 个技能实测吃掉 36.6% 上下文——
⭐ **那是因为它们的 description 写得又长又差；
而这个库用 30 tokens 的精简 frontmatter 换来了 754 个的可检索性。**

## frontmatter 里的领域元数据

真实示例：

```yaml
name: performing-memory-forensics-with-volatility3
description: >-
  Analyze memory dumps to extract running processes, network connections,
  injected code, and malware artifacts using the Volatility3 framework.
domain: cybersecurity
subdomain: digital-forensics
tags: [forensics, memory-analysis, volatility3, incident-response, dfir]
atlas_techniques: [AML.T0047]
d3fend_techniques: [D3-MA, D3-PSMD]
nist_ai_rmf: [MEASURE-2.6]
nist_csf: [DE.CM-01, RS.AN-03]
version: "1.2"
author: mukul975
license: Apache-2.0
```

**五类元数据各自的作用**：

| 字段 | 作用 |
|---|---|
| `domain` / `subdomain` | ⭐ 两级分类，粗筛 |
| `tags` | ⭐ 检索主力——多标签允许一个技能从多个角度被找到 |
| `atlas_techniques` 等标准映射 | 与外部知识体（ATT&CK/D3FEND/NIST）对齐 |
| `version` / `author` | 溯源与生命周期 |
| `license` | ⭐ 分发合规（呼应 `licensing-ip.md`，**`skill-refining`**） |

> ⭐ **`tags` 是被低估的字段**。
> 一个技能只能有一个 domain，但可以有多个 tag——
> 而用户是从不同角度描述需求的。

## 正文的五个固定章节

```
1. When to Use      —— 触发条件
2. Workflow         —— 分步技术流程
3. Verification     —— ⭐ 怎么验证结果
4. References       —— 标准映射（ATT&CK 等）
5. Gotchas          —— ⭐ 见下
```

目录结构也固定：

```
skills/<name>/
├── SKILL.md                 # 定义
├── references/
│   ├── standards.md         # ATT&CK / ATLAS / D3FEND / NIST 映射
│   └── workflows.md         # 深度技术流程
├── scripts/process.py       # 可用脚本
└── assets/template.md       # ⭐ 填好的检查单与报告模板
```

**官方对价值来源的定位值得抄**：

> ⭐ **每个技能编码的是真实从业者的工作流，
> 不是生成的摘要。**

以及效果对比：

```
没有技能：agent 猜工具命令，漏掉关键步骤
有了技能：agent 按资深分析师会用的同一本手册走
```

## 对通用技能的启示

**① domain + tags 是规模化的前提**

```
技能少于 20 个 → 靠 description 就够
技能超过 50 个 → ⭐ 必须有结构化分类字段
技能超过 200 个 → ⭐ 再加标准映射（行业标准/内部规范编号）
```

**② "填好的模板"比"空白模板"有用**

注意 `assets/template.md` 的定位是
**"filled-in checklists and report templates"**——
已填好的检查单，不是空表。

呼应 `examples.md` 那条：**agent 对具体结构模式匹配得很好**。

**③ 长尾域要合并，不要为对称而凑数**

```
合规与治理 5 个、欺骗技术 2 个
→ 它们单独成域的成本高于收益
```

**④ Verification 是独立章节，不是散在步骤里**

呼应 `grounding-verification.md`（**`skill-crafting`**）：
剩余错误的主要来源是落地与验证**支持不足**——
把它做成独立章节，就不容易被省略。

## 自查

- [ ] 技能超过 50 个了吗？有 domain/tags 字段吗？
- [ ] 每个技能有多个 tag 吗？（允许从多个角度被找到）
- [ ] frontmatter 控制在扫描成本内了吗？（目标 ~30 tokens）
- [ ] 有独立的 Verification 章节吗？
- [ ] assets 里是"填好的模板"还是空表？
- [ ] 长尾域合并了吗，还是为了对称在凑数？
