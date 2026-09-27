---
name: skill-loading
description: 技能的加载机制与结构类故障排查——frontmatter 解析与静默失败、两级加载与作用域级联、渐进式披露的 token 成本、嵌套作用域发现、参数替换、上下文分层与位置偏差、提示缓存、以及"技能不生效"的四层诊断法。用于技能加载失败、手动能调自动不能、改了不生效、长会话中途失效、同名覆盖。
  Do NOT use for 从零创建技能的整体流程（用 skill-authoring）、目录与文件该放哪（用 skill-structuring）、正文措辞与指令形态（用 skill-crafting）、触发词与 description 写法（用 skill-description），也不用于评估打分。
---

# 技能的加载机制与排查

## 边界

- 用于：**frontmatter 解析** · 加载与作用域 · 渐进式披露成本 · 参数替换 · 缓存 · **"不生效"的排查**
- 不用于：创建流程 · 目录布局与打包 · 正文措辞 · description 写法 · 评估打分

## 核心原则

> ⭐⭐ **技能不生效时，先分清是"没加载"还是"加载了但没触发"。**
> 前者查文件层，后者查描述层——**80% 的问题在文件层**（`four-layer-diagnosis-flow.md`）。

三层加载的成本形状：

```
L1 元数据   30–50 tokens/技能，常驻，100 个也才 5K
L2 正文     触发时整份加载，200–500 行
L3 参考     未读取前为零
```

> ⭐ **问题通常不在库存数量，而在每次判断时的候选质量。**

## 何时不用本技能

- 文件该放哪个子目录 → `skill-structuring` 的 `directory-contract.md`
- description 怎么写才触发 → `skill-description` 的 `description-patterns.md`
- 触发率评测与打分 → `skill-evaluating` 的 `trigger-tuning-loop.md`
- 正文写得好不好 → `skill-crafting`

## 路由表（按需深读）
| `frontmatter-full-reference.md` | ⭐⭐⭐ 六字段开放标准 vs CC 扩展边界；⭐ 加载失败硬条件四则 |
| `frontmatter-advanced-fields.md` | ⭐⭐⭐ `context: fork` / `agent` / `hooks` / `paths` |
| `yaml-frontmatter-errors.md` | ⭐⭐⭐★★ **半可用**：手动能调、自动不能；★中文全角冒号；三条验证命令 |
| `diagnostic-commands.md` | ⭐⭐⭐★★ 三类收敛（加载/优先级/描述）；/context vs /skills；作用域优先级 |
| `three-stages-discovery-activation-execution.md` | ⭐⭐⭐⭐ 三阶段；★★★真失忆 vs 假失灵二分诊断 |
| `nested-scope-discovery.md` | ⭐⭐⭐⭐ 嵌套作用域只在子目录工作时才被发现（极易误诊） |
| `prompt-caching-and-skills.md` | ⭐⭐★★★ 缓存是前缀匹配；★allowed-tools 是缓存事件 |
| `three-tier-token-math.md` | ⭐⭐⭐★ L1 30–50 tokens/技能；★健康基线 8K=窗口 4% |
| `skill-cascade-css.md` | ⭐⭐⭐ CSS 级联比喻：生效范围 vs 同名冲突；★插件不在梯子上 |
| `prompt-layering-positional-bias.md` | ⭐⭐⭐ 四层职责 + 位置偏差；★关键规则两端重复 |
| `four-layer-diagnosis-flow.md` | ⭐⭐⭐ 四步排查 + 停机规则；★80% 问题在文件层 |
| `official-spec-and-style.md` | ⭐⭐⭐ 加载失败硬条件四则；Markdown 不用 XML |
| `argument-substitution.md` | ⭐⭐ 参数替换：⭐⭐⭐ 会静默损坏 shell 代码示例 |
| `skill-reload-and-session-state.md` | ⭐⭐⭐⭐⭐ 唯一需要重启的情况；⭐⭐⭐⭐⭐ 生效 vs 看清效果；⭐⭐⭐⭐⭐ 问它最快 |
| `nine-checks-not-working.md` | ⭐ 九项排查清单 + 显式调用隔离技巧 |
| `frontmatter-fields.md` | ⭐ 字段速查与 YAML 六个陷阱 |
| `frontmatter-pitfalls.md` | ⭐ 静默失败根因：两阶段解析 + 完整雷区表 |
| `metadata-fields.md` | ⭐ 四必需字段 + 六元数据 + 六章节 |
| `invocation-control-fields.md` | ⭐ 谁能调用：两个 frontmatter 声明字段 |
| `five-minute-diagnosis.md` | ⭐ 五分钟诊断八步：model pin、缓存、大小写 |
| `verbose-debug.md` | ⭐ Verbose 调试：trace-compare 循环、grep 断言 |

**先读哪一份**：

| 症状 | 读 |
|---|---|
| ⭐ 手动能调、自动不触发 | `yaml-frontmatter-errors.md`（元数据为空） |
| ⭐ 改了不生效 | `diagnostic-commands.md` · `five-minute-diagnosis.md` |
| ⭐ 新鲜会话好用、中途失效 | `three-stages-discovery-activation-execution.md` |
| ⭐ 目录看着对但列表里没有 | `nested-scope-discovery.md` |
| 长会话成本不合比例地涨 | `prompt-caching-and-skills.md` |

## Critical Rules

- ⭐ **`---` 必须在文件第 0 字节**；从 Word 复制最容易引入不可见字符
- ⭐ **"loaded" 只代表文件存在，不代表能跑**——两阶段解析，第二阶段才严格校验
- ⭐ **含 `$N` 的代码示例必须移进 `references/`**——参数替换在加载时执行，会静默损坏 shell
- ⭐ **压缩带回的是"开头 5000"，不是"最重要的 5000"**——关键指令放两端
- ⭐ 改完 frontmatter 若怀疑缓存，**重启会话**是唯一永远有效的手段
- ⭐ **name 不得含 "claude" / "anthropic"**——其他端能加载，Claude 拒收

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "技能在列表里，所以加载成功了" | loaded ≠ 能跑。两阶段解析，第二阶段才严格校验。 |
| "我本地能跑就行" | 大小写敏感性在 macOS/Windows 与 Linux 不同——只能靠规范 + 静态检查防。 |
| "改了 description 就生效了" | 平台缓存技能描述；怀疑时重启会话。 |
| "技能中途失效了，估计被压缩挤掉了" | ⭐ 先重新调用一次：回来是真失忆，没回来是假失灵——修法完全不同。 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/validate_skill.py <dir>` | 自举校验：结构、路由表覆盖、孤立文件、行数上限 |

## 参考

- 相关技能：《skill-structuring》（目录与打包）·《skill-description》（触发词）·
  《skill-evaluating》（触发与行为评测）·《skill-refining》（上下文压缩）
