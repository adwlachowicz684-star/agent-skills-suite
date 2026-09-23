# 供应链信任：像对待代码依赖一样对待技能

> 相关：《skill-governance》的 `marketplace-security.md` ·
> `security-audit-ops.md` · （已移至 _parked 领域实例库）的 `injection-audit.md`

---

## 目录

- [1. ⭐ 核心态度](#1--核心态度)
- [2. 六条实践](#2-六条实践)
- [3. 脚本的四条约束](#3-脚本的四条约束)
- [4. 负向触发与测试](#4-负向触发与测试)

---

## 1. ⭐ 核心态度

> ⭐ **像对待代码依赖一样对待技能：
> 安装前审查、锁定版本、设信任闸门、带安全约束地设计。**
>
> ⭐ **真实的供应链攻击已经发生过了。**

这不是理论风险（见 `marketplace-security.md` 的 ClawHub 2026-03 事件）。

---

## 2. 六条实践

| 实践 | 说明 |
|---|---|
| ⭐ **锁定版本** | 用注册中心时 pin 到具体版本，不要追 latest |
| ⭐ **信任边界** | ⭐ **不要从不新克隆的仓库自动加载项目级技能——先审查** |
| **最小权限** | 用 `allowed-tools` 限制执行期能力（见 `least-privilege.md`） |
| ⭐ **审批闸门** | ⭐ 破坏性动作（删文件、部署、发消息）前显式确认 |
| **脚本最小化** | 短、可读、非交互、⭐ **除非绝对必要否则不做网络调用** |
| 版本化迭代 | 随项目演进更新，像维护代码一样 |

> 第二条容易被忽略：
> `git clone` 一个陌生仓库后直接开跑，
> **仓库里的 `.claude/skills/` 会自动生效**。
> 部分平台会自动加闸门，但不要指望它。

---

## 3. 脚本的四条约束

```
① ⭐ 所有输入通过命令行参数传入（无交互式提示）
② 提供 --help，用法说明清晰
③ ⭐ 尽量输出结构化数据（JSON）
④ ⭐ 有意义的退出码与错误信息
⑤ ⭐ 默认安全行为——破坏性操作默认 dry-run
```

> 第 ⑤ 条尤其值得抄：**破坏性脚本默认 dry-run**，
> 需要真干时显式加参数。

---

## 4. 负向触发与测试

**Always define when the skill should NOT activate.**

> ⭐ **没有它，你会得到让用户恼火的误触发。**

一份好的 "When to use" 同时含正反例：

```markdown
## When to use this skill
Use when the user asks to: "run tests", "check if tests pass", "verify the test suite".

Do NOT use when the user:
- Asks to write or create new tests
- Asks about test coverage percentages
- Mentions "testing" in a non-code context
```

**测试配置**：

```
至少 5–10 条应该触发
⭐ 3–5 条不应该触发
⭐ 跑"有技能" vs "无技能"基线对比
```

> 这与 `eval-case-sources.md` 的数量建议一致，
> 且再次强调 **baseline delta 是唯一有意义的问题**。

---

## 速查

| 风险 | 防线 |
|---|---|
| 恶意/被篡改的技能 | ⭐ 安装前审查 + 锁版本 |
| 陌生仓库自动加载 | ⭐ 先审查，别直接跑 |
| 破坏性动作 | ⭐ 显式确认闸门 |
| 脚本副作用 | ⭐ 默认 dry-run |
| 过宽触发 | ⭐ Do NOT use 段 |
| 不知道有没有用 | ⭐ 有/无技能基线对比 |
