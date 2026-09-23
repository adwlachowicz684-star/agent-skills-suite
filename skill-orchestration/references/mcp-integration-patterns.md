# MCP 协同落地：配置、护栏与四个坑

> 前置：`mcp-composition.md`（三层栈、五问决策树、三种混合模式）
> 这份只讲**工程落地**：配置怎么写、护栏加在哪、协同时会踩什么。

---

## 目录

- [1. 三个配置作用域](#1-三个配置作用域)
- [2. ⭐ 一个逗号禁用所有 server](#2--一个逗号禁用所有-server)
- [3. 护栏才是技能的价值所在](#3-护栏才是技能的价值所在)
- [4. 四个真实集成模式](#4-四个真实集成模式)
- [5. 协同四坑](#5-协同四坑)
- [6. 落地路径](#6-落地路径)

---

## 1. 三个配置作用域

| 作用域 | 位置 | 特点 |
|---|---|---|
| **local** | `~/.claude.json` | 绑定当前 checkout，**仅你自己** |
| **project** | 仓库根 `.mcp.json` | ⭐ **提交进版本控制，团队共享** |
| **user** | 用户级 `~/.claude.json` | 跨所有项目可用 |

```bash
claude mcp add github --command npx \
  --args "-y @modelcontextprotocol/server-github" \
  --env GITHUB_TOKEN=...
```

```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {"GITHUB_TOKEN": "${env:GITHUB_TOKEN}"}
    },
    "postgres": {
      "type": "stdio",
      "command": "uvx",
      "args": ["postgres-mcp", "--read-only"],
      "env": {"DATABASE_URL": "${env:DATABASE_URL}"}
    },
    "linear": {"type": "http", "url": "https://mcp.linear.app/sse"}
  }
}
```

注意 `postgres` 那条：`--read-only` 是**在 server 侧就限死**的——
这是后面"权限失控"那条坑的正解。

---

## 2. ⭐ 一个逗号禁用所有 server

> ⚠️ **`.mcp.json` 里一个放错位置的逗号，会静默禁用文件里的每一个 server。**

没有报错，只是全部不可用。

**修法**：重启前先 lint JSON。

```bash
python -m json.tool .mcp.json > /dev/null && echo OK
```

> 这与 `skill-structuring` 的 `frontmatter-pitfalls.md` 是同一类问题——
> **配置文件语法错误在这个生态里普遍是静默失败**。

---

## 3. 护栏才是技能的价值所在

最能说明"技能 + MCP 各干什么"的例子：

> **Postgres MCP server 本身会愉快地执行你给它的任何 SQL。**
> **技能加的是护栏。**

```markdown
- 绝不执行 DROP / TRUNCATE / ALTER
- 无界查询一律包上 LIMIT 100
- 表超过 1000 万行先跑 EXPLAIN
- 优先用只读副本连接，不用主库
```

还有一条经常被忽略的：

> 技能引用 `references/schema-overview.md`——**手工整理的数据模型地图**，
> 让 Claude ⭐ **不用每次从 information_schema 重新推导表关系**。

**实测收益**：跑这个模式的团队报告**危险查询减少 5–10 倍**，
因为流程在技能里，而不是在每个使用者的脑子里。

---

## 4. 四个真实集成模式

| 模式 | MCP 干什么 | Skill 干什么 |
|---|---|---|
| **code-review + GitHub MCP** | 拉 diff、发评论、提交评审 | ⭐ 编码团队风格：注释密度、何时建议重构、什么叫 blocker |
| **database-analyst + Postgres MCP** | 执行 SQL | ⭐ 护栏（见第 3 节）+ schema 地图 |
| **incident-response + Sentry + GitHub MCP** | 拉 issue/栈/最近提交 | ⭐ 编码二分定位启发式，起草修复 PR |
| **support-triage + Slack + Linear MCP** | 读频道、建 issue、回帖 | ⭐ 分类规则（bug/需求/配置）+ 打标签 |

> 共同点非常清楚：
> ⭐ **MCP 持有对实时状态的访问权；Skill 持有"拿它做什么"的判断。**

### 一个可复制的收益数据

Stripe MCP + 财务技能：

```
47 步手动提示  →  技能 + MCP 组合
平均完成轮次   14 → 4
30 次试验零错误
```

### 改哪边？

> ⭐ **优先改 Skill（业务逻辑），MCP 只要接口不变就不用动。**

新增一条团队评审规范 = 给技能提一行 PR；**MCP 层零改动**。
这是"技能才是差异化所在"那个判断的工程体现。

---

## 5. 协同四坑

| 坑 | 表现 | 解法 |
|---|---|---|
| **指令冲突** | MCP 说返回 JSON，技能说输出 Markdown | ⭐ **MCP 管数据格式，Skill 管最终呈现** |
| **Token 膨胀** | 技能 L2 + MCP schema 全塞进上下文 | 技能用渐进式加载；⭐ **MCP 工具按需 discovery** |
| **权限失控** | 技能调用了不该写的 MCP 工具 | ⭐ **在 MCP Server 端设最小权限** + 技能里标注安全红线 |
| **维护碎片化** | 改一个流程要同时改技能和 MCP | 优先改技能，MCP 接口稳定 |

> ⚠️ 第三条是最容易做错的：
> **不要在技能里声明权限就以为管住了**（`allowed-tools` 不是安全边界，
> 见 `skill-invocation-control.md`）。
> ⭐ **真正的边界在 MCP server 侧**——`--read-only` 这种才是硬限制。

---

## 6. 落地路径

```
1️⃣ 先跑通一个 MCP demo（官方 modelcontextprotocol.io）
2️⃣ 选一个高频场景，写一个技能（如"周报生成"）
3️⃣ ⭐ 在技能里声明 mcp_dependencies，明确它调用哪些工具
4️⃣ 用真实 MCP server 验证端到端流程
5️⃣ 逐步扩展：一个技能编排多个 MCP，一个 MCP 被多个技能复用
```

第 3 步值得强调：**显式声明依赖**让"这个技能需要什么外部环境"变成可读的契约，
换机器/换人时不会靠猜。

一句话总结：

> **MCP 让 AI"连得上"，Skill 让 AI"用得对"。**

---

## 速查

| 问题 | 处置 |
|---|---|
| 所有 MCP server 突然不可用 | ⭐ lint `.mcp.json`，多半是逗号 |
| 危险 SQL 被执行 | 护栏写进技能 + server 侧 `--read-only` |
| 上下文被 schema 撑爆 | 技能渐进式加载 + MCP 按需 discovery |
| 数据格式打架 | MCP 管格式，技能管呈现 |
| 改流程要动两边 | 只改技能，保持 MCP 接口稳定 |
| 换环境不知道缺什么 | 技能里声明 `mcp_dependencies` |
