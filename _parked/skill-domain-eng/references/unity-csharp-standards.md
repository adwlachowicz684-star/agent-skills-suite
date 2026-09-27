# Unity C# 规范类技能：命名前缀与性能清单

> 相关：《skill-domain-eng》的 `gamedev-skill-routing.md` ·
> `code-review-skill-instance.md` · 《skill-crafting》的 `guidance-forms.md`

---

## 目录

- [1. 这类技能在管什么](#1-这类技能在管什么)
- [2. 命名约定（含具体前缀）](#2-命名约定含具体前缀)
- [3. ⭐ 性能清单](#3--性能清单)
- [4. ⭐ Unity 特有的坑（"假 null"）](#4--unity-特有的坑假-null)
- [5. 生命周期与物理时序](#5-生命周期与物理时序)
- [6. ⭐ Skip if 边界声明](#6--skip-if-边界声明)

---

## 1. 这类技能在管什么

Unity C# 规范类技能是**偏好型技能**的绝佳样本
（见 `capability-vs-preference.md`）：
规则明确、可机械检查、模型升级也不易破坏。

它的价值不在"教 AI 写 Unity"，
而在**让 AI 写出来的代码符合你们团队的约定**。

---

## 2. 命名约定（含具体前缀）

```
PascalCase  —— public 成员
camelCase   —— private 成员

⭐ 变量：m_VariableName
⭐ 常量：c_ConstantName
⭐ 静态：s_StaticName
```

> ⭐ 前缀这种东西**必须写进技能**——
> 模型默认不会猜到你们用 `m_` 前缀，
> 而这类不一致会在 code review 里被反复挑出来。

序列化与 Inspector：

```
[SerializeField]  应用到 private 字段（保持封装同时可 Inspector 访问）
[Header]          分组
[Range]           钳制取值范围
```

---

## 3. ⭐ 性能清单

| 项 | 做法 |
|---|---|
| **对象池** | ⭐ 频繁实例化的对象用池，`SetActive(false)` 而非 `Destroy` |
| **Draw call** | 通过合批优化 |
| **LOD** | 实现细节层次系统 |
| **Profiler** | ⭐ 用它定位瓶颈，不要靠猜 |
| **组件缓存** | ⭐ 在 `Awake` 里缓存引用 |
| **GC** | ⭐ 最小化垃圾回收 |

### 组件缓存的具体规则

```
✅ Awake 里 GetComponent 并缓存
❌ Update 里调用 GetComponent
❌ Update 里用 Find 系列方法
```

> ⭐ "在 Awake 里缓存" 比 "缓存组件引用" 有效得多——
> 后者没说在哪缓存，模型可能写在 Update 里。

### 热路径的分配

```
❌ LINQ
❌ 字符串拼接
✅ GC 安全的方法 + 缓存引用
```

---

## 4. ⭐ Unity 特有的坑（"假 null"）

> ⭐ **标准 null 检查对 Unity Object 会失效——
> 底层 C++ 对象可能已被销毁，而 C# 包装器还在。**

```
❌ obj?.Method()      Unity 不支持这样判断
✅ if (obj == null)   用重载的 bool 运算符
✅ TryGetComponent    避免 null 引用
```

> 这是 `skill-types.md` 说的 **Gotchas** 的典型形态：
> **来自实际踩过的坑，无法靠推理得出**。
> 也正因如此，它几乎不可能通过 no-op 测试——修剪时别动它。

---

## 5. 生命周期与物理时序

| 项 | 规则 |
|---|---|
| **Awake vs Start** | ⭐ `Awake` 做自身初始化；`Start` 做外部引用 |
| **FixedUpdate** | ⭐ 物理逻辑从 `Update` 迁到 `FixedUpdate`，保证时序与帧率无关 |

> 两者都是"可机械检查"的规则——
> 扫描到 `Update` 里做物理位移就该报。

---

## 6. ⭐ Skip if 边界声明

一个高质量技能会明确写"什么时候不该用我"：

```
Skip if：
  - Unreal 或 Godot 项目
  - 只需要服务端多人后端基础设施、不涉及 Unity 客户端代码
```

> ⭐ 与 `scope-section.md` 的边界章节一致。
> **没有 Skip if 的技能会被错误地用在 Godot 项目上**，
> 然后输出一堆 Unity API。

---

## 速查

| 类别 | 关键规则 |
|---|---|
| 命名 | ⭐ m_ / c_ / s_ 前缀 |
| 组件 | ⭐ Awake 缓存，Update 禁用 GetComponent/Find |
| null | ⭐ 用 `== null`，不用 `?.` |
| 生命周期 | Awake 自身 / Start 外部 |
| 物理 | ⭐ FixedUpdate |
| 池 | ⭐ SetActive(false) 而非 Destroy |
| 边界 | ⭐ 写明 Skip if |
