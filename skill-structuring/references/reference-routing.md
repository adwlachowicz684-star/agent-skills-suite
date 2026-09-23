# 引用路由：让"按需加载"真的发生

> ⭐ **一份从未被加载的 reference，等于不存在。**
> 正文不是百科全书，是**调度器**。

## 目录

- [两层结构：Router + Index](#两层结构router--index)
- [强制加载要用动词，不用形容词](#强制加载要用动词不用形容词)
- [内联清单要剪到 ≤3 条](#内联清单要剪到-3-条)
- [引用必须一层深](#引用必须一层深)
- [长文件要有 Contents](#长文件要有-contents)
- [看起来像修复其实不是的五件事](#看起来像修复其实不是的五件事)
- [重构检查清单](#重构检查清单)
- [怎么验证](#怎么验证)

## 两层结构：Router + Index

```
⭐ Required Reading Router  —— 在前 50 行内（导言/理念之后）
⭐ Reference Index          —— 紧挨着 Router
```

为什么是前 50 行：截断保头不保尾（见 `runtime-truth.md`），
路由信息放太后面可能根本进不了上下文。

## 强制加载要用动词，不用形容词

```
❌ "更多细节见 references/advanced.md"
❌ "（重要）请参考 references/advanced.md"
✅ ⭐ "STOP. Read `references/accessibility-floor.md` in full
      before implementing or reviewing any interactive widget."
```

三条：

```
① ⭐ 强制性靠动词（STOP. Read…），不靠形容词（重要/必须）
② 触发条件要具体——"在……之前"比"如果需要"强得多
③ ⭐ agent 读的是语气，不是装饰
   加 emoji 或"（重要）"不会让它更可能读
```

## 内联清单要剪到 ≤3 条

正文里内联的清单如果和 reference 覆盖同样的内容：

> ⭐ **reference 永远赢——把内联的剪掉。**

保留下来的内联内容要标明是 **tripwire（绊线）** 或 **gist（要点）**，
长度 **≤3 条**。

```
✅ 三条绊线（不是完整契约）：
   - 每个交互元素 focus-visible ≥ 2px
   - 全键盘可达；尊重 prefers-reduced-motion
   - 语义化地标 + 标题顺序

   ⭐ STOP. 实现或审查任何交互组件前，
      完整读取 references/accessibility-floor.md。
```

> 关键是最后一句：**绊线不是契约，契约在 reference 里。**

## 引用必须一层深

官方规则：

```
✅ SKILL.md → references/advanced.md
✅ SKILL.md → references/details.md

❌ SKILL.md → references/advanced.md → references/details.md
❌ SKILL.md → references/index.md → references/foo.md
```

> ⭐ **为什么：更深一层时，agent 会用 partal read（`head -100`）然后漏掉内容。**

所以：**所有 `references/*.md` 都必须直接被 SKILL.md 链接，彼此之间不互相链接。**

## 长文件要有 Contents

```
⭐ 任何超过 100 行的 reference 文件，顶部必须有 ## Contents
```

理由同上：**部分读取时也能看到它覆盖什么**。

⚠️ 但注意是 **Contents（章节名列表）**，不是 **TL;DR（摘要）**——
见下节第 3 条。

## 看起来像修复其实不是的五件事

**① 给触发行加"（重要）"或 emoji**

```
❌ agent 读的是语气，不是装饰
   强制性需要动词（STOP. Read…），不是形容词
```

**② 为了让正文保持内联而把 reference 写短**

```
❌ 这跟目标相反
   ⭐ 正文越短，reference 应该越长
```

**③ 给每个 reference 加 "TL;DR"**

```
❌ agent 读完 TL;DR 就跳过正文了
✅ 用 Contents TOC —— ⭐ 列章节名，不列摘要
```

**④ 把 reference 改名来暗示紧急性**

```
❌ URGENT-read-this.md / MUST-READ.md
   ⭐ 文件名不改变读取决策
      改变它的是 SKILL.md 里的触发措辞
```

**⑤ 把 SKILL.md 拆成很多同层小文件**

```
❌ SKILL.md 是唯一入口点
   多个顶层技能文件会破坏发现机制
```

## 重构检查清单

对着重写后的 SKILL.md 逐项打勾：

```
[ ] Required Reading Router 在前 50 行内（导言/理念之后）
[ ] Reference Index 紧挨着 Router
[ ] ⭐ 每个有对应 reference 的操作步骤，都以
    "STOP. Read references/X.md …" 结尾
[ ] 与 reference 重复的内联清单已剪到 ≤3 条，
    且标为 "tripwires" 或 "gist"
[ ] ⭐ 没有 reference 文件链接到另一个 reference 文件（一层深）
[ ] ⭐ >100 行的 reference 文件顶部有 ## Contents
[ ] SKILL.md 正文 < 500 行
[ ] ⭐ 不再有 "深度见 X" / "更多请读 X" 这类措辞
    ——每处引用要么是 router/index（描述性），
      要么是 STOP 指令（强制性）
```

最后一条特别值得注意：**不允许中间态措辞**。
"更多细节见 X" 既不是描述性索引也不是强制指令，
agent 会当成可选建议。

## 怎么验证

重构完不要靠"看起来对了"：

```
① ⭐ 开一个全新的 agent 实例
② 给它一个【需要用到某份 reference】的任务
③ ⭐ 观察它是否真的读了那个文件
④ 没读 → 那份文件的 STOP 触发条件太弱，加强它
```

> ⭐ **"我写了链接"不等于"它会被读"。**
> 唯一能证明的是观察到它被读。

## 什么时候不用这套

```
❌ 从零写新技能（那是 skill-authoring 的事）
❌ 只改 reference 文件本身、不动 SKILL.md
❌ ⭐ 150 行以下、没有 reference 文件的技能（没东西可路由）
❌ AGENTS.md / CLAUDE.md 重构（规则不同）
```

## 一句话总结

> ⭐ **正文是调度器，不是百科全书。**
> 剪掉内联的，强制加载，压平层级。
