# 数据库/SQL 类技能

> ⭐ **这类技能特别适合封装**——因为规则全是**可判定的**：
> 该不该建索引、迁移安不安全，都有明确答案。

## 目录

- [安全迁移模式](#安全迁移模式)
- [索引：该建与不该建](#索引该建与不该建)
- [常见坑](#常见坑)
- [反模式](#反模式)
- [零停机：expand-contract](#零停机expand-contract)

---

## 安全迁移模式

> ⭐ **四步法（加列）**——直接抄：

```sql
-- 步骤 1：加列，允许为空
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- 步骤 2：回填既有行
UPDATE users SET status = 'active' WHERE status IS NULL;

-- 步骤 3：改成 NOT NULL
ALTER TABLE users ALTER COLUMN status SET NOT NULL;

-- 步骤 4：给新行设默认值
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';

-- ⭐ 回滚计划
ALTER TABLE users DROP COLUMN status;
```

```
□ ⭐ 每一步都要有对应的回滚语句
□ ⭐ 迁移必须带验证查询——没有后置验证的迁移
   有静默数据损坏的风险
□ ⭐ 大表（千万行以上）要加 --zero-downtime，走 expand-contract
```

> ⭐ **"直接 ALTER TABLE ... SET NOT NULL 在一亿行表上会锁表"**——
> 这是 Gotchas 的典型形态：不写下来，agent 每次都会踩。

---

## 索引：该建与不该建

**✅ 该建**：

```
□ WHERE 子句里的列
□ JOIN 条件里的列
□ ORDER BY 里的列
□ ⭐ 外键列
```

**❌ 不该建**：

```
□ ⭐ 小表（<1000 行）
□ ⭐ 低选择性的列（boolean 字段）
□ ⭐ 频繁更新的列
```

**索引类型选型**：

| 类型 | 适合 | 例子 |
|---|---|---|
| B-tree | 范围查询、排序、等值 | `CREATE INDEX idx ON tasks (status, created_date)` |
| ⭐ 部分索引 | 热数据子集 | `CREATE INDEX idx ON users (email) WHERE status='active'` |
| ⭐ 覆盖索引 | 避免回表 | `CREATE INDEX idx ON users (email) INCLUDE (name, status)` |
| Hash | 仅精确匹配 | 主键、缓存键 |
| GIN | JSONB、数组、全文 | `CREATE INDEX idx ON docs USING GIN (data)` |

```
□ ⭐ 复合索引的列顺序很重要——按选择性排序（最具选择性在前）
□ ⭐ 用 --analyze-existing 查冗余索引
□ ⭐ 复合索引顺序看似不对时：
   优化器按"估计选择性"排，不是按查询子句的顺序
```

---

## 常见坑

> ⭐ **这份清单是这类技能最值钱的部分**：

```
□ ⭐ N+1 查询——用 JOIN，不要在循环里发查询
□ 大表上做探索性查询不带 LIMIT
□ ⭐ 隐式类型转换导致索引失效
□ ⭐ 用 COUNT(*) 而 EXISTS 就够的时候
□ ⭐ NULL 处理不当（NULL = NULL 永远是 NULL，不是 TRUE）
□ ⭐ 用 SELECT DISTINCT 当创可贴，而不是修好查询本身
□ 相关操作忘记用事务
□ ⭐ 在索引列上用函数导致索引失效
□ ⭐ 避免 SELECT * ——只选需要的列
```

**关键准则**：

```
□ ⭐ 始终用参数化查询防 SQL 注入
□ 相关操作用事务保证原子性
□ 加适当的约束（PRIMARY KEY / FOREIGN KEY / NOT NULL / CHECK）
□ 表上带 created_at / updated_at
□ ⭐ 用 DECIMAL 存钱，不要用 FLOAT
□ 变长字符串用 VARCHAR 而非 CHAR
```

---

## 反模式

```
❌ 过度索引
   每列都建索引——浪费写性能与存储
   ⭐ 只给出现在 WHERE / JOIN / ORDER BY 的列建

❌ ⭐ 缺失外键
   靠应用层保证引用完整性 → 产生孤儿记录
   必须声明 FK 约束

❌ VARCHAR(255) 到处用
   过大的列在索引里浪费内存——按实际数据定长

❌ ⭐ 过早反规范化
   ⭐ 只有 EXPLAIN ANALYZE 显示 join 是瓶颈时才反规范化，
      不要提前做

❌ ⭐ 大表上直接 ALTER
   一亿行表上 SET NOT NULL 会锁表 → 用 expand-contract

❌ 迁移里没有验证查询
```

---

## 零停机：expand-contract

> ⭐ **大表迁移的正确姿势**：

```
expand（扩展）  加新结构，新旧并存，双向写入
contract（收缩） 回填完成、验证通过后，移除旧结构
```

```
□ 大表（10M+ 行）必须走这条路
□ ⭐ 列类型变更直接 ALTER COLUMN ... TYPE 可能锁表
   且遇到不兼容数据会失败
   → 用 --zero-downtime 生成带安全回填的 expand-contract
□ ⭐ 每一步前向操作都要有对应的回滚
□ ⭐ 验证查询必须在测试数据上先跑通
```

**UPSERT**（跨库差异要写清）：

```sql
-- PostgreSQL
INSERT INTO users (user_id, name, email, updated_at)
VALUES (1, 'John', 'john@example.com', NOW())
ON CONFLICT (user_id) DO UPDATE
SET name = EXCLUDED.name, email = EXCLUDED.email, updated_at = NOW();

-- MySQL
INSERT INTO users (user_id, name, email, updated_at)
VALUES (1, 'John', 'john@example.com', NOW())
ON DUPLICATE KEY UPDATE
name = VALUES(name), email = VALUES(email), updated_at = NOW();
```

> ⭐ 呼应 `skill-selection` 的 `cross-model.md` 与 `skill-crafting` 的 `script-engineering.md`：
> **跨库差异必须显式列出**，否则 agent 会用错方言。

**递归 CTE**（层级数据遍历）——也是值得写进技能的高级模式。

---

## 自查

```
□ 是否有安全迁移四步法（含回滚）？
□ ⭐ 是否警告"大表直接 SET NOT NULL 会锁表"？
□ 是否要求迁移带验证查询？
□ ⭐ 是否区分了"该建索引"与"不该建索引"（小表/低选择性/频繁更新）？
□ 是否有索引类型选型表（含部分索引与覆盖索引）？
□ ⭐ 是否说明了复合索引列顺序按选择性排？
□ 是否有常见坑清单（N+1、隐式转换、索引列上用函数等）？
□ 是否强调"用 DECIMAL 存钱"？
□ ⭐ 是否禁止过早反规范化（要 EXPLAIN ANALYZE 证明）？
□ 是否有 expand-contract 零停机模式？
□ 是否列出了跨库方言差异（UPSERT）？
□ ⭐ 是否要求参数化查询（防注入）？
□ 是否要求显式声明外键？
□ 是否有冗余索引检测？
```
