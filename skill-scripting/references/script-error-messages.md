# 脚本的错误消息：写给模型看的

> 相关：《skill-scripting》的 `script-engineering.md`（该不该抽成脚本）·
> `tool-output-design.md`（输出设计）·
> `script-testing.md`（golden 文件）·
> 《skill-execution》的 `execution-error-protocol.md`（`safe_reply` 字段）·
> 《skill-security》的 `hooks-skill-cooperation.md`（stderr 就是模型看到的全部）
> 前置：那些讲⭐⭐⭐ 退出码要分级、⭐⭐⭐⭐ 输出要压缩，
> 这份讲⭐⭐⭐⭐⭐ **错误消息本身的写法**——
> 为什么"报错了"三个字会让模型去做一件比错误本身更糟的事。

---

## 目录

- [1. ⭐⭐⭐⭐⭐ 读者是模型，不是人](#1--读者是模型不是人)
- [2. ⭐⭐⭐⭐⭐ 一个坏错误消息的代价](#2--一个坏错误消息的代价)
- [3. ⭐⭐⭐⭐ 四段式结构](#3--四段式结构)
- [4. ⭐⭐⭐⭐ 三类错误各写什么](#4--三类错误各写什么)
- [5. ⭐⭐⭐ 绝对不能写进错误消息的](#5--绝对不能写进错误消息的)
- [6. ⭐⭐⭐ 与退出码的分工](#6--与退出码的分工)
- [7. ⭐⭐ 测试错误消息](#7--测试错误消息)

---

## 1. ⭐⭐⭐⭐⭐ 读者是模型，不是人

我们写脚本时，错误消息的习惯来自给人看：

```
Error: failed
❌ 无效输入
Permission denied
```

> ⭐⭐⭐⭐⭐ **但技能脚本的错误消息，第一个读者是模型。**
> 人看到"failed"会去查日志；
> 模型看到"failed"只有一个选项——⭐ **自己想办法**。

而模型"自己想办法"在错误场景下的典型行为是：

```
重试 → 换个参数再试 → 绕过这一步 → 编一个结果继续往下走
```

> ⭐⭐⭐⭐ 最后一步最致命：它满足了"流程要走完"的压力，
> **而它编的那部分会进入最终输出，且看起来完全正常。**

---

## 2. ⭐⭐⭐⭐⭐ 一个坏错误消息的代价

对照一个真实链条：

```
脚本：  "Error: API request failed"
模型：  认为是网络抖动 → 重试 3 次 → 仍失败
       → ⭐ 决定"根据上下文推断结果" → 编了一个
输出：  "分析完成"（含一段编造的数据）
用户：  完全看不出来
```

> ⭐⭐⭐ **根因不是模型不诚实，是错误消息没告诉它"不要推断"。**

一句 `Error: API request failed (HTTP 401). Do not infer or substitute values; report the failure and stop.`
就能拦住整条链——**成本是一行，收益是避免一次静默编造。**

这与 `execution-error-protocol.md` 的 `safe_reply` 是完全同一件事：
**你不给"该说什么"，模型就得自己组织语言，而组织语言正是它开始编的时候。**

---

## 3. ⭐⭐⭐⭐ 四段式结构

一条错误消息写四段，缺一段就少一层防护：

```
① 发生了什么（事实）
② ⭐ 为什么（直接原因，可观察）
③ ⭐⭐ 模型下一步该做什么（动作指令）
④ ⭐⭐⭐ 明确禁止什么（防编造/防绕过）
```

实例：

```
① Failed to write report: /out/report.md
② Parent directory does not exist
③ Re-run with --create-dirs, or create the directory first
④ ⭐ Do not write to an alternate path or skip the write step
```

> ⭐⭐⭐⭐⭐ **第 ④ 段是最容易被省的一段，也是唯一能防住"绕路"的一段。**
> 没有它，模型会去找一个"能写成功"的路径——
> 而那个路径不是你想要的，但它不会报错。

四个段落都能压缩成一行，所以成本很低：

```python
raise SystemExit(
  "Failed to write /out/report.md: parent dir missing. "
  "Re-run with --create-dirs. "
  "Do not write elsewhere or skip the step."
)
```

---

## 4. ⭐⭐⭐⭐ 三类错误各写什么

| 类型 | ⭐ 第 ③ 段该说 | ⭐⭐ 第 ④ 段该禁 |
|---|---|---|
| **输入问题** | 哪个字段、期望什么、实际是什么 | 不要用默认值替代 |
| **环境问题** | 缺什么依赖、怎么装 | ⭐ 不要降级为"部分成功" |
| ⭐ **外部失败** | 状态码、是否可重试 | ⭐⭐⭐ 不要推断或替代值 |

> ⭐⭐⭐⭐ 第二类最常被写错：
> 缺一个可选依赖时，脚本"贴心"地降级继续跑，
> 然后输出一份缺了一块的分析——**而这比直接失败危险得多。**
> ⭐ 是否降级是**调用方的决定**，不是脚本的。

第三类的"是否可重试"必须显式写：

```
❌ "API request failed"
✅ "API request failed (HTTP 429, rate limited). Retry after 60s. Max 3 attempts."
```

> ⭐⭐⭐ **不给重试次数，模型就会自己定一个——
> 而这正是"跑满 200 次烧光 token"那类事故的来源。**

---

## 5. ⭐⭐⭐ 绝对不能写进错误消息的

| 不能写 | 原因 |
|---|---|
| ⭐⭐⭐ 密钥、token、完整 URL | 会进上下文、进日志、可能进最终输出 |
| ⭐⭐ 堆栈里含内网地址 | 同上 |
| ⭐ 模糊的"可能/也许" | 模型会当成不确定 → 自己猜 |
| 多行无结构的 dump | ⭐ 挤占上下文（见 `tool-output-design.md`） |

第一条的具体做法：**报错里只放标识符的后四位**。

```
❌ "Auth failed for key sk-ant-abc123...xyz"
✅ "Auth failed for key ...xyz (last 4). Check ANTHROPIC_API_KEY env var."
```

---

## 6. ⭐⭐⭐ 与退出码的分工

两者不是重复，是**分层**：

```
退出码 → ⭐ 给机器：决定走哪个分支（见 script-engineering.md 的退出码分级）
消息   → ⭐⭐ 给模型：决定在那个分支里说什么、做什么
```

> ⭐⭐⭐ **常见错误是把信息只放在一边**：
> 给了精准退出码但消息写"failed"→ 模型知道该停，但不知道该说什么，于是开始编。
> 给了详细消息但退出码恒 1 → ⭐ 模型把"接口不通"当成"测试未通过"，跑去改测试。

所以脚本工程里的那三条（区分退出码、stdout/stderr 分离、非交互）
加上这份的四段式，**是同一套契约的两半**。

---

## 7. ⭐⭐ 测试错误消息

golden 文件通常只测成功路径。补一条：

```python
def test_error_message_is_actionable(result):
    assert result.returncode == 10          # VALIDATION_FAILED
    msg = result.stderr
    assert "Do not" in msg                  # ⭐ 有禁止段
    assert not re.search(r"sk-|token|Bearer", msg)   # ⭐ 无泄露
    assert len(msg) < 500                   # ⭐ 不挤占上下文
```

> ⭐⭐⭐ 第二条是关键——**把"不能写密钥"从一句提醒变成一条断言**。
> 这是我们反复说的"书面规则编码成校验器"在脚本侧的实例。

---

## 一句可贴在墙上

> ⭐⭐⭐ **错误消息里没有"不要推断"，模型就会推断——
> 而它推断出来的东西不会报错。**
