# 发布前该删掉的东西

> 相关：`skill-structuring` 的 `references-vs-assets.md` · `skill-structuring` 的 `enterprise-layout.md` ·
> 《skill-refining》的 `pruning.md`（逐句修剪）

---

## 目录

- [1. ⭐ 技能目录内不要有的文件](#1--技能目录内不要有的文件)
- [2. 不要有的内容](#2-不要有的内容)
- [3. 不要有的写法](#3-不要有的写法)
- [4. 发布前清理清单](#4-发布前清理清单)

---

## 1. ⭐ 技能目录内不要有的文件

规范明确点名的：

```
README.md · INSTALLATION_GUIDE.md · QUICK_REFERENCE.md · CHANGELOG.md
```

> ⭐ 技能只应包含 AI agent 完成工作所需的信息。
> 不应包含：关于创建过程的辅助上下文、安装与测试步骤、**面向用户的文档**。

**额外文档文件只会增加混乱**——它们会被当成候选参考资料，稀释检索。

**扫描器也会抓**：`skillscheck` 的 quality 类会检测
技能根目录的多余文件（README / LICENSE / Makefile），
以及 scripts/references/assets 里未被 SKILL.md 引用的孤儿文件。

---

## 2. 不要有的内容

| 不要 | 原因 |
|---|---|
| ⭐ **密钥、API key、密码** | 一律环境变量；扫描器会抓（AWS key、GitHub token、私钥、.env） |
| ⭐ **二进制文件** | 不可审计——`skill-structuring` 的 `directory-contract.md`：技能应当可读，正文就是审计轨迹 |
| **过大的资源** | 撑爆加载 / 超出预算 |
| ⭐ **时敏信息**（"截至 2024 Q4…"） | ⭐ 腐烂极快；用脚本取实时数据或直接省略 |
| **重复内容** | ⭐ 信息只应存在于 SKILL.md 或 references 之一，**不要两处都有** |
| **给人类看的安装步骤** | 放仓库根 README，不放技能内 |

---

## 3. 不要有的写法

| 不要 | 改成 |
|---|---|
| 面向用户的措辞（"I help you…"） | ⭐ 第三人称（"Generates…"） |
| 泛动词（"manage"、"handle"） | 具体动作动词 |
| 关键词堆砌 | 自然的触发描述 |
| 硬编码路径（/Users/...、C:\） | 占位符 / 相对路径 |
| 只描述格式而不给格式 | ⭐ 明确指定（JSON schema、Markdown 表格、纯文本） |

最后一条尤其重要：

```markdown
❌ "输出结构化的评审结果"
✅ "始终返回符合此精确 schema 的 JSON 对象。
    绝不在 JSON 块之外添加散文。"
```

> ⭐ **如果模型的默认格式习惯与技能要求冲突，必须显式压制它。**

---

## 4. 发布前清理清单

```
□ 无 README / CHANGELOG / INSTALLATION_GUIDE 等多余文件
□ scripts/references/assets 里无孤儿文件（都被 SKILL.md 引用）
□ 无密钥 / token / 私钥 / .env
□ 无二进制文件
□ 无时敏信息
□ SKILL.md 与 references 无重复内容
□ 描述用第三人称 + "Use when..." + 具体动词
□ 无硬编码路径
□ 输出格式被显式指定（不是"描述"）
□ 本地 markdown 链接全部可达（含锚点）
□ 代码栅栏全部闭合
□ 跑过 lint 工具（见 lint-tooling.md）
```

---

## 速查

| 抓到什么 | 意味着 |
|---|---|
| 技能根目录有 README | ⭐ 面向人类的文档放错地方 |
| references 有未被引用的文件 | 孤儿，稀释检索 |
| 扫出 AWS key | 密钥泄露 |
| 描述里有 "I help you" | 第一人称，触发效果差 |
| 有 /Users/... 路径 | 换机器就断 |
| 有"截至 2024 Q4" | 会腐烂 |
