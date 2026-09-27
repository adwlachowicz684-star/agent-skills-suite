# 代码简化类技能：脚本驱动 + 何时不该简化

> 一个把"确定性检查"用到极致的语言简化技能：
> **7 个分析脚本 + 反模式表 + 明确的"何时不做"**。

## 目录

- [脚本驱动的分析](#脚本驱动的分析)
- [六类代码异味](#六类代码异味)
- [过度工程的六种反模式](#过度工程的六种反模式)
- [惯用法改写对照](#惯用法改写对照)
- [⭐ 何时不该简化](#-何时不该简化)
- [可迁移的三条做法](#可迁移的三条做法)

## 脚本驱动的分析

**关键设计**：把"判断"用脚本做，模型负责"改写"。

```bash
# 综合分析（跑全部检查）
python scripts/analyze_all.py /path/to/project

# 单独的分析器
python scripts/analyze_complexity.py .       # 圈复杂度/认知复杂度
python scripts/find_code_smells.py .         # 可变默认参数、裸 except 等
python scripts/find_overengineering.py .     # YAGNI 违规、未用抽象
python scripts/find_dead_code.py .           # 未用的导入/函数/变量
python scripts/find_unpythonic.py .          # 非惯用模式
python scripts/find_coupling_issues.py .     # 特性依恋、低内聚
python scripts/find_duplicates.py .          # ⭐ 基于 AST 归一化的结构重复

# JSON 输出，供 CI/工具链消费
python scripts/analyze_all.py . --format json
```

> ⭐ **七个脚本各管一类**——呼应 `language-reviewer-skills.md`
> **按类别切分而非按语言切分**的矩阵思路。

**为什么必须脚本化**：

```
□ "圈复杂度 >10"是可判定的 → 脚本
□ "这段代码太绕了"是判断   → 模型
□ ⭐ 混在一起会让模型自己算复杂度，而且算不准
```

呼应 `script-engineering.md`（**`skill-crafting`**）：
**确定性推进代码**。

## 六类代码异味

| 异味 | 检测 | 修法 |
|---|---|---|
| 可变默认参数 | `def f(x=[])` | 用 `None`，在函数内创建 |
| 裸 except | `except:` | `except Exception:` |
| God class | 15+ 方法、10+ 属性 | 拆成聚焦的类 |
| 长函数 | 50+ 行 | ⭐ 提取辅助函数 |
| 深嵌套 | 4+ 层 | ⭐ 提前返回、提取 |
| 特性依恋 | 方法更多用别的类 | ⭐ 移动方法 |
| 魔法数字 | 无解释的数字字面量 | 命名常量 |

**量化阈值是重点**：

```
God class：15+ 方法、10+ 属性
长函数：50+ 行
深嵌套：4+ 层
```

> ⭐ **没有数字的检查项等于没有检查项**。
> 呼应 `design-system-skills.md` 的"可自动检查的验收清单"，
> 与 `a11y-skills.md` 的"4.5:1 / 3:1"——
> **数字让规则从建议变成断言**。

## 过度工程的六种反模式

| 模式 | 问题 | 解法 |
|---|---|---|
| 单一实现接口 | 抽象类只有一个子类 | 合并，或等真的需要再拆 |
| 不必要的工厂 | 工厂只创建一种类型 | 直接实例化 |
| 过早的策略 | 策略模式只有一个策略 | 简单函数 |
| 薄包装器 | 类只是转发 | 直接用被包装的类 |
| 投机性通用 | 为"未来需求"写代码 | ⭐ 删掉（YAGNI） |
| 深继承 | 4+ 层继承 | ⭐ 用组合而非继承 |

> ⭐ 这条清单本身就是 Gotchas——
> 它编码的是"看起来专业实际有害"的模式，
> 通用知识推不出来。

## 惯用法改写对照

**提前返回**（消深嵌套）：

```python
# Before：层层嵌套
def process(data):
    if data:
        if data.valid:
            if data.ready:
                return compute(data)
    return None

# After：卫语句
def process(data):
    if not data or not data.valid or not data.ready:
        return None
    return compute(data)
```

**推导式**：

```python
result = [item.name for item in items if item.active]
```

**字典技巧**：

```python
value = d.get(key, default)          # 而不是 if key in d
groups = defaultdict(list)           # 而不是手动初始化分组
```

**上下文管理器**：

```python
with open('file.txt') as f:
    data = f.read()
```

**复杂条件提取**：

```python
# Before：一行塞不下
if user.age >= 18 and user.country in ALLOWED and not user.banned:

# After：命名意图
if is_eligible:
```

> ⭐ **最后一条常被忽略但价值最高**——
> 它改的不是语法，是**把条件命名成一个意图**。

## ⭐ 何时不该简化

> **这份技能最值得抄的一节：显式列出不做的场景。**

```
❌ 没有测试的老旧可运行代码
❌ ⭐ 性能关键的热路径（先测量再动）
❌ 即将被替换的代码
❌ 外部 API 约束导致的必要复杂
```

**为什么必须有这一节**：

```
□ 模型默认倾向"把代码改得更漂亮"
□ ⭐ 没有排除清单，它会去重构没有测试覆盖的祖传代码
□ 而那正是最不该碰的地方
```

呼应 `legacy-modernization.md` 的
**"先修关键 bug、建安全网，再动结构"**——同一条纪律。

## 可迁移的三条做法

**① 检测脚本化，改写交给模型**

```
可判定的度量 → scripts/（可 CI、可 JSON 输出）
需要审美与上下文的改写 → 模型的活
```

**② 每条异味都要有数字阈值**

```
❌ "函数不要太长"
✅ "函数 50+ 行 → 提取辅助函数"
```

**③ 显式写"何时不做"**

```
□ 这份技能的四条排除项
□ ⭐ 比"什么时候做"更能防止破坏
```

呼应 `what-not-to-do.md`（**`skill-authoring`**）：
**先写"不做什么"，再写"做什么"**。

## 多语言版本

同一模式在其他语言上的对应：

```
python-simplifier     → Pythonic 模式、ruff、pydantic
typescript-simplifier → 现代 ES 特性
go-simplifier         → 惯用错误处理、接口、并发、标准库约定
rust-simplifier       → 所有权、错误处理、trait、迭代器
swift-simplifier      → 可选值、协议、值语义、并发
```

> ⭐ **注意每个语言的"惯用"内容完全不同**——
> 这印证了 `language-reviewer-skills.md` 的矩阵必要性：
> **不能用一个通用的"简化"规则套所有语言**。

## 自查

- [ ] 度量类检查用脚本做了吗？
- [ ] 每条异味都有数字阈值吗？
- [ ] 有"何时不该简化"一节吗？
- [ ] 惯用法改写是 Before/After 对照吗？
- [ ] 覆盖了"把条件命名为意图"这类非语法改进吗？
- [ ] 按语言分开了吗？
