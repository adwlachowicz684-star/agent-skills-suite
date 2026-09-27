# 游戏状态机：从 switch 到状态模式的可迁移结构

> 相关：《skill-domain-eng》的 `gamedev-skill-routing.md` ·
> `save-system-skill.md` · 《skill-crafting》的 `guidance-forms.md`

---

## 目录

- [1. 最简单的形态](#1-最简单的形态)
- [2. ⭐ 状态表驱动](#2--状态表驱动)
- [3. ⭐ 为什么 switch 是好起点](#3--为什么-switch-是好起点)
- [4. ⭐ 暂停的坑](#4--暂停的坑)
- [5. 与存档的整合](#5-与存档的整合)

---

## 1. 最简单的形态

```cpp
void Game::Run() {
    while (running_) {
        switch (state_) {
            case GameState::Menu:       UpdateMenu();     break;
            case GameState::Explore:    UpdateExplore();  break;
            case GameState::Battle:     UpdateBattle();   break;
            case GameState::GameOver:   UpdateGameOver(); break;
        }
    }
}
```

> ⭐ 主循环**只做一件事：看当前状态，调用对应函数**。
> 状态由各函数内部自行改变（如 `UpdateMenu` 检测到"开始游戏"
> 就自己 `state_ = Explore`）。

---

## 2. ⭐ 状态表驱动

| 状态 | 进入条件 | 退出条件 |
|---|---|---|
| Menu | 程序启动 | 玩家选择新建游戏或读档 |
| Explore | 菜单确认开始 | 踩到怪物事件 / 被陷阱杀死 |
| Battle | 探索中踩到战斗格子 | 怪物死亡 / 玩家逃跑 |
| GameOver | 玩家 HP 归零 | 选择重开或退出 |

> ⭐ **这张表本身就是技能里该有的东西**——
> 它把"状态机怎么写"从抽象问题变成查表。
> 与 `methodology-skills.md` 的"公式选择表"同一种设计。

---

## 3. ⭐ 为什么 switch 是好起点

> ⭐ **如果以后想升级为状态模式，把每个 `UpdateX` 抽成独立类即可，
> 主循环甚至不需要改动。**

这是个很实用的渐进建议：

```
① 先用 switch（简单、可调试）
② 状态变多、每个状态逻辑变重时，再抽成类
③ ⭐ 因为这个结构，迁移成本很低
```

> 与 `first-skill-minimal.md` 的"第一个技能可以只有 10 行"、
> `catalog-shape.md` 的渐进复杂度同构——
> **先跑通简单版，再按需升级**。

---

## 4. ⭐ 暂停的坑

一个 Unity 场景里非常典型的问题：

```
Time.timeScale = 0 之后：
  ✅ 玩家移动停了
  ✅ 动画停了
  ❌ ⭐ 动画回调、协程、UI 动画可能还在跑
     —— 部分 Tween 插件用 Time.unscaledDeltaTime，不会自动暂停
  ❌ ⭐ 暂停时调用 Rigidbody 操作可能导致物理穿透
```

**正确做法**：

```
⭐ 暂停不能只靠 timeScale
⭐ 还要在 UIManager 里统一处理：
   弹出暂停面板时，把所有动态元素禁用或切到 unscaledTime 模式
```

> ⭐ 这类"看起来做了但实际上漏了一半"的坑，
> 正是 Gotchas 章节最该收录的内容——
> 来自真实踩坑，无法靠推理得出。

---

## 5. 与存档的整合

> ⭐ **状态机数据不是孤立的**——
> 当前状态、内部变量、历史信息都要与玩家属性、背包、
> 世界状态、任务进度一同序列化。

加载后两条验收标准（可直接做 eval 断言）：

```
① 一致性：HP 加载为 50 → UI 血条与内部属性都必须反映
② ⭐ 行为正确性：加载后状态机行为与保存前完全一致
   —— AI 继续之前的决策流程，玩家输入得到预期响应
```

详见 `save-system-skill.md` 第 4 节的统一存档管理器模式，
以及**加载顺序**（世界状态先于实体状态）。

---

## 速查

```
□ 状态表是否列出（进入条件 / 退出条件）
□ 主循环是否只做分派
□ 状态切换是否在状态函数内部
□ ⭐ 暂停是否只靠 timeScale（坑）
□ 状态机数据是否纳入存档
□ ⭐ 加载顺序：世界先于实体
□ 是否需要从 switch 升级为状态模式（按需，别提前）
```

**与状态机配合的常见系统**：

```
平台跳跃  coyote time、跳跃缓冲、可变跳跃高度、单向平台
战斗      连招、受击硬直、无敌帧
AI        巡逻 / 警戒 / 追击 / 攻击 / 返回
```

> 这些都属于 `gamedev-skill-routing.md` 的"学科维"，
> 与"引擎维"正交组合。
