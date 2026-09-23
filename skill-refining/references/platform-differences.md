# 平台差异：同一份技能在不同运行时上的差别

> 技能是开放标准，但**分发与执行方式各平台不同**。
> 这份讲实际会碰到的差别。

## 目录

- [两种执行形态](#两种执行形态)
- [两种上传方式](#两种上传方式)
- [挂载与版本](#挂载与版本)
- [目录约定](#目录约定)
- [跨平台的三条硬差别](#跨平台的三条硬差别)
- [自查](#自查)

## 两种执行形态

以 OpenAI Responses API 为例，它支持两种：

```
① 本地执行   —— 用 shell tool 的 local execution 模式
                 在你自己的机器上跑代码

② 托管执行   —— container-based，在容器里跑
```

> ⭐ 这个区分对技能设计有直接影响：
> **托管容器里没有你本机的凭据与文件**，
> 所以依赖本地环境的技能（读 `~/.ssh`、访问内网）在托管模式下会失败。

## 两种上传方式

**① 目录上传（multipart）**

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files[]=@./basic_math/SKILL.md;filename=basic_math/SKILL.md;type=text/markdown' \
  -F 'files[]=@./basic_math/calculate.py;filename=basic_math/calculate.py;type=text/plain'
```

注意：**每个 part 的路径都在同一个顶层目录内**。

**② zip 上传**

```bash
curl -X POST 'https://api.openai.com/v1/skills' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./basic_math.zip;type=application/zip'
```

> ⭐ **zip 必须包含单个顶层文件夹。**
> 这个约束和 Claude Code 插件的打包要求一致——
> 违反它是最常见的"上传成功但用不了"的原因。

**上传后的技能是版本化 bundle**——这点很重要，
它意味着**每次改动都是一个新版本**，天然可回滚。

## 挂载与版本

```json
{ "type": "shell",
  "environment": {
    "type": "container_auto",
    "skills": [
      { "type": "skill_reference", "skill_id": "<id>" },
      { "type": "skill_reference", "skill_id": "<id>", "version": 2 }
    ] } }
```

> ⭐ **可以显式指定 version，也可以不指定（用最新）。**

生产环境应该**总是指定**——
理由和 `skill-packs.md` 里的 pin 纪律完全一致：
**不指定版本，更新就是"某天发生的事件"而不是"某人做的决定"。**

## 目录约定

官方示例结构：

```
review-pr/
├── SKILL.md
├── references/
│   └── review-guidelines.md
├── scripts/
│   └── check-changes.sh
└── assets/
    └── review-template.md
```

```
references/   背景材料（读进上下文）
scripts/      ⭐ 可重复执行的动作（执行，不进上下文）
assets/       ⭐ 可复用模板（被消费）
```

> ⭐ `assets/` 这个目录在一些文档里被忽略，
> 但它是"模板类资源"的正确去处——
> 详见 `skill-structuring` 的 `resource-bundling.md`。

## 跨平台的三条硬差别

**① 发现机制的差别**

```
Claude Code / Copilot / VS Code / Cursor / Codex
  → 直接解析 SKILL.md，目录约定基本一致

OpenAI Agents API
  → ⭐ 会话从其沙箱中的目录发现技能
     （不是上传 bundle 那套）
```

**② description 的要求一致，但措辞示例不同**

官方给的对照（OpenAI）：

```
❌ "Helps with legal work."
✅ "Review and redline vendor agreements using the fallback clauses"
```

> 和 Anthropic 的说法完全同构：
> **描述必须同时说清"做什么"和"什么时候用"。**

**③ 每个请求能带几个技能**

```
⭐ API 请求最多支持 8 个技能
```

> 这是个硬约束，而且它解释了为什么要控制库规模——
> 详见 `trigger-eval-set.md` 里"召回随技能数退化"。

## 自查

```
[ ] zip 只有一个顶层文件夹？
[ ] 每个技能目录里都有 SKILL.md？
[ ] ⭐ 生产环境 pin 了 version？
[ ] 托管执行时，技能不依赖本机凭据/文件？
[ ] 用 references/ 放背景材料、scripts/ 放动作、assets/ 放模板？
[ ] description 同时说了"做什么"和"什么时候用"？
[ ] ⭐ 单次请求的技能数 ≤ 8？
```

## 一条关于"开放标准"的提醒

> 技能"兼容开放标准"意味着**格式**可移植，
> ⭐ **不意味着行为可移植**。

同一个 SKILL.md 在 Claude 和 Codex 上的表现可能不同，
原因正是 `cross-model.md` 讲的那条：
**提示词是模型相关的**。

所以：**格式一次写就到处能读，但触发与遵循仍要各平台各测一遍。**
