# 依赖声明与 lockfile：技能不是孤岛

> 相关：《skill-distribution》的 `packaging.md` ·
> `cross-agent-portability.md` · 《skill-governance》的 `retirement-pipeline.md`

---

## 目录

- [1. ⭐ 一个惊人的实证](#1--一个惊人的实证)
- [2. ⭐ 声明三类关系](#2--声明三类关系)
- [3. ⭐ lockfile 锁三样东西](#3--lockfile-锁三样东西)
- [4. ⭐ 锁文件生成的三个战场](#4--锁文件生成的三个战场)
- [5. ⭐ 五步加固策略](#5--五步加固策略)

---

## 1. ⭐ 一个惊人的实证

对 **143 万个** agent 技能的大规模实证：

```
36.60%  的技能携带隐藏依赖
⭐ 1.40%  的技能声明了它们
```

> ⭐ **你看到的东西和你实际在跑的东西之间，
> 差距危险地宽。**
>
> ⭐ 安全信号会**传递性地传播到多数根节点**。

> ⭐ 结论很明确：**agent 技能正在成为新的软件包，
> 它们需要 npm / PyPI 花十年才发展出来的那套依赖管理严谨性。**
> **差别在于技能供应链同时跨越三个渠道，攻击面更宽、治理更难。**

---

## 2. ⭐ 声明三类关系

frontmatter 里：

```yaml
---
name: my-skill
depends:
  - weather          # ⭐ 必需（缺失即失败）
  - coding-agent
optional:
  - github           # ⭐ 有则增强
conflicts:
  - old-weather      # ⭐ 不能共存
  - legacy-calendar
---
```

**版本约束**（semver 风格）：

```yaml
depends:
  - weather@>=1.0.0    # 1.0.0 或更高
  - calendar@^2.0.0    # 兼容 2.x.x
  - browser@~1.2.0     # 约 1.2.x
  - coding-agent@*     # 任意
  - github@1.5.0       # ⭐ 精确
```

**分级策略**（不同组件用不同宽松度）：

```
核心组件    固定版本  =1.2.3
工具类依赖  允许补丁  ~1.2.0
非关键库    允许次要  ^1.2.0
```

**registry 元数据**（`skill.json`）：

```json
{"name":"my-skill","version":"1.0.0",
 "depends":{"weather":">=1.0.0","coding-agent":"*"},
 "optional":{"github":">=2.0.0"}}
```

---

## 3. ⭐ lockfile 锁三样东西

```yaml
lockfileVersion: 2
skills:
  - name: demo-skill
    source: {type: apm, ref: org/repo/skills/demo-skill}
    dependencies: [helper-skill]
    files:
      - path: SKILL.md
        hash: sha256:0bf96dd1...
        size: 244
```

```
① 来源（git / npm / 本地路径）
② 依赖关系（谁依赖谁）
③ ⭐ 每个文件的 sha256（⭐ 改一个字节就能发现）
```

> ⭐ **MCP 与 Rules 这类 context 也能锁进同一个文件（v2 的 context 段）——
> 避免"技能锁了但 MCP 配置还在漂"。**

**工具分工**（别搞混）：

```
APM / Vercel skills / skillpm  → 解决"怎么装"
⭐ skilllock                    → 解决"装完之后怎么管"（锁/验/审计/复现/升级）
sklock                          → 处理嵌套 skills/*/skills/* + closureHash
```

> ⭐ **skilllock 不是安装器、不是技能仓库，也不替你做 code review。
> 它做的是 DevOps / 供应链治理——类似 lockfile + npm ci + npm audit 那套。**

---

## 4. ⭐ 锁文件生成的三个战场

**① semver 范围与精确版本的拉锯**

```
开发机用 npm install 生成松散范围
生产 CI 却要求 --frozen-lockfile
→ ⭐ 本地测试通过的技能在生产环境 missing dependency

✅ 统一使用精确安装模式
```

**② 双源同步的延迟暴雷**

```
开发者 A 更新私有仓但未发布到 Registry
开发者 B 从 Registry 取旧版本生成 lockfile
→ ⭐ CI 因混合来源引发哈希校验失败

检查清单：
□ 所有私有技能必须带 git+https 协议头
□ ⭐ CI 增加源一致性检查：if 'registry.claw' not in dep.source: fail()
□ ⭐ 私有仓到 Registry 的自动同步间隔 ≤1h
```

**③ 新人引导的版本雪崩**

```
⭐ 新手教程建议"初次接触就装全部示例技能"——这会导致：
   · 单点技能更新触发全量 lockfile 变更
   · 团队不同成员锁定不同次要版本
   · 合并时出现不可调和的冲突

✅ 新手初始仅锁定 1 个核心技能
✅ 用 claw audit deps 可视化依赖树后再逐步扩展
✅ ⭐ 建立"最小可用技能集"白名单
```

**三条纪律**：

```
① ⭐ 变更必须有 traceable 的关联（如 Issue ID）
② ⭐ 所有 override 必须附带 24h 过期时间
③ ⭐ 重大版本升级前执行依赖图仿真测试
```

> 某电商团队据此把版本锁导致的生产事故**从每月 3.2 次降至 0.1 次**。

---

## 5. ⭐ 五步加固策略

```
① 枚举技能图
   grep -r 'require|import|\$' ~/.agents/skills/*/SKILL.md
   逐个人工追踪引用

② ⭐ pin 到具体 commit hash，而不是跟踪分支
   git checkout abc123def   # pin to audited commit

③ ⭐ 审计包依赖
   技能 scripts/ 里有 package.json 或 requirements.txt 就跑：
   npm audit --production
   pip-audit -r requirements.txt

④ ⭐ 限制 MCP 服务访问——白名单只放行你审过的工具
   enabled_tools = ["get_file_contents", "create_pull_request"]

⑤ ⭐ 用 PreToolUse hook 拒绝未通过审计的技能发出的工具调用
```

> ⭐ **沙箱隔离和审批策略提供了有意义的运行时遏制，
> ⭐ 但它们在流水线里起作用太晚——
> 下一步是依赖期治理：类型化清单、递归解析、lockfile pin、审计命令。**

**分层测试与回滚**：

```
开发沙箱    进程级隔离   功能逻辑验证
集成沙箱    容器级隔离   依赖兼容性
准生产      虚拟机级     性能与权限控制

⭐ 每日自动备份 lockfile 到异地，保留最近 7 天的可执行回滚点
```

---

## 速查

```
□ ⭐ 36.6% 技能有隐藏依赖，仅 1.4% 声明了
□ 三类关系：depends（必需）/ optional（增强）/ conflicts（互斥）
□ 版本约束：>= ^ ~ * 精确
□ 核心=固定 / 工具=~ / 非关键=^

□ lockfile 锁三样：来源 / 依赖关系 / ⭐ 每个文件 sha256
□ ⭐ MCP 与 Rules 也锁进同文件（防 context 漂移）
□ skilllock 管"装完之后"，不是安装器

三战场：
□ ⭐ 精确安装，别让本地松散 vs CI frozen 打架
□ ⭐ 源一致性检查 + 同步间隔 ≤1h
□ ⭐ 新手只锁 1 个核心技能（别一次装全部）

□ ⭐ 变更可追溯 / override 24h 过期 / 升级前依赖图仿真

五步加固：
□ 枚举技能图
□ ⭐ pin commit hash，不跟踪分支
□ ⭐ npm audit / pip-audit 跑 scripts/ 的依赖
□ ⭐ MCP 工具白名单
□ ⭐ PreToolUse hook 拦截未审计技能
```

**一句话**：

> ⭐ **技能不是孤岛。36.6% 带着你没看见的依赖——
> 而只有 1.4% 承认了它们。**
