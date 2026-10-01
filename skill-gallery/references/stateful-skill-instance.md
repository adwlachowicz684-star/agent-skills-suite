# 完整样本：一份有状态的技能（站会记录）

> 相关：《skill-state》的 `skill-state/references/state-file-concurrency.md` ·
> `skill-state/references/state-schema-versioning.md` ·
> `skill-state/references/state-file-lifecycle.md` ·
> `skill-state/references/memory-state.md`
>
> 本文是《skill-gallery》里唯一一份**带状态**的样本。
> 选它是因为状态是最能暴露技能设计问题的部分——
> 无状态技能的毛病多半在措辞，⭐⭐⭐⭐⭐ **有状态技能的毛病在设计。**

---

## 目录

- [1. 它做什么](#1-它做什么)
- [2. 完整源码](#2-完整源码)
- [3. 状态文件的 schema](#3-状态文件的-schema)
- [4. 逐处点评：为什么这么写](#4-逐处点评为什么这么写)
- [5. 这份样本刻意没做的事](#5-这份样本刻意没做的事)

---

## 1. 它做什么

每天第一次运行时生成当日站会草稿，之后每次运行做增量更新。
跨会话、跨天都能接着用。

关键特征（也是它值得当样本的原因）：

```
⭐⭐⭐⭐ 状态写进仓库文件，不依赖上下文
⭐⭐⭐⭐ 追加写，允许并发
⭐⭐⭐⭐⭐ 状态带版本与写入时间
⭐⭐⭐⭐ 事实不进状态（项目负责人是谁，运行时查）
```

---

## 2. 完整源码

````markdown
---
name: standup
description: 生成与更新每日站会草稿——从 git 提交、打开的 PR 与任务看板汇总"昨天做了什么／今天要做什么／有什么阻碍"，写入 STANDUP.md 供团队同步。当用户提到站会、日报、每日同步、scrum、昨天做了什么时使用。
  Do NOT use for: 周报月报（用 weekly-report）、代码评审（用 code-review）。
---

# 站会草稿

## 状态文件

- 路径：`.standup/log.jsonl`（追加写，一行一条）
- ⭐ 允许多个写者并发；重复条目由读取侧按 run_id 去重
- 当前 state_version = 2

## 执行流程

1. 读 `.standup/log.jsonl` 的**尾部 200 行**（不是全量）。
   若 `state_version` 不等于 2，或 `written_at` 早于 48 小时前，
   ⭐ 判定为无状态，从空状态开始，并在输出首行注明"未找到有效历史"。

2. 采集当日事实（不查状态，每次都重新查）：
   - `git log --since="24 hours ago" --author=me --oneline`
   - 我名下的开放 PR（用 gh 或看板工具）
   - 我名下状态为 blocked 的任务

3. 与步骤 1 读到的历史比对，标出**今天新出现**的条目。

4. 写入 `.standup/log.jsonl`（追加一条，不覆盖）：

   {"state_version":2,"run_id":"<ISO时间>-<4位随机>",
    "written_at":"<ISO8601>","written_by":"standup@1.2.0",
    "data":{"date":"<YYYY-MM-DD>","done":[...],"plan":[...],"blocked":[...]}}

5. 重写 `STANDUP.md`（覆盖——它是产物，不是状态）。

## 输出

```
统计区间：2026-10-01 10:12 起 24 小时（基准：当前时间）
历史状态：有效（2 条，最新 2026-09-30）

昨天做了什么
- 修复登录跳转（commit a7f2，今天新增）
- 评审 #412

今天要做什么
- 完成 #418 的分页改造

阻碍
- 等待设计确认，已 2 天（未获取到阻塞人 → 不填）
```

## Critical Rules

- ⭐⭐⭐⭐⭐ 采集不到就写"未获取到"，不得写"无"或 0
- ⭐⭐⭐⭐⭐ 不得从状态文件里读"谁负责什么"——那是事实，每次重新查
- ⭐⭐⭐⭐ 状态文件只追加，不覆盖
- ⭐⭐⭐⭐ 状态读取失败 = 无状态，重算；不得猜测旧格式
- ⭐⭐⭐⭐ 输出首行必须写统计区间的时间基准
````

---

## 3. 状态文件的 schema

```json
{
  "state_version": 2,
  "run_id": "20261001-101233-a7f2",
  "written_at": "2026-10-01T10:12:33+08:00",
  "written_by": "standup@1.2.0",
  "data": {
    "date": "2026-10-01",
    "done": [
      {"text": "修复登录跳转", "ref": "commit a7f2", "new": true}
    ],
    "plan": [{"text": "完成 #418 的分页改造", "ref": "#418"}],
    "blocked": [
      {"text": "等待设计确认", "since_days": 2, "owner": "未获取到"}
    ]
  }
}
```

四个元数据字段的用途见 `state-schema-versioning.md`。
这里只强调一条：

> ⭐⭐⭐⭐⭐ **`data` 单独一层**——将来加元字段（比如 `valid_for`）时，
> 不会和业务字段混在一起，schema 才能演进。

---

## 4. 逐处点评：为什么这么写

### ① "尾部 200 行"，不是"全量"

> ⭐⭐⭐⭐ **读全量是状态文件最常见的事故**：文件长了以后读不进来，
> 截断静默发生，于是读到的是最旧的那部分，而最新状态在文件末尾。

写死 200 而不是"读全部"，是因为⭐⭐⭐⭐ **读取上限应该是一个写下来的数**，
不能取决于文件当时有多大。

### ② 两道新鲜度判断

```
state_version != 2            → 结构不兼容
written_at 早于 48 小时前     → 内容过期
```

> ⭐⭐⭐⭐⭐ 只有第一个是不够的：**结构兼容不等于内容有效。**
> 一份三个月前写的、格式完全正确的日志，对今天的站会毫无用处，
> 而它读起来和"刚刚写的"一模一样。

### ③ 事实每次重查

```
"谁负责什么" 不进状态，每次查
```

> ⭐⭐⭐⭐⭐ 这是最容易被做反的一处。把负责人存进状态很省事，
> 而它会在换人之后持续提供错误答案——**且无人质疑，因为它在"历史记录"里。**

判据见 `state-file-lifecycle.md`：状态里不该有会腐烂的事实。

### ④ 追加日志 + 覆盖产物

```
log.jsonl   追加  ← 状态
STANDUP.md  覆盖  ← 产物
```

> ⭐⭐⭐⭐⭐ **两者性质不同，写入方式就该不同。**
> 状态要保留历史且允许并发 → 追加；
> 产物是"当前这一版"，保留旧版本只会让人读错文件 → 覆盖。

### ⑤ 采集不到写"未获取到"

```
"owner": "未获取到"      ← ✅
"owner": null / "无"     ← ❌
```

理由见 `skill-output/references/placeholder-in-output.md`：
⭐⭐⭐⭐⭐ **"无"是一个完整的、语法正确的、语义错误的回答。**

### ⑥ 输出首行写时间基准

```
统计区间：2026-10-01 10:12 起 24 小时（基准：当前时间）
```

约 10 个 token，换来的是⭐⭐⭐⭐⭐ **"最近一天"到底指哪一天"变成可见**——
见 `skill-input/references/relative-time-resolution.md`。

---

## 5. 这份样本刻意没做的事

| 没做 | 为什么 |
|---|---|
| ⭐⭐⭐⭐⭐ 没写"如果状态文件损坏，尝试修复" | 修不好时的行为未定义；直接重算 |
| ⭐⭐⭐⭐ 没用文件锁 | 引入有状态机制来保护状态，总量反而增加 |
| ⭐⭐⭐⭐ 没做压实（compaction） | 每天一条，一年 250 行，还没到需要 |
| ⭐⭐⭐⭐ 没把 `.standup/` 加进 .gitignore | ⭐⭐⭐⭐⭐ 丢了它技能就退化，它是数据不是缓存 |
| ⭐⭐⭐⭐⭐ 没有 Gotchas 章节 | ⭐⭐⭐⭐⭐ Gotchas 是采集的，第一版没有素材（见 `skill-content/references/gotchas-mining.md`） |

最后一行值得强调，因为它正是这份样本和其他样本最大的差别：

> ⭐⭐⭐⭐⭐ **一份刚写好的技能，Gotchas 应该是空的。
> 空白不是缺陷——填满它才是，因为那意味着填进去了没验证过的东西。**

---

## 相关

- 《skill-state》的 `skill-state/references/memory-state.md`
- 《skill-output》的 `skill-output/references/placeholder-in-output.md`
- 《skill-input》的 `skill-input/references/relative-time-resolution.md`
- 《skill-content》的 `skill-content/references/gotchas-mining.md`
- 《skill-gallery》的 `skill-gallery/references/bad-skill-anatomy.md`
