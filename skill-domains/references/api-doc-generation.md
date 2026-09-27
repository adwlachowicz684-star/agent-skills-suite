# API 文档生成类技能

> 相关：（领域实例库·已归档） 的 `api-design-skills.md` ·
> `documentation-skills.md` · `skill-crafting` 的 `output-contract.md`

---

## 目录

- [1. ⭐ 关键前提：Claude 无法文档化不存在的东西](#1--关键前提claude-无法文档化不存在的东西)
- [2. 五步工作流](#2-五步工作流)
- [3. ⭐ 输出模板：定义一次，全队一致](#3--输出模板定义一次全队一致)
- [4. 让文档不腐烂：与代码同步](#4-让文档不腐烂与代码同步)
- [5. 四个常见故障](#5-四个常见故障)
- [6. 约定要写下来](#6-约定要写下来)

---

## 1. ⭐ 关键前提：Claude 无法文档化不存在的东西

```
缺参数文档  → 在源码里补 JSDoc 注释
            ⭐ Claude 无法文档化"不在那里"的东西
```

这不是技能的局限，是物理限制。
**生成的文档质量上限 = 源码注释的质量。**

典型的已注释源码：

```javascript
/**
 * Fetch a user by their unique identifier.
 * @param {string} userId - The user's unique ID
 * @param {Object} options - Fetch options
 * @param {boolean} options.includeProfile - Include full profile data
 * @returns {Promise} The user object
 * @throws {NotFoundError} When user does not exist
 */
async function getUser(userId, options = {}) { ... }
```

---

## 2. 五步工作流

| 步骤 | 做什么 |
|---|---|
| 1 | 建文档目录结构（`docs/api-reference/`） |
| 2 | 在源码里写 JSDoc/类似注释 |
| 3 | 定义范围：扫哪些目录、输出什么 |
| 4 | 生成初版，⭐ **审查输出填补源码注释的缺口** |
| 5 | 格式化与自动化更新 |

第 4 步的典型输出值得看——**它会主动报告缺失**：

```
Processing: src/api/users.js
  - getUser(userId, options)
  - createUser(data)
  - updateUser(userId, data)
  - ⭐ MISSING return docs
Processing: src/api/orders.js
  - getOrder(orderId)
  - listOrders(filters)
  - ⭐ MISSING examples
```

> ⭐ **"MISSING xxx" 这种主动标记是这类技能的关键设计**——
> 它把"静默产出不完整文档"变成"明确指出缺什么"。

---

## 3. ⭐ 输出模板：定义一次，全队一致

**端点文档模板**：

```markdown
Endpoint: POST /users/register
Method: POST
Description: Creates a new user account and returns a session token.

Request
interface RegisterRequest {
  email: string; password: string; displayName?: string;
}

Response
interface RegisterResponse {
  data: { userId: string; sessionToken: string; expiresAt: string };
  error: null;
}

Error Codes
| Code | HTTP | Description |
| EMAIL_TAKEN | 422 | Email already registered |
| WEAK_PASSWORD | 422 | Password too weak |
| RATE_LIMITED | 429 | Too many attempts |

Example Usage
curl -X POST https://api.example.com/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"u@e.com","password":"Sec123!"}'
```

> ⭐ **把模板定义在技能里，意味着团队每个人生成的文档格式都一样，
> 与个人习惯或 prompt 措辞无关。**

这是 `output-contract.md` 那条"输出格式要显式指定"的直接收益。

---

## 4. 让文档不腐烂：与代码同步

```
任何 API 变更后 → 跑生成命令
               → git diff 与上一版比对
               → ⭐ 文档与代码一起提交
```

> ⭐ **文档与代码同提交**是防止腐烂的唯一有效手段
> ——分开提交必然漂移。

---

## 5. 四个常见故障

| 故障 | 修法 |
|---|---|
| 缺参数文档 | 在源码补 JSDoc |
| 返回类型过时 | ⭐ 跑测试类技能交叉比对文档类型与实际实现 |
| 格式不一致 | 定义风格指南并在每次生成时引用 |
| ⭐ 大 API 超时 | ⭐ **分模块处理再合并** |

最后一条很实用：**不要一次性生成整个大 API**，
按模块分别生成，最后合并成一份。

---

## 6. 约定要写下来

文档约定必须持久化，否则每次重新生成都会不一致。

```markdown
- 可选参数用 [] 包裹
- 返回类型用 TypeScript 风格记法
- 示例同时给出成功与错误两种情况
- 每个端点都要有 curl 命令
```

> ⭐ 这些约定属于 `instruction-layering.md` 里的持久上下文，
> 写进技能或 CLAUDE.md，不要靠每次口头说。

---

## 速查

| 问题 | 处置 |
|---|---|
| 文档缺参数 | 补源码注释（根本解法） |
| 类型过时 | 与测试交叉比对 |
| 格式每次不一样 | 模板 + 风格指南写进技能 |
| 大 API 卡住 | 分模块生成再合并 |
| 文档腐烂 | ⭐ 文档与代码同提交 |
