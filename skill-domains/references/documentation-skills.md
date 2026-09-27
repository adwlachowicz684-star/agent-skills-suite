# 文档类技能

> ⭐ **文档技能的核心不是"写得更长"，而是"更易审计"。**

## 目录

- [文档技能的分阶段结构](#文档技能的分阶段结构)
- [README 质量清单](#readme-质量清单)
- [API 文档的必含元素](#api-文档的必含元素)
- [写作风格：Do / Don't](#写作风格do--dont)
- [反模式：为自己写 vs 为用户写](#反模式为自己写-vs-为用户写)
- [Changelog](#changelog)

---

## 文档技能的分阶段结构

> 一个成熟实现把文档工作拆成 7 个阶段，
> 每阶段声明"要调用哪些技能、做哪些动作"：

```
Phase 1 API 发现     盘点端点、请求/响应、认证、错误码、限流
Phase 2 OpenAPI 规范  建 schema、路径、安全、示例
Phase 3 开发者指南    快速上手、认证指南、常见模式、排错、FAQ
Phase 4 代码示例      示例请求、SDK 示例、curl 示例、教程
Phase 5 交互式文档    Swagger UI / Redoc / try-it
Phase 6 文档站        平台选择、结构设计、导航、搜索
Phase 7 维护          自动生成、校验、评审流程、更新排期、反馈监测
```

**质量关卡**（放在技能末尾，作为完成判定）：

```
□ OpenAPI 规范完整
□ 开发者指南已写
□ ⭐ 代码示例可运行
□ 交互式文档可用
□ 文档已部署
```

> ⭐ **"代码示例可运行"** 呼应 `skill-crafting` 的 `grounding-verification.md`——
> 写了不等于能跑，必须有验证步骤。

**一条值得抄的 Limitations 声明**：

```
□ 只在任务明确匹配上述范围时使用
□ ⭐ 不要将输出当作环境特定验证、测试或专家评审的替代品
□ 若缺少必要输入、权限、安全边界或成功标准，停下来询问
```

---

## README 质量清单

```
□ 标题清楚标识项目
□ ⭐ 一句话说清它做什么
□ 安装步骤在全新系统上可行
□ ⭐ 快速上手让用户 5 分钟内跑起来
□ ⭐ 所有代码示例都测过且是最新的
□ 配置选项都有文档
□ 相关文档链接有效
```

> ⭐ 呼应 `skill-refining` 的 `anti-patterns-practice.md` 的坑 3：
> **代码示例会过时**——所以清单里明确要求"测过且最新"。

---

## API 文档的必含元素

| 元素 | 何时包含 |
|---|---|
| Description | **总是**——做什么 |
| Parameters | **总是**——每个的类型与用途 |
| Returns | **总是**——返回什么 |
| Throws | 可能出错时 |
| **Example** | **总是**——真实用法 |
| Since | 有版本 API |
| Deprecated | 有替代功能时 |

**示例格式**（Google / NumPy / Sphinx 三选一，写进技能）：

```python
def calculate_total(items, tax_rate):
    """Calculates the total price including tax.

    Args:
        items: Array of items with price property
        taxRate: Tax rate as decimal (e.g., 0.08 for 8%)

    Returns:
        Total price with tax applied

    Raises:
        Error: If items array is empty

    Example:
        calculateTotal([{price: 10}, {price: 20}], 0.08)
        # Returns: 32.40
    """
```

> ⭐ **`Example` 标为"总是"**——
> 呼应 `skill-authoring` 的 `examples.md`：示例是 agent 理解期望形状的最快通道。

**用户指南的四段结构**：

```
Getting Started   前置条件 · 安装 · ⭐ 第一次成功（quick win）· 常见坑
Core Concepts     关键术语 · 如何运作 · 心智模型
How-To Guides     任务导向 · 分步 · 预期结果
Reference         完整选项列表 · API 参考 · 配置参考
Troubleshooting   常见错误与修复 · FAQ · 求助途径
```

---

## 写作风格：Do / Don't

> ⭐ **这类清单最适合放进技能**——全是可观察、可检查的动作。

**Do**：

```
□ 用主动语态
  ✅ "Run the command"   ❌ "The command should be run"
□ ⭐ 先说目标
  ✅ "To deploy to production, run..."
□ 给出预期输出
□ 相关时提供替代方案
```

**Don't**：

```
□ ❌ 不说明前置条件就假定读者已有知识
□ ❌ 跳过"看起来显然"的步骤
□ ❌ 用不加解释的行话
□ ❌ 写没有结构的大段文字
```

---

## 反模式：为自己写 vs 为用户写

> ⭐ **这是文档技能里最有价值的一条对比**：

```
❌ Bad（为自己写）
   "The frobnicator uses a modified Dijkstra algorithm
    with O(n log n) complexity for path optimization."

✅ Good（为用户写）
   "The route finder calculates the fastest path between
    locations. For most routes, results appear in under 1 second."
```

> ⭐ **差别在于：作者懂了 vs 读者能用。**
> 复杂度分析让作者显得专业，但不帮读者决定要不要用。

**第二条同样重要**：

```
❌ Bad  "Run npm start to begin."
✅ Good "Starting the Development Server
        运行开发服务器以实时查看你的改动：
        bash: npm start
        ⭐ 这会启动 http://localhost:3000 的服务。
           源文件改动会自动刷新浏览器。"
```

> ⭐ **"跳过显而易见步骤"是最常见的文档缺陷**——
> 因为对作者显而易见，对读者不是。

---

## Changelog

**格式**（Keep a Changelog）：

```markdown
## [Unreleased]
### Added / Changed / Fixed

## [1.0.0] - 2024-01-15
### Added
- Initial release features
### Security
- Security fix description
```

**六类变更**：

```
Added      新功能
Changed    现有功能的改动
Deprecated 将要移除的功能
Removed    已移除的功能
Fixed      bug 修复
Security   安全漏洞修复
```

**四条最佳实践**：

```
□ ⭐ 为用户写，不是为开发者写
□ 破坏性变更要附迁移说明
□ 链接到 issue/PR 提供上下文
□ 一致使用语义化版本
□ 条目简洁但信息充分
```

---

## 自查

```
□ 是否把文档工作拆成了阶段（而非一个笼统流程）？
□ 每阶段是否声明了"要调用什么、做什么动作"？
□ 质量关卡是否含"代码示例可运行"？
□ 是否有 Limitations 声明（不做环境验证、缺输入就停）？
□ README 清单是否含"5 分钟跑起来"与"示例测过且最新"？
□ API 文档是否标明了哪些元素"总是"需要？
□ 是否指定了 docstring 风格（Google/NumPy/Sphinx）？
□ 是否有写作风格的 Do/Don't 清单？
□ ⭐ 是否有"为自己写 vs 为用户写"的对比示例？
□ 是否强调不跳"显而易见"的步骤？
□ Changelog 是否含安全类与迁移说明？
```
