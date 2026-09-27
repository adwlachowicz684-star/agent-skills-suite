# Verbose 调试：把 trace 变成可断言的测试

> 相关：`skill-evaluating` 的 `troubleshooting-manual.md`（四层定位）·
> `reload-debug.md`（加载排查）

---

## 目录

- [1. verbose 与 debug 的分工](#1-verbose-与-debug-的分工)
- [2. 该看哪几段](#2-该看哪几段)
- [3. 四条过滤命令](#3-四条过滤命令)
- [4. ⭐ trace-compare 循环](#4--trace-compare-循环)
- [5. 把 trace 变成自动断言](#5-把-trace-变成自动断言)
- [6. 常用别名](#6-常用别名)

---

## 1. verbose 与 debug 的分工

一个好用的心智模型：

```
--verbose  回答「技能做了什么」
--debug    回答「模型实际看到了什么、API 返回了什么」
```

> ⭐ **大多数技能问题属于第一类**——
> 所以**从 verbose 起步，只有需要更细时才升级到 debug**。
> 一上来就开 debug，会被几千行输出淹没。

---

## 2. 该看哪几段

冗长输出里，聚焦这五段就够：

| 段 | 看什么 |
|---|---|
| Tool Selection | 选了哪些工具、为什么 |
| Execution Results | 每个工具返回了什么 |
| Reasoning Steps | 模型的思维链 |
| Errors and Warnings | 需要注意的问题 |
| Token counts | ⭐ 上下文用量，**诊断截断问题的关键** |

---

## 3. 四条过滤命令

原始 trace 动辄几千行。用 grep 抽特定信号，不要逐行读：

```bash
# 只看工具选择决策
claude --verbose "task" 2>&1 | grep "Selected:"

# 只看错误与告警
claude --debug "task" 2>&1 | grep -E "\[ERROR\]|\[WARN\]"

# 看整场会话的 token 用量
claude --debug "task" 2>&1 | grep "tokens"

# 看每个工具调用的耗时
claude --debug "task" 2>&1 | grep "execution time"
```

典型用途配对：

```
技能找错文件      → --verbose 观察 Glob / Read 调用
技能执行异常慢    → --debug + grep "execution time"
上下文溢出/截断   → --debug + grep "tokens"
```

---

## 4. ⭐ trace-compare 循环

这是**技能开发期最有效的迭代方法**：

```bash
# 1. 在已知良好的输入上跑，存为基线
claude --verbose "test input" 2>&1 > baseline.log

# 2. 改你的 SKILL.md
...

# 3. 同样输入再跑一次
claude --verbose "test input" 2>&1 > updated.log

# 4. 对比
diff baseline.log updated.log
```

> ⭐ **diff 直接显示你的修改究竟如何改变了模型行为**
> ——既能验证改动是否生效，也能抓出**没预料到的回归**。

这比"感觉变好了"可靠得多，而且**完全不需要模型评委**。

---

## 5. 把 trace 变成自动断言

进一步：把 verbose 输出变成开发期的自动化质量检查。

```bash
#!/bin/bash
OUTPUT=$(claude --verbose "run tdd skill on src/auth.ts" 2>&1)

echo "$OUTPUT" | grep -q "Skill context loaded: tdd.md" \
  && echo "PASS: skill loaded" || echo "FAIL: skill not loaded"

echo "$OUTPUT" | grep -q "Read result.*auth.ts" \
  && echo "PASS: correct file read" || echo "FAIL: wrong file"

echo "$OUTPUT" | grep -q "Write complete.*auth.*test" \
  && echo "PASS: tests written" || echo "FAIL: no test output"
```

三条断言分别覆盖：

```
加载层   → 技能真的被加载了吗
定位层   → 读对文件了吗
产出层   → 产物生成了吗
```

> ⭐ 这正好对应 `test-pyramid.md` 的下三层，
> 而**成本只有 grep**——不消耗 token、不依赖模型。

---

## 6. 常用别名

用 `tee` 同时输出到终端和文件，实时看、事后查：

```bash
alias claude-debug='claude --debug 2>&1 | tee debug-$(date +%Y%m%d-%H%M%S).log'
alias claude-verbose='claude --verbose 2>&1 | tee verbose-$(date +%Y%m%d-%H%M%S).log'
```

> 不要一直开着 verbose——**只在主动调试时开**，
> 并重定向到文件以便事后分析。

---

## 速查

| 症状 | 用什么 |
|---|---|
| 技能没被加载 | `--verbose` + grep 加载行 |
| 读了错的文件 | `--verbose` 观察 Glob / Read |
| 慢 | `--debug` + grep "execution time" |
| 截断/溢出 | `--debug` + grep "tokens" |
| 改动是否生效 | ⭐ trace-compare（diff 两次 trace） |
| 想自动化 | 把 grep 断言写成脚本 |
