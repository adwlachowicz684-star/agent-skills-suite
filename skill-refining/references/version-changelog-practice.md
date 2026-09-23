# 版本与 Changelog：三种记录方式与四个常见错误

> 相关：《skill-refining》的 `version-strategy.md` ·
> `iteration-three-levels.md` · 《skill-governance》的 `retirement-pipeline.md`

---

## 目录

- [1. ⭐ 为什么需要版本](#1--为什么需要版本)
- [2. SemVer 三类变更的判定](#2-semver-三类变更的判定)
- [3. ⭐ 三种记录方式](#3--三种记录方式)
- [4. ⭐ 四个常见错误](#4--四个常见错误)
- [5. 破坏性变更的处理](#5-破坏性变更的处理)

---

## 1. ⭐ 为什么需要版本

```
没有版本管理就会出现：
  项目 A 用 v1.0 的 code-review
  项目 B 用 v2.0 的 code-review
  ⭐ 两人审查标准不一致
```

frontmatter 示例：

```yaml
---
name: code-review
version: 2.1.0
description: 代码审查 Skill
updated: 2026-07-10
author: 开发者A
---
```

> ⭐ `author` 有个少有人知的用途：
> **多技能共存时，它是 `claude code list` 输出的唯一分组依据**——
> 想让 frontend-team 和 backend-team 在面板里自动分组，靠的就是它。

---

## 2. SemVer 三类变更的判定

**MAJOR（破坏性）**：

```
· 技能推荐的方法发生根本改变
· 内容大幅重构
· ⭐ 技能范围变化（变宽或变窄）
· 前置条件实质变化
· ⭐ ⭐ 按旧版本做会做出错的事
```

**MINOR（新增）**：

```
· 新增章节
· 新增示例或模式
· 适配新的库/工具版本
· 扩展已有主题的覆盖
· 新增平台支持
· 向后兼容的改进
```

**PATCH（修复）**：

```
· 错别字 · 格式修正
· ⭐ 不引入新内容的澄清
· 修复失效链接
· 代码示例的 bug 修复
· 输出/结果纠正
```

> ⭐ MAJOR 的判定与 `iteration-three-levels.md` 那条一致：
> **不是"改了多少字"，而是"按旧版本用会不会错"**。

一个具体例子：

```
MAJOR  报告格式从 JSON 改为 Markdown 表格
MINOR  给 pdf 技能新增图片提取
PATCH  修复 pdf 技能的文本提取准确率
```

---

## 3. ⭐ 三种记录方式

**方式一：技能文件内的 Changelog 章节**

```markdown
## Changelog
- 2.1.0 (2025-12-15): 新增 WebGPU 示例，Three.js 升到 r170
- 2.0.0 (2025-06-01): 为 React 19 重写，Server Components 新方案
- 1.2.0 (2025-03-10): 新增测试章节与新代码示例
```

> ⭐ **团队维护的技能尤其该用这一种**：
> ⭐ **Changelog 随文件走——一个孤立拿到这个文件的人，
> 不需要 git 权限就能立刻看到它的历史。**

**方式二：Git 追踪**

```
frontmatter 里放 version
git tag 打发布版本（skill-name/v1.0.0）
git log 提供变更历史
版本间 diff 显示究竟改了什么
```

**方式三：外部版本注册中心**

```
集中式版本目录 · 追踪全部技能与版本
提供检查最新版本的 API · 可通知用户更新
```

> ⭐ **建议：⭐ 两者都用——
> git tag 给工具集成用，内嵌 changelog 给人读。**

---

## 4. ⭐ 四个常见错误

**① 为了省事跳过 MAJOR**

```
⭐ 有些人不愿跳主版本，怕用户不便。
⭐ 这造成混淆——用户会以为次版本更新总是安全的。
   一个 3.9.1 但其实两版前引入过破坏性变更的技能，
   会误导用户对稳定性的判断。

⭐ 接受这个摩擦。⭐ 破坏时就跳主版本。
   用户第一次设置自动更新检查时就会感谢你。
```

**② patch 版本不一致**

```
⭐ patch 应该修 bug，不应该引入特性。
   在 patch 里给命令加一个新参数会破坏 semver 约定。
   筛选"仅 bug 修复"的用户会拿到意外行为。
```

**③ 不记录破坏性变更**

> ⭐ **一个没有迁移说明的 MAJOR 版本，
> 只是一个附带着数字的挫折。**

**④ 永远停在 0.x**

```
⭐ 有人一直留在 0.x.y，因为 0.x 理论上表示"什么都可能变"。
⭐ 这是逃避——一旦你的技能稳定到别人可以依赖它，
   就承诺 1.0.0 并从那里开始遵守 semver 契约。
```

**第五条**（很实用）：

```
⭐ 技能文件里写 1.2.0 但 git tag 是 v1.1.0 → 你有问题
⭐ 自动化版本管理，或至少加一个 pre-commit 检查两者一致
```

---

## 5. 破坏性变更的处理

**时间线**（与 `retirement-pipeline.md` 的四阶段互补）：

| 阶段 | 时长 | 动作 |
|---|---|---|
| 公告 | ⭐ 破坏性变更前 ≥30 天 | 加 `deprecation_notice` 到 frontmatter，写进 changelog |
| ⭐ 并行支持 | ⭐ 60–90 天 | ⭐ 通过 flag 同时支持新旧行为 |
| 软移除 | 30 天 | 移除旧行为，发布 legacy 技能，迁移文档定稿 |
| 硬移除 | 窗口关闭后 | 归档 legacy 技能，关闭旧 issue |

> ⭐ **高流量或面向企业的技能，并行支持应考虑延长到 6 个月。**

**声明方式**：

```yaml
---
name: "Unit Test Generator (Legacy)"
version: "1.5.0"
description: "Generates Jest unit tests - DEPRECATED, use Unit Test Generator v2.x instead"
stability: "deprecated"
deprecation_notice: |
  This skill will receive security fixes only until 2026-12-31.
  Migrate to Unit Test Generator v2.x...
---
```

**迁移指南该含什么**：

```
· 改了什么
· ⭐ 为什么改
· 逐步迁移步骤
· ⭐ 旧行为的临时开关（如 --legacy）及其移除版本
· 求助渠道
```

**灰度发布**（重大变更前）：

```
1. 建 feature/code-review-v3 分支
2. ⭐ 在 2-3 个项目中试点
3. 收集反馈、修正
4. 合并到 main，更新为 v3.0.0
5. ⭐ 通知团队所有人更新
```

---

## 速查

```
□ MAJOR：⭐ 按旧版做会出错（不是改了多少字）
□ MINOR：新增章节/示例/平台，向后兼容
□ PATCH：错别字/澄清/坏链/示例 bug（⭐ 不引入特性）

三种记录：
□ ⭐ 文件内 Changelog（⭐ 随文件走，不需 git）
□ git tag（工具集成）
□ 外部注册中心
□ ⭐ 建议：tag + 内嵌 changelog 都用

四错误：
□ ⭐ 怕麻烦跳 MAJOR → 误导用户以为次版本安全
□ ⭐ patch 里加特性 → 破坏 semver
□ ⭐ 不写迁移说明的 MAJOR = 带数字的挫折
□ ⭐ 永远 0.x = 逃避
□ ⭐ 文件内版本号与 git tag 要一致（pre-commit 检查）

破坏性变更：
□ 公告 ≥30 天
□ ⭐ 并行支持 60-90 天（企业 6 个月）
□ 软移除 30 天
□ 硬移除
□ ⭐ 迁移指南含：改了什么/为什么/步骤/临时开关/求助
□ 灰度：2-3 个项目试点再全量
□ ⭐ author 字段是 list 命令的唯一分组依据
```

**一句话**：

> ⭐ **Changelog 随文件走——孤立拿到这个文件的人，
> 不需要 git 权限就能看见它的历史。**
