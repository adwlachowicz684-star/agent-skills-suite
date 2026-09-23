# 跨平台可移植：破坏它的三件事

> 相关：《skill-authoring》的 `cross-model.md` ·
> 《skill-distribution》的 `distribution-three-ways.md` ·
> `packaging.md`

---

## 目录

- [1. ⭐ 目录地图](#1--目录地图)
- [2. ⭐ 破坏可移植性的三件事](#2--破坏可移植性的三件事)
- [3. 字段支持度分级](#3-字段支持度分级)
- [4. 触发可靠度实测差异](#4-触发可靠度实测差异)
- [5. ⭐ 最大可移植子集](#5--最大可移植子集)

---

## 1. ⭐ 目录地图

| 客户端 | 目录 |
|---|---|
| Claude Code | `.claude/skills/` / `~/.claude/skills/` |
| Codex CLI | `.codex/skills/` / `~/.codex/skills/` |
| Gemini CLI | `.gemini/skills/` / `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/`（仓库内） |
| Cursor | `.cursor/rules/`（仓库内）或 `~/.cursor/skills/` |
| ⭐ **中性位置** | ⭐ **`.agents/skills/`** |

> ⭐ **`.agents/skills/` 正在成为中性之家。**
> Gemini CLI 和 Copilot 都直接读它。
> **在那儿提交一次，两个 agent 都能找到，零重复**；
> 对坚持自己路径的工具，从这一处**符号链接**回去，
> ⭐ **而不是维护会漂移的副本**。

**Cursor 的额外行为**：`Cursor` 会把技能与项目中已有的 `.cursorrules` 合并。

---

## 2. ⭐ 破坏可移植性的三件事

**① 工具专属的旁支文件**

```
Codex 会读 SKILL.md 旁一个可选的 openai.yaml
（UI 提示、MCP 工具依赖）
⭐ 它在 Codex 里有用，在其他任何地方都被完全忽略

⭐ 处置：任何旁支文件视为"给某一个工具的加分项"，
       ⭐ 绝不能成为技能运作所必需的依赖
```

**② 假设了你不拥有的运行时的脚本**

```
技能可以打包脚本，模型通过 bash 跑它们
⭐ 但各端运行时差异极大：

· Claude Code       —— 完整网络
· ⭐ Claude API     —— ⭐ 沙箱容器，无网络、不能运行时装包
                       ⭐ 一个 curl 或 pip install 的脚本
                          在 Codex/Claude Code 能跑，在 API 上死
· Gemini CLI        —— 把技能目录加入 agent 的允许文件路径
```

> ⭐ **如果脚本需要网络或依赖包：
> 在正文里写明，⭐ 并把"无网络路径"设为默认。**

**③ ⭐ 名字里的保留词（这条会静默咬人）**

```
Claude 要求 name 字段：
  · 小写、连字符
  · ≤64 字符
  · ⭐ 不得包含 "claude" 或 "anthropic"

⭐ 把技能命名为 claude-reviewer：
   在 Cursor / Codex / Gemini CLI 里都正常加载
   ⭐ 然后 Claude 拒绝它
```

> ⭐ **取一个工具中性的名字（`code-reviewer`，不是 `claude-reviewer`），
> 它就能通过每一道门。**

---

## 3. 字段支持度分级

```
⭐ 普遍支持（所有端）：   name · description
⭐ 广泛支持（4+ 端）：    when_to_use · argument-hint · arguments

专属字段（被其他端静默忽略）：
  allowed-tools · context · agent · hooks · model · disable-model-invocation
```

> ⭐ **专属字段在其他 agent 里不会报错，⭐ 它们会被静默忽略。**
> 这既是好消息（不破坏）也是坏消息（你以为的护栏不存在）。

**实测的一个安全后果**（很值得记）：

```
Claude Code / Codex / Gemini CLI / Copilot / OpenClaw
  都尊重或安全地忽略 allowed-tools

⭐ Cursor：不完整——它不解析 allowed-tools，
   ⭐ 于是技能在没有工具限制的情况下运行
   ——⭐ 权限范围比预期更宽

⭐ 输出是对的，但安全约束没有被执行
```

> ⭐ **结论：工具权限字段是 agent 专属的。
> ⭐ 如果安全约束真的要紧，必须在每个目标 agent 上单独测试。**

---

## 4. 触发可靠度实测差异

同一个 40 行 SKILL.md、一字不改放进四个 agent、20 次运行：

| 客户端 | 表现 |
|---|---|
| **Claude Code** | ⭐ 最可靠；`when_to_use` 提供额外匹配上下文 |
| **Codex CLI** | 触发可靠，但**偶尔需要更明确的提示** |
| **Gemini CLI** | 描述清楚时触发良好；⭐ **含糊描述导致的漏触发比 Claude 更多** |
| **Cursor** | ⭐ **需重新加载窗口才出现**；且常把技能当纯正文处理、跳过脚本与参数 |

> ⭐ Cursor 那条最麻烦：**它把"一次编写到处运行"变成"一次编写到处调试"**。
> 所以若目标含 Cursor，**高级约束必须人工验证**。

---

## 5. ⭐ 最大可移植子集

```
frontmatter：⭐ 只用 name + description（可选 when_to_use）
正文：        ⭐ 纯 markdown —— 编号步骤、标题、代码示例、表格
脚本：        ⭐ 用相对路径
子代理：      ⭐ 不要假设支持——设计成线性流程也说得通
工具权限：    ⭐ 不要依赖 allowed-tools 被执行；
              改用正文写明"该做/不该做什么"
描述：        ⭐ 最影响可移植性的单个字段——清楚具体，各端都能匹配
示例：        ⭐ 含在正文里（各端对含糊指令的解读不同，示例降低方差）
```

**决策一句话**：

> ⭐ **保持 SKILL.md 纯净：正文放可移植的 know-how、
> 一个值得触发的 description、一个工具中性的名字、
> ⭐ 以及没有任何假设了某个端不会给你的运行时的脚本。**

**放置策略**：

```
单一真源放 .agents/skills/
各工具的自己的路径指回它（symlink 或配置）
```

> ⭐ **手抄副本的方式一定漂移**：
> 修了 Claude 副本的 bug，忘了同步 Codex 和 Cursor 副本，
> **三个版本的同一个技能互相矛盾，你还记不清哪个是最新的**。
> 20 个技能 × 4 个 agent = **80 个本该是 1 个的文件**。

---

## 速查

```
□ ⭐ 名字不含 claude / anthropic（否则 Claude 拒收）
□ ⭐ 中性位置 .agents/skills/ 做单一真源，其余 symlink
□ ⭐ 不手抄副本（必然漂移）
□ ⭐ 旁支文件只能是加分项，不能是依赖
□ ⭐ 脚本需要的网络/包要写明，无网络路径设默认
□ ⭐ allowed-tools 在 Cursor 不生效 → 安全约束要各端实测
□ ⭐ 只用 name / description / 可选 when_to_use
□ ⭐ 不要假设子代理支持
□ ⭐ 描述清楚具体（最影响可移植性）
□ ⭐ 正文含示例（降低各端解读方差）
□ Cursor 需重载窗口；高级约束要人工验证
```

**一句话**：

> ⭐ **可移植性（一个文件在各端跑）由开放格式和目录地图解决；
> 发现与信任（找到对的技能并知道它有效）是格式解决不了的。**
