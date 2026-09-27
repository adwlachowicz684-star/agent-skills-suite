# Godot 信号实践：向上发信号，向下调方法

> 相关：《skill-domain-eng》的 `gamedev-skill-routing.md` ·
> `godot-composition.md`（如有）· 《skill-crafting》的 `guidance-forms.md`

---

## 目录

- [1. 信号解决什么](#1-信号解决什么)
- [2. ⭐ 方向规则](#2--方向规则)
- [3. ⭐ 何时不要用信号](#3--何时不要用信号)
- [4. 事件总线](#4-事件总线)
- [5. 依赖注入的四种方式](#5-依赖注入的四种方式)
- [6. 连接写法与断开](#6-连接写法与断开)

---

## 1. 信号解决什么

信号是 Godot 版的观察者模式。核心收益是**解耦**：

```gdscript
# ❌ 紧耦合：玩家知道整棵树
func take_damage(amount):
    health -= amount
    get_node("../../UI/HealthBar").value = health   # 知道 UI 位置
    get_node("../../AudioManager").play("hurt")     # 知道音频系统

# ✅ 解耦：只宣布发生了什么
signal health_changed(new_health)
signal damaged

func take_damage(amount):
    health -= amount
    health_changed.emit(health)
    damaged.emit()
```

> ⭐ 收益很具体：
> **加屏幕震动时再接一个监听即可，玩家代码一行不改。**
> 新反应对发射方零成本。

---

## 2. ⭐ 方向规则

```
Parent → child   : ⭐ 直接调方法（父拥有子，知道它存在）
Child  → parent  : ⭐ 发信号（子绝不能知道父是谁）
Sibling → sibling: 通过共同父节点，或 autoload 事件总线
```

> ⭐ **依赖永远只向下指**——这才让单个场景能被完整搬进另一个项目。

命名约定：**信号名用过去时**（`door_opened`、`score_changed`、`item_collected`）。

> ⭐ 过去时命名不是风格偏好，它编码了
> "这是对已发生事件的通知，不是请求"——
> 与"用信号响应、不用信号发起"是同一条规则的两面。

---

## 3. ⭐ 何时不要用信号

| 反模式 | 问题 | 替代 |
|---|---|---|
| ⭐ **信号冒泡** | 父节点转发子节点的信号 → 要开三四个文件才能追到连接 | 直接连接，或事件总线 |
| ⭐ **多步连接** | 引用传好几手才能连上 | ⭐ 事件总线 |
| 用信号发起行为 | 语义错了 | ⭐ 用方法调用发起，用信号响应 |

> ⭐ "信号冒泡"这条最有价值：
> 三个发射和连接要追踪，
> **遇到这种情况就该换方案**。
> 这与 `systematic-debugging-skill.md` 的
> "三次修复规则"是同一种思路——**给可判定的停止条件**。

---

## 4. 事件总线

```
# event_bus.gd，注册为 Autoload 名 "Events"
signal player_damaged(amount, new_health)
signal player_died
signal enemy_killed(enemy_type)
signal quest_completed(quest_id)
signal level_completed
```

任何脚本都能 emit / connect，**谁都不持有别人的引用**。

⚠️ 但有个重要的克制原则：

> ⭐ **别太早用它——多数通信是局部的。**
> 它是"上下路由变得别扭时"的泄压阀。

autoload 的取舍（与事件总线相关）：

```
autoload 引入：全局状态、全局访问（难追的 bug）、
              常常还有全局资源分配
⭐ 优先场景内状态，而非全局
只有满足三条才用 autoload：
  ① 追踪自己的数据
  ② 必须全局可访问
  ③ 独立存在，不修改其他系统的数据
  例：任务系统、对话管理器
```

> Godot 4.1 起，`class_name` + `static var/func`
> 减少了对纯辅助函数用 autoload 的必要。

---

## 5. 依赖注入的四种方式

场景需要与外部交互时，**父（或高层 API）向子注入依赖；
子绝不向上够、绝不假设环境**：

| 方式 | 用途 |
|---|---|
| ⭐ **连接信号** | 最安全；⭐ 只用于响应行为，不用于发起 |
| **调用方法** | 用于发起行为 |
| **设置 Callable 属性** | ⭐ 比传方法名安全；用于发起行为 |
| **设置 Node 引用 / NodePath** | 子使用父提供的目标 |

> ⭐ 子保持松耦合的判据：
> **没有指向父/兄弟的硬编码节点路径，不假设树结构。**

配套技巧：tool 脚本里用 `_get_configuration_warnings()`
**自文档化必需的依赖设置**（如缺失依赖时报错）。

---

## 6. 连接写法与断开

```gdscript
$Enemy.died.connect(_on_enemy_died)                       # 方法引用（最常用）
$Button.pressed.connect(func(): get_tree().quit())        # lambda（简单一行）
$Enemy.died.connect(_on_enemy_died.bind(name, xp))        # 带额外参数
$Timer.timeout.connect(_on_timeout, CONNECT_ONE_SHOT)     # 一次性
$Area.body_entered.connect(_on_entered, CONNECT_DEFERRED) # 帧末触发
```

**断开**：节点被释放时 Godot 会自动清理连接，但菜单反复开关会叠加：

```gdscript
func open_menu():
    if not $ConfirmButton.pressed.is_connected(_on_confirm):
        $ConfirmButton.pressed.connect(_on_confirm)
func close_menu():
    if $ConfirmButton.pressed.is_connected(_on_confirm):
        $ConfirmButton.pressed.disconnect(_on_confirm)
```

> ⭐ 这种"每次打开都接一次、从不断开"是最常见的泄漏——
> 与前端的事件监听器泄漏完全同构。

---

## 速查

```
□ 信号用于响应，不用于发起
□ 信号名用过去时
□ ⭐ 向上发信号，向下调方法
□ ⭐ 冒泡超过一层 → 换总线或直接连接
□ 子不持有父/兄弟的硬编码路径
□ 依赖由父注入
□ 菜单开关要成对 connect/disconnect
□ ⭐ 别太早用全局总线
```

**节点 vs 轻量类型**（性能相关）：

```
Object      最小，手动引用计数；适合自定义结构
RefCounted  引用计数；⭐ 多数不需要序列化的自定义数据用它
Resource    序列化 + Inspector；⭐ 多节点共享的数据/配置用它
```

> 数万个复杂节点会拖慢性能——
> **不需要节点特性时就别用节点**。
