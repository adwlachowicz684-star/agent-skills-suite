# 隐藏 Unicode 指令注入：看不见的对抗载荷

> 相关：《skill-governance》的 `injection-audit.md`（六类红旗）·
> `supply-chain-audit.md` · `pre-install-security-audit.md` ·
> `marketplace-security.md`
> 前置：那份把"Unicode 转义或同形字"列为六类红旗之一，
> 这份把它⭐ **单独展开成一种完整攻击面**，含⭐⭐ 具体检测方法与⭐⭐ 一条反直觉结论。

---

## 目录

- [1. ⭐⭐⭐ 攻击面：工具描述 / 技能文件 / MCP server](#1--攻击面工具描述--技能文件--mcp-server)
- [2. ⭐⭐ 为什么它特别危险](#2--为什么它特别危险)
- [3. ⭐⭐ 检测方法：Unicode linting](#3--检测方法unicode-linting)
- [4. ⭐⭐ 三层防御](#4--三层防御)
- [5. ⭐⭐⭐ 反直觉：模型越强越脆弱](#5--反直觉模型越强越脆弱)
- [6. ⭐ 已知的"不确定性"](#6--已知的不确定性)

---

## 1. ⭐⭐⭐ 攻击面：工具描述 / 技能文件 / MCP server

攻击载荷藏在三处：

```
① ⭐ 工具描述（tool descriptions）
② ⭐ 技能文件（SKILL.md 及 references/）
③ ⭐ MCP server manifest
```

**载荷形式**：

```
· ⭐ Unicode Tags 区块码点（Tags-block codepoints）
· ⭐ 零宽字符（zero-width characters）异常密度
· 同形字替换（homoglyph substitution）
· 编码混淆（encoding obfuscation）
```

> ⭐⭐ 这类攻击的厉害之处：**人读源文件时什么都看不见**——
> 它们在大多数编辑器里不渲染或渲染成空白。
> **你逐行审查过这个文件，你依然中招了。**

---

## 2. ⭐⭐ 为什么它特别危险

```
⭐⭐⭐ 人类审查这一道防线对它完全失效。
```

对比其他注入：

| 攻击 | 人能不能看出来 |
|---|---|
| 明文"忽略之前的指令" | ✅ 能 |
| HTML 注释里藏指令（ClawHub 事件） | ⚠️ 要看原始文件 |
| ⭐⭐ **Unicode 隐藏指令** | ⭐⭐ **看不出来** |

> ⭐⭐⭐ 这直接推翻了 `pre-install-security-audit.md` 里
> "读一遍 SKILL.md 和 scripts/"这条建议的有效性——
> **对这类载荷，读一遍是不够的，必须机器检测**。

---

## 3. ⭐⭐ 检测方法：Unicode linting

> ⭐⭐ **CI/CD 流水线应加入 Unicode linting，
> 拒绝任何含 Tags 区块码点或异常零宽字符密度的技能文件、
> MCP server manifest 或 AI 配置文件。**

**应用范围**（四条，缺一不可）：

```
· ⭐ vendored 依赖
· ⭐ 社区来源的技能包
· ⭐ 共享配置仓库的贡献
· ⭐⭐ 第三方 MCP server（批准使用前必做）
```

**现有工具**（2026 年）：

```
· Lasso Security 的 claude-hooks（2026-01）
  ⭐ PostToolUse hook，在模型处理工具输出⭐ 之前拦截
  ⭐⭐ 50+ 检测模式，含编码混淆与同形字替换
· wunderwuzzi 的 aid scanner（2026-02）
  ⭐ 专门针对技能文件与 agent 配置里的 Unicode Tag 序列
· NVIDIA Garak
  ⭐ 用于组织自己做实证测试
· AWS Bedrock Guardrails 的 Unicode 字符走私防御指南
```

> ⭐⭐ PostToolUse hook 这个位置很关键：
> **它在模型看到输出之前拦截**——
> 这与 `determinism-boundary.md` 的"执行侧强制"是同一思路：
> **不指望模型自己识别，而是在它看到之前就处理掉。**

---

## 4. ⭐⭐ 三层防御

```
① ⭐ 构建与供应链层
   Unicode linting + ⭐ 版本 pinning + ⭐ 加密哈希校验工具描述
   ⭐⭐ 后者防 "rug-pull"：可信的 MCP server 被静默更新成含恶意指令

② ⭐ agent 配置层
   ⭐⭐ 自动批准模式（VS Code 的 chat.tools.autoApprove 等）
       ⭐ 默认关闭，启用前需显式安全评审
   ⭐⭐ 依据：CVE-2025-53773 表明自动批准消除了
       "本可捕获 agent 执行意外 shell 命令"的人工确认步骤
   最小权限原则

③ ⭐ 检测与响应层
   上文那些工具
```

> ⭐⭐⭐ **"密码学来源验证 + 行为沙箱 + 运行时监控"三者都是必需组件**——
> 原文用的是 "required components of a defensible agentic AI deployment"。
>
> ⭐⭐ 一句可以直接记住的原则：
> **⭐ 任何技能或 MCP server 都不得"仅因其来源"而被信任。**
> 这与 `marketplace-security.md` 的"签名验的是身份与完整性，不是善意"
> 是同一条，只是换了措辞。

**CCM 的归类**也值得注意——它给出了一个有用的心智模型：

> ⭐ **把技能文件和 MCP server 的工具描述当作⭐ 应用输入，
> 与 Web 应用的输入适用同样的校验要求。**

---

## 5. ⭐⭐⭐ 反直觉：模型越强越脆弱

MCPTox 基准的发现：

> ⭐⭐ **能力越强的模型越脆弱**（more capable models are more vulnerable）——
> 这是个显著且反直觉的结果。

另两个数据点：

```
· Trend Micro 实测：对 Claude 3.5 Sonnet 攻击成功率 ⭐ 87.5%
· Claude-3.7-Sonnet 对 Tool Poisoning 的⭐ 最大拒绝率低于 3%
```

> ⭐⭐⭐ 如果"越强越脆弱"成立，那么**升级模型不会自动带来安全性提升**——
> 这与 `capability-vs-preference.md` 那条
> "模型升级对能力型影响远大于偏好型"
> 形成了一个令人不安的推论：**升级改善了能力，却可能扩大攻击面。**

> ⭐ 所以 `cross-model.md` 的跨模型测试矩阵里，
> **安全性必须在每个模型档位单独测**，不能只测一次。

---

## 6. ⭐ 已知的"不确定性"

这份研究罕见地列出了自己的局限，值得照抄这种态度：

```
· ⭐ 厂商的缓解状态记录不完整
  （Anthropic 2024 年的初始回应把它定性为"不是安全问题"；
   2026 年初的行为未确定）

· ⭐ 87.5% 的成功率会随模型版本变化
  ⭐⭐ 组织应⭐ 自己做实证测试（如 NVIDIA Garak），
      再对自身暴露面下结论

· ⭐⭐ "越强越脆弱"⭐ 尚未被独立团队复现
   可能只反映被测的那组攻击场景，而非普遍原则

· ⭐ 拒绝率 <3% 只针对基准里那组攻击配置，
   ⭐ 分布外攻击下模型行为可能不同
```

> ⭐⭐⭐ **"组织应自己做实证测试再下结论"** ——
> 这与 `skillsbench-vs-realworld.md` 那条
> "基准里的优势会被真实场景压缩"是同一种谨慎：
> **别人的数字不能直接搬到你的环境。**

---

## 速查

```
□ ⭐⭐⭐ 载荷藏在：工具描述 · 技能文件 · MCP server manifest
□ Tags 区块码点 · ⭐ 零宽字符异常密度 · 同形字 · 编码混淆
□ ⭐⭐⭐ ⭐ 人类审查对它完全失效（编辑器里看不见）

□ ⭐⭐ CI 加 Unicode linting，拒绝含 Tags/零宽异常的文件
□ 范围：vendored 依赖 · 社区技能包 · 仓库贡献 · ⭐ 第三方 MCP server
□ 工具：claude-hooks（⭐ PostToolUse，模型看到前拦截）
       aid scanner（技能文件 Unicode Tag）· Garak（自测）

□ ⭐⭐ 三层：供应链（linting + pinning + ⭐ 哈希校验防 rug-pull）
       配置（⭐⭐ 自动批准默认关闭）· 检测响应
□ ⭐⭐⭐ 任何技能/MCP 都不得仅因来源被信任
□ ⭐ 把技能文件当作⭐ 应用输入，适用 Web 输入同样的校验

□ ⭐⭐⭐ ⭐ 越强越脆弱（未复现）· 87.5% 成功率 · 拒绝率 <3%
□ ⭐⭐ 升级改善能力但可能⭐ 扩大攻击面 → ⭐ 每个模型档位单独测安全
□ ⭐⭐⭐ 别人数字不能直接搬 → ⭐ 自己做实证测试
```

**一句话**：

> ⭐⭐⭐ **隐藏 Unicode 指令的可怕之处不是技术多高明，
> 而是它让"人读一遍源文件"这道防线完全失效——必须机器检测，
> 而且要在模型看到输出之前拦截。**
