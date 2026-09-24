# Monorepo 中的技能组织

> 一个大仓库里既有前端又有后端、既有 Go 又有 Rust 时，
> 技能该放哪、怎么避免互相干扰。

## 目录

- [三个作用域](#三个作用域)
- [按目录激活](#按目录激活)
- [⚠️ 嵌套发现的陷阱](#-嵌套发现的陷阱)
- [语言检测优先](#语言检测优先)
- [避免重复与冲突](#避免重复与冲突)

## 三个作用域

```
个人级  ~/.claude/skills/          跨项目通用
项目级  <repo>/.claude/skills/     ⭐ 随仓库走，团队共享
嵌套    <repo>/packages/x/skills/  ⭐ 只在处理该目录时生效
```

**monorepo 的推荐组合**：

```
□ 通用规范（代码风格、git 工作流）→ ⭐ 项目级根
□ 语言专属（Go/Rust/TS 规则）    → ⭐ 嵌套在对应 package
□ 个人偏好                        → 个人级
```

呼应 `team-repo-structure.md`（**`skill-distribution`**）的
`base/` + `frontend/` + `backend/` 分层——同一思路。

## 按目录激活

> ⭐ **用 `paths` 字段限定自动激活范围。**

```yaml
paths: "**/*.ts"        # 只在处理 TS 文件时加载
paths: "packages/api/**"
```

呼应 `skill-structuring` 的 `frontmatter-fields.md`（**`skill-crafting`**）：
**paths 是 glob 模式，限定何时自动激活**。

**好处**：

```
□ ⭐ 处理前端时不加载 Go 规则——省上下文
□ ⭐ 减少跨语言误触发（用 Rust 惯用法改 Go 代码）
```

## ⚠️ 嵌套发现的陷阱

> ⭐ **这是 monorepo 场景最容易踩的坑**：
> 嵌套 skills **不预加载**，
> 只有在处理那个目录的文件时才被发现。

**两条重要提醒**：

```
1. ⭐ 它与 CLAUDE.md 的加载行为正好相反
   ——CLAUDE.md 向上查找（子目录会读到父级的）
   ——嵌套 skills 是向下按需发现

2. ⭐ 启动时看不到不代表不存在
   ——排查"技能不生效"时要先确认当前工作目录
```

**一个 A/B 对照**：

```
场景 A：在 repo 根工作，编辑 packages/api/main.go
  → packages/api/skills/ 下的技能 ⭐ 会被发现（处理该目录文件）

场景 B：在 repo 根工作，编辑 README.md
  → 嵌套技能 ⭐ 不会被发现，也无法触发
```

## 语言检测优先

> ⭐ **不要让 agent 猜项目用什么技术栈。**

```bash
python tools/language-detector.py --project .
python tools/language-switcher.py --set go
```

呼应 `language-reviewer-skills.md`（**（领域实例库·已归档）**）：
**检测优先于推断**——确定性判断进脚本。

**monorepo 的特殊处理**：

```
□ ⭐ 每个 package 可能语言不同
□ ⭐ 检测粒度应该是 package，不是 repo
□ 跨 package 的任务要显式指定
```

## 避免重复与冲突

**两类问题**：

```
1. ⭐ 重复：同一个规范在根级和 package 级各放一份
   → 必然漂移
   → ⭐ 根级放公共部分，package 级只放差异

2. ⭐ 冲突：两个 package 的技能描述相近
   → agent 摇摆
```

**冲突三解法**（呼应 `skill-composition-patterns.md`，
**`skill-orchestration`**）：

```
□ 定优先级
□ 合并
□ ⭐ 限定作用域（用 paths）——⭐ 最优雅，让冲突根本不发生
```

> ⭐ 在 monorepo 里，**限定作用域几乎总是最优解**，
> 因为天然有目录边界可用。

**命名也要避免通用词**：

```
❌ review、test、deploy
✅ ⭐ go-api-review、react-component-test、api-deploy
```

呼应 `naming-description.md`（**`skill-authoring`**）。

## 与渐进式披露的关系

monorepo 天然适合三层加载：

```
L1  所有技能的 description（目录税，靠 paths 与嵌套控制规模）
L2  被激活技能的正文
L3  references/ 与 scripts/
```

> ⭐ **monorepo 的目录结构本身就是一层作用域过滤**——
> 这是它相对单仓库的额外优势。

## 自查

- [ ] 通用规范在项目级根，语言专属嵌套了吗？
- [ ] 用了 `paths` 限定激活范围吗？
- [ ] ⭐ 知道嵌套技能不预加载吗？
- [ ] ⭐ 知道它与 CLAUDE.md 的加载方向相反吗？
- [ ] 语言是检测出来的还是让 agent 猜的？
- [ ] 根级与 package 级有没有重复内容？
- [ ] 冲突用 `paths` 限定了吗？
- [ ] 技能名避免了通用词吗？
