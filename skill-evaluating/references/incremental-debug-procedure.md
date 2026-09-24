# 增量验证：从最小配置一步步加

> 相关：《skill-evaluating》的 `test-pyramid.md` ·
> `troubleshooting-manual.md` · 《skill-patterns》的 `nine-checks-not-working.md`
> 前置：那些文档讲"故障后怎么定位"，
> 这份讲⭐ 开发过程中怎么用增量方式让故障根本不发生。

---

## 目录

- [1. ⭐ 先用最小配置验证](#1--先用最小配置验证)
- [2. ⭐⭐ 增量加功能，每步都验证](#2--增量加功能每步都验证)
- [3. ⭐ diff 测试](#3--diff-测试)
- [4. 常见错误与修法](#4-常见错误与修法)
- [5. 测试用例要文档化](#5-测试用例要文档化)

---

## 1. ⭐ 先用最小配置验证

> ⭐ **先用最小内容确认技能被识别。**

```markdown
---
name: test-skill
description: Test skill
---

## Instructions

Output "Test successful".
```

```
⭐ 如果 /test-skill 能跑，基础设置就是对的。
```

> ⭐ 这一步的价值是**把"技能根本没被识别"和"技能逻辑有问题"
> 一次性分开**——和 `nine-checks-not-working.md` 的显式调用是同一招，
> 只不过这个更早、更便宜。

---

## 2. ⭐⭐ 增量加功能，每步都验证

```
⭐ 一次性构建复杂技能会让问题定位变得困难。
```

**推荐顺序**（每步验证过再走下一步）：

```
Step 1: 验证最小配置能跑        ✓
Step 2: 加基本指令
Step 3: 定义输出格式
Step 4: 加 references/
Step 5: 加 scripts/（如果需要）
```

> ⭐ **每步都验证，就能快速定位问题出在哪一步。**
>
> 这与 `argument-substitution.md` 的"一次只改一处"是同一条纪律：
> **同时改多处，出问题就分不清是哪个引起的。**

---

## 3. ⭐ diff 测试

```
⭐ 出问题时，和能用的版本对比：

diff working-skill/SKILL.md broken-skill/SKILL.md
```

**可用的调试手段**：

```
· /skills 命令：查看当前激活的技能
   ⭐ 如果技能没出现 = 位置或格式问题
· ⭐ 提高日志级别看技能加载状态
· ⭐ claude --debug：查看加载错误，搜索你的技能名
   ⭐ 有时仅靠这一步就能直接定位
```

---

## 4. 常见错误与修法

**YAML 解析错误**（最常见）：

```yaml
# ✗ 冒号后没空格
name:my-skill
# ✗ 引号不匹配
description: "description text'
# ✓
name: my-skill
description: "description text"
```

**字符编码问题**：重新存为 **UTF-8（无 BOM）**。

**`scripts/` 不执行**：

```
⭐ 原因①：没有执行权限 → chmod +x scripts/my-script.sh
⭐ 原因②：工具不支持 scripts/
⭐ ⭐ 建议：⭐ 提供一个不依赖 scripts/ 的回退路径
```

> ⭐ 第 ② 条的回退建议很实用：
> **不要让你的技能在没有脚本能力时完全瘫痪**——
> 至少退化成"用自然语言指导模型自己做"。

**官方课程给出的五类故障与处置**（顺序即优先级）：

```
1. 不触发 → ⭐ 先改 description，覆盖用户真实会说的语句
2. 不加载 → 先查目录、SKILL.md 文件名、YAML 格式
3. 调错技能 → ⭐ 让名称和描述更有区分度
4. 同名冲突 → 检查企业级/个人级/项目级/插件级优先级
5. ⭐ 运行失败 → ⭐ 最后才查依赖、执行权限、路径分隔符
```

> ⭐ 第 5 条的措辞值得注意：**"运行失败"才查依赖与权限**。
> 多数人一上来就查这些，但按概率它们排最后。

**运行时错误三项**：

```
依赖缺失 · 文件权限（chmod +x）· ⭐ 路径分隔符（⭐ 统一用正斜杠）
```

---

## 5. 测试用例要文档化

```markdown
## Test Cases

### TC-1: 基本操作
- Input: `/code-review src/index.ts`
- Expected: JSON 格式的审查结果

### TC-2: 未指定文件
- Input: `/code-review`
- Expected: 错误 "Please specify a file"

### TC-3: 文件不存在
- Input: `/code-review nonexistent.ts`
- Expected: 错误 "File not found"
```

> ⭐ 三类用例的划分与 `three-failure-modes.md` 的
> 正例/反例/边界例一致：**正常 / 缺参数 / 坏输入**。

**回归测试**：

```
⭐ 更新技能后，重跑之前通过的用例。
```

这与 `skill-ownership-changeflow.md` 的"任何修改必须跑 eval"是同一条。

---

## 速查

```
□ ⭐ 先最小配置确认被识别（把"没识别"和"逻辑错"一次分开）
□ ⭐⭐ 增量加功能：最小→指令→输出格式→references→scripts
□ ⭐ 每步验证；⭐ 一次只改一处
□ ⭐ 出问题 diff 能用的版本
□ /skills 查激活；⭐ claude --debug 查加载错误
□ YAML：冒号后空格、引号匹配
□ 编码：UTF-8 无 BOM
□ ⭐ scripts 不执行：chmod +x，或⭐ 提供无脚本回退路径
□ ⭐ 故障顺序：不触发→不加载→调错→同名冲突→⭐ 最后才查依赖权限
□ ⭐ 路径统一正斜杠
□ 测试用例三类：正常/缺参数/坏输入
□ ⭐ 更新后重跑历史用例
```

**一句话**：

> ⭐ **一次性构建复杂技能，等于放弃定位问题的能力。**
