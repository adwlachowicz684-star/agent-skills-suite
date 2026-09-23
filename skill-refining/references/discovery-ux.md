# 可发现性：用户怎么知道技能存在

> **技能写得再好，用户不知道它存在就等于不存在。**
> 这一章讲**用户侧**的发现机制——与 `skill-evaluating` 的 `triggering.md` 讲的**模型侧**匹配是两回事。

## 目录

- [三种触发方式](#三种触发方式)
- [怎么查当前有哪些技能](#怎么查当前有哪些技能)
- [发现层级与优先级](#发现层级与优先级)
- [管理命令](#管理命令)
- [装太多会怎样](#装太多会怎样)
- [帮用户找技能](#帮用户找技能)

---

## 三种触发方式

```
① 自动匹配   你说需求 → 模型拿你说的话比对每个 description → 命中则调出
② 手动喊名字 打 /技能名
③ 直接问     "现在有哪些 Skill 可用？"
```

> ⭐ **日常更推荐第 ① 种——说需求就行，触发交给它。**
>
> 这也反过来说明 description 该怎么写：
> **必须包含"用户会自然说出口的关键词"**，
> 而不是技能的内部命名或技术术语。

> 官方排查"技能没触发"的**第一条就是查这个**：
> **检查描述是否包含用户会自然说的关键字。**

---

## 怎么查当前有哪些技能

```
□ 装了一堆、内置一堆，怎么知道现在手上有啥？
  → 最直接：问它 "现在有哪些 Skill 可用？"
  ⭐ 这也是官方排查技能问题的标准动作之一
     ——先确认它到底在不在列表里，再谈触发

□ 打 / 调出命令菜单，能看到可手动调用的那些

□ /doctor 能查"技能描述是不是因为装太多被截断了"
```

> ⚠️ **最后这条极其重要，见下文"装太多会怎样"。**

---

## 发现层级与优先级

> 不同客户端层数不同，但结构相似。以 Gemini CLI 为例（四层，低→高）：

```
1. 内置技能      随客户端提供的标准技能
2. 扩展技能      捆绑在已安装扩展中的
3. 用户技能      ~/.gemini/skills/ 或 ~/.agents/skills/
4. 工作区技能    .gemini/skills/ 或 .agents/skills/（随版本控制与团队共享）
```

**同名覆盖规则**：

```
□ 高优先级位置覆盖低优先级
□ 同一层内，.agents/skills/ 别名优先于厂商专属目录
  ——这个别名提供跨 AI 工具兼容的互操作路径
```

> 对照 `skill-authoring` 的 `skill-crafting` 的 `skill-structuring` 的 `directory-contract.md`：
> **跨客户端分发优先用 `.agents/skills/`**，正是因为它在这个优先级里占位。

**生命周期**：

```
发现 Discovery   启动时扫描各层，把已启用技能的名称与描述注入系统提示
激活 Activation  模型判断任务匹配某 description 时，调用 activate_skill
确认 Consent      ⭐ UI 弹确认，展示技能名称、用途、以及它将获得的目录访问路径
注入 Injection   批准后：SKILL.md 正文与目录结构加入会话；
                 技能目录加入 agent 的允许文件路径（可读其打包资源）
执行 Execution   模型带着专业能力继续
```

> ⭐ **Consent 这一步值得注意**——
> 它把"这个技能将能访问哪个目录"**显式摆给用户**。
> 这正是 `skill-governance` 的 `sandbox-execution.md` 里权限最小化在交互层的体现。

---

## 管理命令

**会话内**（以 `/skills` 为例）：

```
/skills list [all] [nodesc]   列出已发现技能
                              all 含内置，nodesc 隐藏描述
/skills link <路径> [--scope] 从本地目录链接技能
/skills disable <名>          禁用
/skills enable <名>           重新启用
/skills reload                从所有层级刷新
```

**终端**：

```bash
gemini skills list --all
gemini skills install https://github.com/user/repo.git --consent
gemini skills uninstall my-skill --scope workspace
```

**通用 CLI**（`npx skills`）：

```bash
npx skills find [query]      # 搜索
npx skills add <源>          # 安装
npx skills list              # 已安装
npx skills check             # 检查更新
npx skills update            # 升级全部
npx skills remove <名>       # 卸载
```

---

## 装太多会怎样

> ⭐ **这是最该记住的一条**：

```
装的技能多到一定程度，
描述会被压缩以省字符预算，
⚠️ 可能把匹配用的关键词削掉。
```

也就是说——**你精心写进 description 的触发词，可能根本没进上下文。**
这解释了为什么"我明明写了触发词却还是不触发"。

**缓解手段**：

```
□ 定期用 /skill-doctor 查：
  每个技能占多少上下文、被调用多频繁、有没有被截断
□ 关掉从没用过的技能（呼应 library-ops.md 的清库）
□ ⭐ 合并功能重叠的技能、对技能分类分组
□ 定期审计技能描述的差异化程度
```

> 呼应 `skill-evaluating` 的 `metrics.md` 里"候选池 5 → 100 精确率掉 10 倍"：
> **技能库从 17 个涨到 100+ 时，描述开始重叠，agent 频繁选错。**

---

## 帮用户找技能

> 生态里已经出现了专门的 `find-skills` 技能
> （安装量榜首，77 万+），它做的事值得抄进团队技能库：

```
触发语："how do I do X" · "find a skill for X" ·
        "is there a skill that can..." · "can you do X"

流程：
1. 理解需求——领域是什么、具体任务是什么、
   是否常见到可能已有现成技能
2. 搜索——npx skills find <query>
3. 呈现选项——技能名 + 做什么 + 安装命令 + 详情链接
4. 询问是否安装
```

**搜索技巧**：

```
□ 用具体关键词："react testing" 比 "testing" 好
□ 试同义替换：deploy 不行就试 deployment / ci-cd
□ 看热门来源：vercel-labs/agent-skills、ComposioHQ/awesome-claude-skills
```

> ⭐ **找不到时怎么办**——这个处理很值得学：
> **承认没找到 → 用通用能力直接帮忙 → 建议用户可以自己创建一个**
> (`npx skills init`)。不硬凑一个不存在的答案。

---

## 自查

```
□ 用户能否用一句话问出"现在有哪些技能"？
□ description 是否包含用户自然说出口的关键词？
□ 是否知道本客户端的发现层级与同名覆盖规则？
□ 跨客户端分发是否放在 .agents/skills/？
□ 是否定期跑 /skill-doctor 查截断与调用频次？
□ 技能数量是否已多到描述被压缩？（是→清库或分组）
□ 是否有技能之间的描述重叠？
□ 是否提供了"找不到技能"的优雅降级路径？
□ 安装第三方技能前是否看过它将获得的目录访问路径？
```
