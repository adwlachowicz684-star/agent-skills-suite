# Agent Skills Suite

一套关于「如何创建 Agent 技能（SKILL.md）」的方法论知识库。

**不是**领域技术手册，而是**教你怎么把方法论写成技能**的手册。
领域实例（Unity / Godot / SQL / 图表选型等纯技术知识）已单独归档，不在此仓库。

## 现状

- **10 个技能，318 份 references，约 56,000 行 Markdown**
- 全部通过自举校验（0 错误 0 警告），无孤立文件

## 十个技能

| 目录 | 份数 | 负责 |
|---|---|---|
| `skill-authoring` | 30 | 从零写：识别模式、六步流程、description 写作 |
| `skill-crafting` | 37 | 正文构件：指令形态、输出契约、脚本、前置门禁 |
| `skill-structuring` | 19 | 物理结构：目录布局、frontmatter、加载机制、命名 |
| `skill-refining` | 28 | 优化：瘦身、拆分、上下文预算、版本迭代 |
| `skill-distribution` | 28 | 发布与推广：打包、依赖锁、团队约定、度量 |
| `skill-evaluating` | 34 | 评估：四层测试金字塔、A/B、trace 排错、Rubric |
| `skill-governance` | 30 | 治理：安全、合规、遥测、成本、生命周期 |
| `skill-orchestration` | 35 | 编排：多技能组合、fork 隔离、子代理 |
| `skill-selection` | 23 | 选型：该不该做成技能（vs RAG / 微调 / MCP） |
| `skill-patterns` | 54 | 范式库：按任务类型归纳的设计模式 |

## 校验

每个技能自带校验脚本：

```bash
python3 skill-authoring/scripts/validate_skill.py skill-authoring
```

## 阅读版

```bash
python3 build_reader.py   # 生成 skills-suite-reader.html
```

单文件 HTML，侧边栏导航 + 全文搜索，双击即开。

## 三条最重要的结论

1. **技能一旦激活，指令会留在对话里持续消耗上下文**——步骤措辞要能承受被反复看到
2. **把破坏性拦截写进技能是表演**——Hooks 用于模型不可被信任去遵守的事
3. **改了技能不生效，八成是文件层问题**（名字对不上、大小写错），而且它不报错
