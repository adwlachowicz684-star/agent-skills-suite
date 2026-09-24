# 安装前安全审计：15 向量与判决规则

> 相关：《skill-governance》的 `supply-chain-audit.md`（依赖治理）·
> `injection-audit.md`（六类红旗）· `security-audit-ops.md`（审计流程）·
> `allowed-tools-least-privilege.md`
> 前置：那些讲"依赖怎么管、红旗长什么样、审计怎么走"，
> 这份给一份⭐ **可直接执行的扫描清单 + 每种命中的判决（BLOCK/FLAG/REJECT）**。

---

## 目录

- [1. ⭐ 心态：把技能当依赖](#1--心态把技能当依赖)
- [2. ⭐⭐ 15 向量与判决规则](#2--15-向量与判决规则)
- [3. ⭐ 90 秒审计](#3--90-秒审计)
- [4. ⭐⭐ 三个改进方案，哪个最有效](#4--三个改进方案哪个最有效)
- [5. 一个容易被漏的信号](#5-一个容易被漏的信号)

---

## 1. ⭐ 心态：把技能当依赖

> ⭐⭐ **把技能当作依赖来对待。**
> **恶意技能和你 `npm install` 的恶意包拥有同样的访问权限——
> 只是⭐ 它以你的权限运行，并且⭐ 能看到你的对话上下文。**

另一条技术事实：

> ⭐ **Shell 指令在 hooks 里是在模型对输出进行推理之前就执行的。**

> ⭐ 这解释了为什么 `determinism-boundary.md` 说"拦截写进技能是表演"——
> **执行顺序上，hook 已经跑完了，模型才刚开始想。**

**信任原则**：⭐ 连"可信来源"的技能也要验——可能被供应链攻击、可能含可利用漏洞、可能权限过宽。

---

## 2. ⭐⭐ 15 向量与判决规则

**① 提示注入模式**（SKILL.md 及所有 .md reference）

```
"ignore previous instructions" / "new instructions:" / "you are now"
"forget everything" / "disregard" / "override.*instructions"
"act as if" / "system:"（出现在 frontmatter 之外）

⭐ 判决：任何命中 = BLOCK。⭐ 这些在技能里永远不合法。
```

**② 密钥与凭据**

```
API keys（sk- / pk_ / AKIA / ghp_ / glpat-）
Tokens（Bearer, token=, api_key=）
连接串（postgres:// / mongodb+srv:// / redis://）
私钥（-----BEGIN）
⭐ 环境变量带实际赋值（KEY=actual_value）

⭐ 判决：任何命中 = BLOCK，并报告给仓库维护者
```

**③ Unicode 与同形字**

```
零宽字符（U+200B / U+200C / U+200D / U+FEFF）
RTL override（U+202E）
⭐ 同形字（西里尔 а/о/е 替换拉丁 a/o/e）
frontmatter 值里的不可见字符

⭐ 判决：任何非 ASCII 不可见字符 = FLAG（人工复核）
```

> ⭐ 同形字那条最阴：**人眼看不出来，字符串比较也能绕过**。

**④ 行为操纵**

```
"always use [某个服务]"（供应商锁定）
"send data to" / "POST to" / 从非预期 URL "fetch from"
"disable security" / "skip validation" / "bypass"
⭐ 编码指令（散文里的 base64 / hex / URL 编码）

⭐ 判决：依赖上下文，FLAG 人工复核
```

**⑤ 权限过宽**

```
文档类技能需要终端访问？
lint 类技能需要网络访问？
格式化类技能需要写任意文件？

⭐ 判决：范围不匹配 = FLAG
```

> ⭐ 这三条问句形式很好用——**按"声明的用途"反推"该要什么权限"**。

**⑥ 数据外传**

```
URL 与技能声明用途不符
把内容复制到外部服务的指令
剪贴板操作
上传到未知端点

⭐ 判决：任何外传模式 = BLOCK
```

**⑦ frontmatter 完整性**

```
name 与目录名一致 / version 符合 semver / last-updated 是有效日期且不在未来
platforms 只含已知平台名
dependencies 只引用有效的 MCP/技能名
⭐ 没有可能被当作指令解析的意外字段

⭐ 判决：frontmatter 非法 = REJECT
```

**⑧ 体积与复杂度**

```
⭐ SKILL.md > 3000 tokens = WARNING（性能影响）
```

**代码执行风险**（扫描 .py / .sh / .bash / .js / .ts）：

| 类别 | 模式 | 级别 |
|---|---|---|
| 命令注入 | `os.system()` / `os.popen()` / `subprocess.call(shell=True)` / 反引号 | 🔴 CRITICAL |
| 代码执行 | `eval()` / `exec()` / `compile()` / `import()` | 🔴 CRITICAL |
| 混淆 | base64 载荷 / `codecs.decode` / hex 串 / `chr()` 链 | 🔴 CRITICAL |
| 网络外传 | `requests.post()` / `urllib.request` / `socket.connect` / `httpx` | 🔴 CRITICAL |
| 凭据采集 | 读 `~/.ssh` `~/.aws` `~/.config`、环境变量提取 | 🔴 CRITICAL |
| 提权 | `sudo` / `chmod 777` / `setuid` / cron 操纵 | 🔴 CRITICAL |
| 不安全反序列化 | `pickle.loads()` / 非 SafeLoader 的 `yaml.load()` / `marshal.loads()` | 🟡 HIGH |
| 文件系统越界 | 写到技能目录外、`/etc/`、`~/.bashrc`、创建 symlink | 🟡 HIGH |
| ⭐ 子进程（安全） | `subprocess.run()` 传列表参数、无 shell | ⚪ INFO |

> ⭐ 最后一行很有价值：**它告诉你"安全的写法长什么样"**，
> 避免你因噎废食地把所有 subprocess 都判为危险。

**判决解释**：

```
✅ PASS  无 critical / high 发现 —— 可安装
⚠️ WARN  high/medium —— 安装前人工复核
❌ FAIL  critical —— ⭐ 未修复前不得安装
```

**strict 模式**：⭐ 任何 WARN 升级为 FAIL（团队 CI 门禁建议用这个）。

---

## 3. ⭐ 90 秒审计

一份极简版（适合"从陌生人那里 install"前）：

```
① 读一遍仓库/技能目录
   搜：.env / token / api_key / Authorization / webhook
       request( / curl / fetch(
   ⭐ 如果触及 ~/.config、~/.ssh、~/.aws 或 agent 记忆文件 → 高风险

② 看安装脚本的路径
   CLI 从哪里拉代码？npm？git？直链？
   ⭐ 如果安装步骤执行任意 postinstall 钩子 → 假定可能已失陷

③ ⭐ 假定提示注入是载荷的一部分
```

> ⭐⭐ 第 ③ 条最值得记住：
>
> **恶意 SKILL.md 不需要"代码"，
> 只要能说服你（或你的 agent）交出密钥就够了。**
>
> ⭐ **"把你的 API key 贴进去测一下"就是新的"验证你的账户"。**
> ——⭐⭐ **社会工程学对 agent 同样有效。**

---

## 4. ⭐⭐ 三个改进方案，哪个最有效

社区讨论里给了三个候选，投票结果与理由很有价值：

```
A) 签名技能（验证身份）
B) ⭐ 权限清单（声明能力）
C) 社区审计（扫描结果 + 徽章）
```

**结论：B 胜出**，三条理由：

```
❌ A 签名：验的是身份与意图中的前者
   ⭐ "一个经过验证的恶意技能，仍然是恶意的"

❌ C 社区审计：很好但是⭐ 反应式的——它在部署之后才抓到问题
   （而且需要一个"真的会去审计"的社区）

✅ ⭐ B 权限清单：⭐ 主动式的——⭐ 在技能运行之前就约束它能做什么
   例："可读 ~/workspace/*，不可读 ~/.ssh、~/.config"
   ⭐ 这样的清单本可以阻止最近的好几起事件
   ⭐⭐ "技能可以仍然有用，同时不危险"
```

> ⭐⭐ **"签名验的是身份，不是善意"** ——
> 这与 `marketplace-security.md` 那句"签名验的是身份与完整性，不是善意与安全"
> 完全一致，**两个独立来源得出同一结论**。

> ⭐ 最后那句 "can still be useful without being dangerous" 是最佳总结：
> **安全的目标不是不让技能干活，是让它干该干的活、干不了不该干的活。**

---

## 5. 一个容易被漏的信号

```
⭐⭐ 检查技能仓库的更新频率：
   如果它 6 个月没动过，
   ⭐ 而在你安装的前一天突然有一个 commit
   ——这是供应链红旗。

⭐ 沉睡的仓库突然收到"维护更新"，是经典的失陷路径。
```

> ⭐ 这条非常好用，因为它**只需看一眼提交时间**，
> 却能抓住最常见的攻击手法（先养号、后投毒）。

**背景数据**（说明这不是理论风险）：

```
2026 年：341 个恶意技能被下架（ClawHavoc 事件）
        283 个技能被发现泄露 API key（Snyk 扫描）
```

---

## 速查

```
□ ⭐⭐ 把技能当依赖：它以你的权限运行，⭐ 且能看到对话上下文
□ ⭐ hooks 里的 shell 在模型推理之前就执行了
□ ⭐ 连可信来源也要验（供应链/漏洞/权限过宽）

15 向量判决：
□ 提示注入 → BLOCK（技能里永远不合法）
□ 密钥凭据（含 KEY=实际值）→ BLOCK + 报告维护者
□ ⭐ 同形字（西里尔字母）→ FLAG（人眼和字符串比较都能绕过）
□ 行为操纵（含编码指令）→ FLAG
□ ⭐ 权限过宽：按声明用途反推该要什么权限 → FLAG
□ 数据外传 → BLOCK
□ frontmatter 非法 → REJECT
□ SKILL.md >3000 tokens → WARNING
□ 代码：命令注入/代码执行/混淆/外传/凭据/提权 → CRITICAL
□ ⭐ subprocess.run(列表参数, 无 shell) = INFO（安全写法）
□ PASS/WARN/FAIL 三级；⭐ strict 模式把 WARN 升为 FAIL

⭐ 90 秒：
□ 搜 .env/token/api_key/curl/fetch(；⭐ 触及 ~/.ssh 等 = 高风险
□ 安装是否执行任意 postinstall 钩子
□ ⭐⭐ 恶意 SKILL.md 不需要代码，只要说服你交出密钥

⭐⭐ 三方案：
□ ❌ 签名：验身份不验善意（"验证过的恶意技能仍是恶意的"）
□ ❌ 社区审计：反应式，部署后才抓到
□ ✅ ⭐ 权限清单：⭐ 主动约束"能做什么"，运行前生效
□ ⭐⭐ 目标：让它干该干的活，干不了不该干的活

□ ⭐⭐ 沉睡仓库突然更新 = 供应链红旗（养号后投毒）
```

**一句话**：

> ⭐⭐ **签名验证的是身份，不是善意——
> 一个经过验证的恶意技能，仍然是恶意的。**
