# 代码质量类技能（多语言）

> ⭐ **这类技能的骨架最值得抄**——
> 一套核心规则 + 按语言的差异表 + 严重度分级。

## 目录

- [快速模式路由](#快速模式路由)
- [四语言速查表](#四语言速查表)
- [核心规则（所有语言）](#核心规则所有语言)
- [严重度分级](#严重度分级)
- [各语言的硬性红线](#各语言的硬性红线)

---

## 快速模式路由

> ⭐ **按意图只加载需要的章节**（渐进式披露的实例）：

| 意图 | 用哪些章节 |
|---|---|
| 写代码 | 核心规则 + 语言标准 + AI 友好模式 |
| 评审 PR | 评审流程 + `references/checklist.md` + 严重度分级 |
| 配 CI | 配置文件 + 脚本 + 强制策略 |
| Python 风格检查 | `references/python.md`（完整 PEP 8） |

```
□ ⭐ 深度评审时才读对应语言的 references/ 文件
□ 上下文按需加载，不一次全塞
```

---

## 四语言速查表

| 语言 | 类型安全 | Linter | 复杂度上限 |
|---|---|---|---|
| **TypeScript** | strict，⭐ **无 any** | ESLint + typescript-eslint | max 10 |
| **Python** | mypy strict，PEP 484 | Ruff + mypy | max 10 |
| **Go** | staticcheck | golangci-lint | max 10 |
| **Rust** | clippy pedantic | clippy + cargo-audit | max 10 |

---

## 核心规则（所有语言）

**类型安全**：

```
□ 无隐式 any / 无未标注类型的函数
□ ⭐ 不带守卫的类型断言一律禁止
□ ⭐ 公开 API 必须有显式返回类型
```

**安全**：

```
□ ⭐ 无硬编码密钥（用 gitleaks）
□ ⭐ 无 eval / pickle / 不安全的反序列化
□ ⭐ 只用参数化查询
□ ⭐ SCA 扫描（npm audit / pip-audit / govulncheck / cargo-audit）
```

**复杂度**（具体数字，可直接进 CI）：

```
□ ⭐ 圈复杂度上限 10
□ ⭐ 函数行数上限 50
□ ⭐ 嵌套深度上限 3
□ ⭐ 参数个数上限 5
```

**错误处理**：

```
□ 不允许忽略错误（Go：不用 _ 接 err）
□ 不允许裸 except（Python）
□ ⭐ 生产代码不允许 unwrap（Rust）
□ ⭐ 错误要带上下文包装
```

**测试覆盖率**：

```
行覆盖    最低 80%
分支覆盖  最低 70%
⭐ 新增代码 最低 90%
```

---

## 严重度分级

| 级别 | 内容 | 动作 |
|---|---|---|
| **Critical** | ⭐ 安全漏洞、数据丢失 | ⭐ 阻断合并 |
| **Error** | Bug、类型违规、`any` | ⭐ 阻断合并 |
| **Warning** | 代码异味、复杂度 | 必须处理 |
| **Style** | 格式、命名 | ⭐ 自动修复 |

> ⭐ **"Style 自动修复"是个好设计**——
> 把风格问题交给 formatter，评审带宽留给真正的问题。
> 呼应 `skill-governance` 的 `ci-cd-integration.md`：机器能检查的交给 hook/CI。

---

## 各语言的硬性红线

**TypeScript**：

```typescript
// ⭐ CRITICAL: 绝不用 any
const bad: any = data;      // Error
const good: unknown = data; // OK

// ⭐ ERROR：类型断言
const bad = data as User;              // Error
const good = isUser(data) ? data : null; // OK

// ⭐ ERROR：非空断言
const bad = user!.name;        // Error
const good = user?.name ?? ''; // OK
```

**Python（PEP 8 / 3.11+）**：

```python
# ⭐ CRITICAL: 所有函数必须标注类型
def bad(data):                              # Error
    return data
def good(data: dict[str, Any]) -> list[str]: # OK
    return list(data.keys())

# 用现代语法
value: str | None = None   # OK（不用 Optional）
items: list[str] = []      # OK（不用 List）
```

**Go**：

```go
// ⭐ CRITICAL: 绝不忽略错误
result, _ := doSomething()  // Error
result, err := doSomething() // OK
if err != nil {
    return fmt.Errorf("doing something: %w", err)
}
```

**Rust**：

```rust
// ⭐ CRITICAL: 生产代码不 unwrap
let value = data.unwrap();          // Error
let value = data?;                  // OK
let value = data.unwrap_or_default(); // OK
```

**跨语言：结构化日志**（四语言各给一份，避免模型写错方言）：

```typescript
logger.info({ userId, action: 'login' }, 'User logged in'); // pino
```
```python
logger.info("user_login", user_id=user_id)  # structlog
```
```go
log.Info().Str("user_id", userID).Msg("user logged in") // zerolog
```

> ⭐ 呼应 `database-sql-skills.md` 的 UPSERT 方言差异：
> **跨语言/跨库的差异必须显式列出**。

---

## 自查

```
□ 是否按意图做了章节路由（而非一次全读）？
□ ⭐ 是否有四语言速查表（类型安全/linter/复杂度）？
□ 核心规则是否含具体数字（复杂度 10、函数 50 行、嵌套 3、参数 5）？
□ ⭐ 是否有严重度分级且明确了"阻断合并"的级别？
□ ⭐ Style 是否自动修复（释放评审带宽）？
□ ⭐ 各语言是否有硬性红线（TS 无 any / Go 不忽略 err / Rust 不 unwrap）？
□ ⭐ 红线是否给了"错误写法 vs 正确写法"对照？
□ Python 是否用了现代语法（str | None 而非 Optional）？
□ 是否要求显式返回类型（公开 API）？
□ ⭐ 安全规则是否含 gitleaks 与 SCA？
□ 是否禁止 eval/pickle/不安全反序列化？
□ 覆盖率是否分层（新增代码 90% 高于整体 80%）？
□ ⭐ 跨语言差异（如结构化日志）是否逐语言列出？
□ 是否有 AI 友好模式章节？
```
