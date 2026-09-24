# 同名覆盖与冲突：三级命名空间与审计

> 相关：《skill-orchestration》的 `namespace-collision.md` ·
> 《skill-distribution》的 `enterprise-registry.md` ·
> `distribution-three-ways.md`

---

## 目录

- [1. ⭐ 覆盖优先级（从低到高）](#1--覆盖优先级从低到高)
- [2. 三条裁决规则](#2-三条裁决规则)
- [3. ⭐ 冲突的真实事故](#3--冲突的真实事故)
- [4. ⭐ 三个防冲突策略](#4--三个防冲突策略)
- [5. 审计技能](#5-审计技能)

---

## 1. ⭐ 覆盖优先级（从低到高）

```
1（最低） 项目全局目录  ~/.agentscope/skills
2         技能市场      skillRepository —— 后注册的覆盖先注册的
3         工作区公共    workspace/skills —— 覆盖全部市场与全局
4（最高） 用户私有      {userId}/skills —— 只对本人生效
```

**另一种口径**（Claude Code 侧）：

```
⭐ 唯一的覆盖顺序是：enterprise > personal > project
⭐ ⭐ 越"全局"的位置越赢——这与直觉相反
```

> ⭐ 两个口径不一致，说明**各客户端实现不同**。
> 所以不要记死顺序，**要实际审计**（见第 5 节）。

---

## 2. 三条裁决规则

以 Superpowers 的机制为例：

```
场景                       实际加载
个人与官方同名都存在        ⭐ 个人技能
只有官方存在               官方技能
显式 superpowers: 前缀     官方技能
```

可记为：

```
① ⭐ 默认个人优先
② ⭐ 前缀强制官方
③ ⭐ 缺失自动回退
```

**类比**：很像本地 `.env` 覆盖全局配置——**不做合并，就近者生效**。

> ⭐ "不做合并" 这点很关键：
> 你可能会以为个人版会补充官方版缺失的部分，**不会，是直接替换**。

**共存**：两类技能可以和平共存——
你可以逐个把自己的版本替换上去做渐进式升级，
官方新版也不会冲掉你的改动。

---

## 3. ⭐ 冲突的真实事故

> ⭐ **8 人团队共享项目里的 deploy 技能。
> Alice 有个人的 deploy 技能（跳过测试，她用于 hotfix）。
> Bob 装的插件里也有个 deploy 技能。**
>
> ```
> Alice 输入 /deploy → 拿到她的个人版（跳过测试）
> Bob   输入 /deploy → 拿到项目版（跑完整测试）
> 插件版显示为 plugin-name:deploy
> ```
>
> ⭐ **没人知道谁拿到的是什么，
> 然后一次跳过了测试的生产部署就这么跑出去了。**

> ⭐ 这个事故说明：
> **同名覆盖的危险不在于"技术冲突"，而在于"无人知道当前生效的是哪一份"。**

---

## 4. ⭐ 三个防冲突策略

**策略一：个人技能命名约定**

```
~/.claude/skills/my-deploy/SKILL.md   # 个人
.claude/skills/deploy/SKILL.md        # 项目（团队标准）

⭐ /deploy     永远跑团队版
⭐ /my-deploy  跑个人版
⭐ 不会撞车
```

> ⭐ **最简单也最有效**——一个前缀解决问题。

**策略二：在项目 CLAUDE.md 里声明所有权**

```markdown
## Skills
项目技能在 `.claude/skills/`:
- `deploy`     生产部署（⭐ 不要用个人技能覆盖）
- `code-review` 团队代码评审标准
个人技能应使用 `my-` 前缀以避免冲突。
```

**策略三：关键团队技能做成插件**

```
⭐ 插件技能住在独立命名空间里，
⭐ 不会被个人或项目技能覆盖。
代价：开发者要输入 plugin-name:skill-name
```

---

## 5. 审计技能

一个可直接抄的审计技能形态：

```
1. 列出个人技能   ls ~/.claude/skills/
2. 列出项目技能   ls .claude/skills/
3. ⭐ 对每个同时出现在两处的技能名：
     标记为 CONFLICT
     报告哪个版本胜出
     ⭐ 显示两个版本的 description
4. 列出所有技能名及其生效作用域
```

输出：

```
SKILL AUDIT REPORT
==================
Personal skills: [count]
Project skills:  [count]

CONFLICTS:
  deploy — personal overrides project
    Personal: "Deploy to prod (skips tests)"
    Project:  "Deploy to prod (runs full test suite)"

NO CONFLICTS:
  code-review  — project only
  explain-code — personal only
```

> ⭐ 显示两个版本的 description 这一步最关键——
> 因为**差异往往就藏在描述里**（一个说跳过测试，一个说跑全套）。

**其他常见问题**：

```
开发者个人技能覆盖团队标准 → ls 一下，加 my- 前缀或删掉
技能在有些人那能用有些人不能 → ⭐ 检查各人的个人技能目录
新技能不出现                 → ⭐ 只有 .claude/skills/ 是本次会话中首次创建时才需重启
monorepo 里子目录的技能       → ⭐ 只在处理该子目录文件时才被发现
不知道哪个版本生效           → ⭐ 直接问 agent："有哪些技能可用？"
```

---

## 速查

```
□ 个人技能统一加 my- 前缀
□ ⭐ 关键团队技能做成插件（独立命名空间，不可覆盖）
□ CLAUDE.md 里声明所有权与禁止覆盖项
□ ⭐ 定期跑审计，显示冲突双方的 description
□ ⭐ 覆盖是替换不是合并
□ ⭐ 各客户端优先级顺序不同——要实测，别记死
□ 想知道哪个生效 → 直接问 agent
```

**一句话**：

> ⭐ **冲突的危险不在技术，在于没人知道当前生效的是哪一份。**
