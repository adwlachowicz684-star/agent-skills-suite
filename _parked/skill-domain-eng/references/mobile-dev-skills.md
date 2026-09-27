# 移动端开发类技能

> ⭐ **为什么移动端特别需要技能**：
> 框架专属约定极易出错——**屏幕生命周期、导航模式、状态管理、平台特定 API**，
> 通用模型默认写不对。

## 目录

- [按框架分](#按框架分)
- [跨平台关注点](#跨平台关注点)
- [哪些内容最值得编码](#哪些内容最值得编码)

---

## 按框架分

**React Native**（与标准 React 的差异点才是重点）：

```
□ 导航——React Navigation 或 Expo Router
□ ⭐ 平台特定代码分支
□ 原生模块集成
□ ⭐ 性能优化（FlatList 与动画）
□ ⭐ 新架构（Fabric 与 TurboModules）的正确使用
```

```
高频痛点（技能最该覆盖的）
□ ⭐ 跨平台键盘处理
□ 图片缓存与优化
□ ⭐ 离线优先的数据模式（AsyncStorage / MMKV）
□ 推送通知配置
```

**Flutter**：

```
□ Dart 约定与 Flutter 专属模式
□ ⭐ 组件组合
□ 状态管理（Riverpod / Bloc / Provider）
□ 导航（GoRouter）
□ 平台通道通信
□ ⭐ 不同屏幕尺寸的响应式布局
□ ⭐ 构建与发布流水线——生成正确的应用图标、闪屏、
   平台特定配置文件
```

**原生 iOS（Swift）**：

```
□ SwiftUI 模式（视图组合、属性包装器、environment objects）
□ UIKit 模式（遗留代码）
□ Core Data 建模
□ Combine / async-await
□ ⭐ Apple 专属要求——agent 最容易漏的部分：
   privacy manifest 条目 · entitlements · App Store 审核指南合规
```

**原生 Android（Kotlin）**：

```
□ Jetpack Compose 模式
□ ViewModel 架构
□ Room 数据库配置
□ Coroutines 异步
□ Material Design 3 组件
□ ⭐ 正确的生命周期处理，避免常见内存泄漏模式
```

---

## 跨平台关注点

> ⭐ **这些尤其有价值，因为两边都要对**：

```
□ 响应式设计模式
□ ⭐ 无障碍实现（VoiceOver / TalkBack）
□ ⭐ 深链配置
□ ⭐ 认证流程（生物识别、OAuth）——要在两个平台上都能工作
```

> 呼应 `a11y-skills.md`：移动端的无障碍不是"可选项"，
> 而且**平台特有的读屏器行为必须单独处理**。

---

## 哪些内容最值得编码

> ⭐ **判断标准：是不是"框架专属、通用模型默认写错"的**：

```
✅ 高价值（写进技能）
□ 生命周期与内存泄漏模式
□ ⭐ 平台特定 API 与权限/隐私清单
□ 导航与深链
□ 状态管理选型与约定
□ ⭐ 发布相关的配置（图标、闪屏、 entitlements、审核要求）
□ 离线优先与缓存策略

❌ 低价值（模型本来就会）
□ 通用语法
□ 标准库用法
□ 与 Web 相同的通用模式
```

> ⭐ 呼应 `skill-domain-biz` 的 `writing-org-context.md` 的判断：
> **一致性比创造性重要 + 强依赖组织/平台语境 → 做成技能**。
> 移动端恰好两条都满足。

---

## 自查

```
□ 是否覆盖了与通用开发的"差异点"（而非重复常识）？
□ React Native 是否含新架构（Fabric/TurboModules）？
□ 是否含跨平台键盘处理、图片缓存、离线优先？
□ Flutter 是否含状态管理选型与发布配置？
□ ⭐ iOS 是否含 privacy manifest、entitlements、审核合规？
□ Android 是否含生命周期与内存泄漏模式？
□ ⭐ 是否含跨平台无障碍（VoiceOver/TalkBack）？
□ 是否含深链与认证流程？
□ 是否区分了"高价值编码"与"模型本来就会"？
□ 是否按框架/平台分开组织（而非一个大技能）？
□ 是否含发布流水线配置（图标、闪屏、配置文件）？
```
