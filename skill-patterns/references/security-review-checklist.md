# 实例：安全审查清单类技能

> OWASP Top 10 是最常被做成技能的内容之一。
> ⭐ 这份讲这类清单**怎么组织才真的会被逐条执行**。

## 目录

- [它长什么样](#它长什么样)
- [为什么清单能起作用](#为什么清单能起作用)
- [好坏写法的关键差别：DANGEROUS / SAFE 对照](#好坏写法的关键差别dangerous--safe-对照)
- [可迁移的三条](#可迁移的三条)
- [一个警告](#一个警告)
- [自查](#自查)

## 它长什么样

典型的组织方式：按 OWASP 分类分节，每节一个 checkbox 列表。

```
### A01: Broken Access Control
- [ ] Authorization checks on every endpoint
- [ ] Deny by default policy
- [ ] CORS properly configured
- [ ] Directory listing disabled
- [ ] JWT tokens validated server-side

### A02: Cryptographic Failures
- [ ] No sensitive data in URLs
- [ ] HTTPS enforced everywhere
- [ ] Strong encryption algorithms (AES-256, RSA-2048+)
- [ ] Passwords hashed with bcrypt/argon2
- [ ] No hardcoded secrets
...
```

## 为什么清单能起作用

> ⭐ **模型具备"看出 SQL 注入"的能力，
> 缺的是"记得检查这一整类"。**

这正是技能该做的事——
**不是教它什么是注入，而是保证它不漏掉检查项**。

判据（见 `capability-vs-process.md`）：
这属于**流程原语**，不是能力原语。

## 好坏写法的关键差别：DANGEROUS / SAFE 对照

清单本身只解决"记得查"。
真正让它有效的是**代码模式对照**：

```python
# DANGEROUS: SQL Injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# SAFE: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

```javascript
// DANGEROUS: XSS
element.innerHTML = userInput;
// SAFE: Text content
element.textContent = userInput;
```

```bash
# DANGEROUS: Command injection
os.system(f"ping {hostname}")
# SAFE: Use subprocess with list
subprocess.run(["ping", hostname], check=True)
```

> ⭐ **每一对都给了"错的样子"和"对的样子"——
> 这是 `guidance-forms.md` 里"配方"形态的教科书示范。**

对照只有 DANGEROUS 没有 SAFE 的写法：
模型知道这段代码有问题，但不知道该改成什么，
于是会自己编一个——可能引入新问题。

## 可迁移的三条

**① 分类要封闭**

```
OWASP Top 10 = 10 类，每一类都是有限的
```

> ⭐ **一个可穷举的分类是清单类技能的前提。**
> 如果类别是开放的，模型会不断漏掉没列出来的。

**② 每类下的条目要可判定**

```
✅ "JWT tokens validated server-side"
✅ "Passwords hashed with bcrypt/argon2"
❌ "认证要做得安全"          ← 无法判定
```

**③ ⭐ 给出安全默认值**

```
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000
```

直接给能复制的配置，而不是"要配置安全响应头"。

## 一个警告

> ⚠️ **OWASP Top 10 有版本（2021 vs 2017 vs 更新的）。**

写进技能时必须标注版本：

```
✅ "OWASP Top 10 (2021)"
❌ "OWASP Top 10"          ← 三年后没人知道是哪一版
```

而且技能要包含**更新机制**：
这类清单会随标准演进而失效，
属于 `lifecycle.md` 里最需要定期复查的一类内容。

配套建议：

```
□ ⭐ 标注版本与生效日期
□ ⭐ 把"如何更新这份清单"写进技能或维护文档
□ 定期复查（见 lifecycle 的 MATURE 阶段）
```

**第二个警告**：清单类技能容易触发**过度验证**。

`failure-modes.md` 的实测：

```
⭐ 过度验证是最大的单一成本源（67/182 退化）
   ——把可选工作变成强制工作是成本杀手
```

所以对安全审查尤其要注意：

```
□ 分"必做"和"按需"，不要一律"总是检查"
□ ⭐ 写"若涉及用户输入则检查 X"
   而不是"总是检查 X"
```

## 自查

```
[ ] 分类是封闭可穷举的吗？
[ ] 每条都能被判定（而不是"要安全"）？
[ ] ⭐ 每个危险模式都配了对应的安全写法？
[ ] 安全默认值能直接复制吗？
[ ] ⭐ 标注了标准的版本与生效日期？
[ ] 区分了"必做"与"按需"？
[ ] 有明确的输出格式（severity + file:line）？
```

最后一条：清单类技能的**输出**也要结构化——
否则 10 类检查跑完，产出的是一段难以执行的散文。

参考格式：

```
[severity] [file:line] [问题]
Fix: [具体建议]
```
