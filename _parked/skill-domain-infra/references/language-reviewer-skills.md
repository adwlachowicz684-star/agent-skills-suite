# 多语言代码审查技能的矩阵式组织

> 一个成熟技能库的做法：**12 种语言 × 5 类规则**，
> 再配 30 个 agent。这份讲这种矩阵怎么搭、为什么这样搭。

## 目录

- [矩阵结构](#矩阵结构)
- [五类规则各管什么](#五类规则各管什么)
- [为什么是矩阵而不是大文件](#为什么是矩阵而不是大文件)
- [质量门禁：三层断言](#质量门禁三层断言)
- [修复前 vs 完成前的不同要求](#修复前-vs-完成前的不同要求)
- [对通用技能的启示](#对通用技能的启示)

## 矩阵结构

```
12 种语言 × 5 类规则 = 77 个规则文件
                    ↓
              + 30 个 agent
```

| 语言 | 规则文件 | 专属 reviewer agent |
|---|---|---|
| TypeScript | coding-style, hooks, patterns, security, testing | typescript-reviewer |
| JavaScript | 同上 | — |
| Python | 同上 | python-reviewer |
| Java | 同上 | java-reviewer |
| Kotlin | 同上 | kotlin-reviewer |
| Go | 同上 | go-reviewer |
| Rust | 同上 | rust-reviewer |
| C++ | 同上 | cpp-reviewer |
| C# | 同上 | — |
| PHP | 同上 | — |
| Perl | 同上 | perl-reviewer |
| Swift | 同上 | — |

另有中文翻译 11 份（`zh/`）。

**触发方式**：先检测项目语言，再设语言模式。

```bash
python tools/language-detector.py --project .
python tools/language-switcher.py --set python
```

> ⭐ **"先检测再切换"是关键设计**——
> 不要指望 agent 自己猜出这是 Rust 项目还是 Go 项目。

## 五类规则各管什么

| 类别 | 内容 | 为什么独立成文件 |
|---|---|---|
| **coding-style** | 命名、格式化、惯用法 | 变化最频繁，单独改不影响其他 |
| **hooks** | PreToolUse/PostToolUse 自动化 | ⭐ 机器可检查的规则从这里落到 hook |
| **patterns** | 语言惯用的设计模式 | 最容易过时，需独立更新 |
| **security** | OWASP、认证授权 | 审计时单独引用 |
| **testing** | 框架约定、覆盖率 | 与测试技能衔接 |

> ⭐ **这个切法跟"按语言切"是正交的**。
> 按语言切：改 Python 规则不影响 Go；
> 按类别切：改安全规则能一次性横扫所有语言。
> **矩阵同时支持两种更新路径。**

## 为什么是矩阵而不是大文件

```
❌ 一个大文件 per language（12 个文件，每个 500 行）
   → 改一条安全规则要动 12 个文件
   → 加载一种语言要吃掉全部 5 类规则的 token

✅ 矩阵（60 个小文件）
   → 改安全规则：动 security 那一列
   → 加载：只加载"当前语言 × 当前需要的类别"
```

**成本对比（粗算）**：

```
大文件方案：加载 1 种语言 = 500 行 ≈ 5,000 tokens
矩阵方案：  加载 1 类规则 = ~40 行 ≈ 400 tokens
⭐ 差 12 倍，且可以按需叠加
```

## 质量门禁：三层断言

```
Before Commit（提交前）
  □ 测试通过
  □ 覆盖率 80%+
  □ 安全扫描干净
  □ 代码评审通过
  □ 无硬编码密钥
  □ 所有输入已校验

Before Completion Claim（声称完成前）
  ⭐ □ 新鲜（fresh）的验证证据
  ⭐ □ 附上测试结果
  ⭐ □ 附上覆盖率报告
  ⭐ □ 附上安全扫描
  ⭐ □ 附上代码评审

Before Bug Fix（修 bug 前）
  □ 根因已定位
  □ 5 Whys 已完成
  □ 修复已测试
  □ 无回归已验证
```

> ⭐ **"Before Completion Claim"这一层是纯粹的防幻觉设计**——
> 它要求的是**新鲜证据**，不是"我记得跑过了"。
>
> 完全对应 `grounding-verification.md`（**`skill-crafting`**）：
> **没有在本会话跑过的验证 = 不准声称"完成了"。**

## 修复前 vs 完成前的不同要求

注意这两层的**性质不同**：

```
Before Bug Fix  → 要求的是"理解"（根因、5 Whys）
Before Completion → 要求的是"证据"（结果、报告、扫描）
```

> 这个区分很值得抄：
> **动手前要说明白为什么，交付时要拿出跑过的东西。**
> 混在一起写，agent 会在交付时给你一大段推理而不是证据。

## 对通用技能的启示

**① 正交切分比分层切分更适合"规则类"内容**

```
规则类内容（规范、检查单）→ ⭐ 矩阵（语言 × 类别）
流程类内容（SOP、工作流）→ 分层（主流程 → 子步骤 → 边界情况）
```

**② 检测优先于推断**

```
❌ "判断项目用的是什么语言"
✅ "跑 language-detector.py，然后 language-switcher --set X"
```

呼应 `script-engineering.md`（**`skill-crafting`**）：
确定性判断进脚本，不交给模型即兴。

**③ 门禁要分"提交前/交付前/动手前"三个时点**

```
每个时点要的东西不一样，写在一起会被稀释
```

**④ reviewer agent 按语言命名，规则按类别命名**

```
typescript-reviewer  ← 一个 agent（编排）
coding-style / security / testing ← 规则文件（内容）

⭐ agent 负责"谁来审"，规则负责"审什么"
   两者分离，改规则不用改 agent
```

**⑤ 覆盖率和安全扫描是"必需"而非"最好有"**

```
□ 覆盖率 80%+    ⭐ Required
□ 安全扫描干净   ⭐ Required
```

呼应 `testing-skills.md`：
覆盖率要**按代码类别分层**，不能一刀切——
简单 getter/setter 可以跳过。

## 自查

- [ ] 规则类内容是矩阵切分还是纵向切分？
- [ ] 改一条通用规则（如安全）需要动几个文件？
- [ ] 项目语言/框架是检测出来的还是让 agent 猜的？
- [ ] 门禁分了"动手前/提交前/交付前"三个时点吗？
- [ ] "交付前"那一层要求的是新鲜证据还是推理？
- [ ] agent（谁来审）与规则（审什么）分离了吗？
