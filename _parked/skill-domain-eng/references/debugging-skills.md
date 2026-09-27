# 调试类技能：四个可复用的调试模式

> 相关：`skill-domain-eng` 的 `debugging-recovery.md` ·
> `log-analysis.md` · `incident-triage.md` ·
> `_new/tooling/five-minute-diagnosis.md`

---

## 目录

- [1. 四个技能，各对应一种能力](#1-四个技能各对应一种能力)
- [2. 组合使用的顺序](#2-组合使用的顺序)
- [3. 三个常见故障](#3-三个常见故障)
- [4. ⭐ 可直接抄的 CLAUDE.md 配置](#4--可直接抄的-claudemd-配置)

---

## 1. 四个技能，各对应一种能力

| 技能 | 做法 | 依赖的能力 |
|---|---|---|
| **日志分析** | `tail -100 /var/log/app/error.log \| claude "..."` | 非结构化文本的模式识别 |
| **Git 二分** | 让 Claude 驱动 `git bisect` | 执行 shell 并解读结果 |
| **假设检验** | 一次给出多个假设，要求逐个取证 | 可证伪的结构化调查 |
| **自动验证** | 每次改动后跑测试，不过不前进 | 迭代编辑 + 反馈回路 |

### ① 日志分析

```bash
tail -100 /var/log/app/error.log | claude \
  "Analyze these error logs. Group by root cause and rank by frequency.
   Suggest fixes for the top 3."
```

> ⭐ **通过 stdin 直接管道喂入**——
> 提供精确上下文，不需要人工摘要。
> **真实错误输出包含的信号，比你对问题的描述多得多。**

### ② Git 二分

```bash
claude "Run git bisect to find which commit broke the /api/users endpoint.
        The test command is: curl -s localhost:3000/api/users | jq '.status' | grep ok"
```

> ⭐ **"上周还能用"的回归，二分是定位破坏性提交的最快路径。**

### ③ 假设检验

```
The API returns 500 intermittently.
Hypothesis 1: Database connection pool exhaustion.
Hypothesis 2: Race condition in cache invalidation.
Hypothesis 3: Memory leak in request handler.
Investigate each hypothesis. Show evidence for or against.
```

> ⭐ **预先提供多个假设，防止模型锚定在第一个看似合理的解释上。**

### ④ 自动验证

```
Fix the null pointer in src/utils/parser.ts.
After each change, run: pnpm test -- parser.test.ts
Do not move on until the test passes.
```

> 每次文件变更都触发测试运行，形成紧密反馈回路。

---

## 2. 组合使用的顺序

```
日志分析（识别症状）
   ↓
假设检验（缩小原因）
   ↓
Git 二分（若是回归，定位到提交）
   ↓
自动验证（确认修复）
```

> ⭐ **永远从日志分析开始**——真实错误输出比任何描述都更有信号。

---

## 3. 三个常见故障

### ① ⭐ 把症状当成根因

```
看到 "connection refused"
→ 症状是错误，原因可能是端口耗尽、防火墙规则、或崩溃的服务
```

修法：明确提示 **"Distinguish between the symptom and the root cause."**

### ② Git bisect 在脏工作树上失败

> Claude 需要干净的工作目录才能跑 bisect。

修法：写进 CLAUDE.md——"Before running git bisect, stash all uncommitted changes."

### ③ ⭐ 假设检验塌缩成单一理论

```
模型立刻偏向一个假设，不调查其他
```

修法：明确要求
**"You must provide evidence for AND against each hypothesis before concluding."**

> ⭐ 这个"要反证"的要求是关键——
> 没有它，模型只会为它已经相信的那个假设找支持证据。

---

## 4. ⭐ 可直接抄的 CLAUDE.md 配置

```markdown
# Debugging Skills Configuration

## Log Analysis
- Production logs: /var/log/app/error.log
- Format: JSON structured, one entry per line
- Key fields: timestamp, level, message, request_id, stack

## Git Bisect
- Known good: last release tag (check `git tag --list`)
- Test command: `pnpm test --bail`
- ⭐ Always stash changes before bisecting

## Hypothesis Testing
- ⭐ Require evidence for AND against each hypothesis
- Minimum 2 hypotheses per investigation
- Log findings before proposing fixes

## Verification
- Test command: `pnpm test --bail`
- Lint command: `pnpm lint`
- Type check: `pnpm tsc --noEmit`
- ⭐ All three must pass before considering a fix complete
```

> ⭐ 这段配置的价值在于：它把"每次口头提醒"变成常驻规则。
> 属于 `instruction-layering.md` 里该放 CLAUDE.md 的那一类。

---

## 速查

| 场景 | 技能 |
|---|---|
| 不知道发生了什么 | 日志分析（管道喂入，别自己摘要） |
| "上周还能用" | Git 二分 |
| 原因不明、多个可能 | 假设检验（要反证） |
| 改完不确定对不对 | 自动验证（三项全过才算完） |
| 模型只找一个假设 | ⭐ 明确要求"正反证据都要" |
