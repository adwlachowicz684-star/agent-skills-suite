# 发布、版本与回滚

> ⭐ **一条来自真实事故的规则**：
> **所有安装命令都必须带 `#vX.Y.Z` 后缀。**

## 目录

- [语义化版本与提交前缀](#语义化版本与提交前缀)
- [git tag 与发布](#git-tag-与发布)
- [回滚](#回滚)
- [不兼容变更的迁移指引](#不兼容变更的迁移指引)
- [gh skill：溯源与锁定](#gh-skill溯源与锁定)
- [发布前检查清单](#发布前检查清单)
- [更新提醒机制](#更新提醒机制)

---

## 语义化版本与提交前缀

```
MAJOR.MINOR.PATCH
```

**推荐提交信息前缀**（这是语义化发布能自动化的前提）：

| 前缀 | 含义 | 例子 |
|---|---|---|
| `feat:` | 新功能 | 新增 Excel 输出支持 |
| `fix:` | Bug 修复 | 修复空文件时的崩溃 |
| `docs:` | 文档更新 | 补充参数说明 |
| `refactor:` | 重构（无功能变化） | 将清洗逻辑抽成独立函数 |
| `perf:` | 性能优化 | 大文件处理速度提升 3 倍 |

**版本变更的边界**（呼应 `versioning-compat.md`）：

```
1.0.1  patch   修处理规则里的 bug
1.1.0  minor   新增一种输出格式
⭐ 2.0.0  major   ⭐ 改变了输入契约（也包含改触发语义）
```

```
□ ⭐ 破坏性变更必须提升 minor 或 major，并单独通知，
   ⭐ 不能混在普通修复里
```

**模块化发布**（多技能仓库的实用技巧）：

```json
{
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/npm", { "npmPublish": true }],
    ["@semantic-release/github", { "assets": ["dist/**"] }]
  ],
  "branches": ["main", "next"]
}
```

```
□ ⭐ 定制 commit-analyzer 的 preset：
   feat(weather) 只触发 weather 模块的 minor 版本，
   ⭐ 不影响 calendar 或 translation 模块
□ 发布产物自动归档——每个技能模块设 publishConfig，
   semantic-release 自动打包 dist/，无需手动 build
```

---

## git tag 与发布

```bash
cd my-skill && git init
git add . && git commit -m "feat: 初始版本 v1.0.0"

# 稳定版本打标签
git tag v1.0.1
git tag -a v1.1.0 -m "新增多文件批量处理功能"

# ⭐ 发布时指定 tag
skills add ./src/skills/weather-forecast#v1.1.0 --g
```

> ⭐ **一个真实教训**：
> 同事直接 `skills add ./path` 覆盖了生产环境的 v1.0.0，
> 导致**下游所有依赖它的调度技能全部中断**。
> → 团队后来强制要求：**所有 add 命令必须带 `#vX.Y.Z` 后缀**。

---

## 回滚

```bash
# 查看历史
git log --oneline
git tag

# 回退到指定标签或提交
git checkout v1.1.0
git checkout a3f7b2c

# 若需从回退版本继续开发
git checkout -b hotfix/v1.1.1 v1.1.0
```

**回滚的四条策略**：

```
□ ⭐ 每个正式版本都对应一个 git tag——回滚就是切回上一个 tag
□ ⭐ registry 中保留最近几个版本记录，⭐ 不要只保留最新一条
□ ⭐ 多个技能之间存在依赖时，回滚要成组处理
   ——避免出现 A 是新版、B 是旧版的不一致状态
□ ⭐ 生产环境的技能更新建议走内部发布服务，控制写入权限，
   避免任意成员临时修改
```

**依赖版本冲突**（这类系统特有的问题）：

```
症状  schedule-reminder 声明依赖 calendar-today@1.0.0，
      而你注册的是 calendar-today@1.1.0 → Runtime 拒绝加载

解法  方案1 降级注册（推荐）
        skills remove calendar-today
        skills add path/to/calendar-today@1.0.0 --g -y
      方案2 更新调度技能定义里的 dependencies

缓存损坏时  skills cache clear && skills agent restart
```

> ⭐ **依赖声明是双刃剑**：它防止了错配，
> 但也意味着**一个技能升级可能连锁打断下游**——
> 所以回滚必须成组。

---

## 不兼容变更的迁移指引

> ⭐ **发生不兼容变更时，必须给现有用户明确的迁移指引**：

```markdown
## 迁移指南：从 v1.x 升级到 v2.0

### 主要变化
v2.0 修改了输出文件命名规则：
`output.xlsx` → `output_YYYYMMDD.xlsx`

### 受影响场景
如果你的工作流依赖固定的输出文件名，需要在使用时重命名，
或使用 `--output` 参数指定文件名。

### 迁移步骤
1. 更新技能到 v2.0
2. 检查是否有依赖固定文件名的脚本或工作流
3. 如有，添加 `--output output.xlsx` 保持旧行为
```

```
□ ⭐ 不兼容变更应在发布前充分评估影响范围
□ ⭐ 若使用者众多，考虑保留旧参数并标记为"已废弃"，
   给用户过渡时间，⭐ 而不是直接删除
```

**CHANGELOG 写在 SKILL.md 末尾**（帮助使用者了解每个版本的改动）：

```markdown
## 版本历史
### v1.2.0（2026-05-18）
- 新增：支持 .xlsx 输入格式
- 优化：大文件（>10MB）处理速度提升 40%
### v1.1.0（2026-04-10）
- 新增：--col 参数，支持只分析指定列
- 修复：列名包含空格时的解析错误
```

---

## gh skill：溯源与锁定

> ⭐ **这套机制解决了"技能从哪来、现在是不是那份"的问题**：

**内容寻址变更检测**：

```
□ ⭐ 每个已安装技能都记录了源目录的 git tree SHA
□ 执行 update 时比较本地与远端 SHA
□ ⭐ 检测的是实际内容变化，而不只是版本号
```

**可移植的溯源信息**：

```
□ ⭐ 安装时把仓库名、引用、tree SHA 直接写进 SKILL.md 的 frontmatter
□ ⭐ 溯源数据随技能文件一起移动——
   无论技能被复制到哪个项目，都能追踪来源并完成更新
```

**锁定与不可变发布**：

```bash
# 锁定到发布 tag
gh skill install github/awesome-copilot documentation-writer --pin v1.2.0
# 锁定到提交，获得最高可复现性
gh skill install github/awesome-copilot documentation-writer --pin abc123def

# ⭐ 被锁定的技能在执行 gh skill update 时会被跳过
#   ——升级变成主动操作而非被动接受
```

```
□ 不可变发布：一旦启用，⭐ 即便仓库管理员也无法修改已发布版本
□ 通过 tag 锁定安装的用户可获得完整保护
```

**更新与发布**：

```bash
gh skill update            # 交互式检查更新
gh skill update git-commit # 更新指定技能
gh skill update --all      # 全量，不提示确认

gh skill publish           # 校验是否符合 agentskills.io 规范 + 检查远端安全设置
gh skill publish --fix     # 自动修复元数据问题
```

```
□ ⭐ publish 会检查远端仓库的安全设置
  （tag 保护、密钥扫描、代码扫描等）
□ 这些不是强制要求，但强烈建议开启——
  ⭐ 提升技能仓库的供应链安全性
```

---

## 发布前检查清单

```
□ version 必须递增，且与 CHANGELOG 最高版本一致
□ updated 必须更新为本次发布时间
□ ⭐ CHANGELOG 记录变更内容，并标注破坏性变更
□ ⭐ 本地至少运行一次技能的验证脚本
□ 远端比对——更新检查脚本能识别新版本
□ tag 已推送到远端
□ 通知——webhook 调用成功，内容含版本与变更摘要
```

---

## 更新提醒机制

> ⭐ **本质不是复杂系统，而是围绕四个环节的最小闭环**：
> **版本 · 变更记录 · 检查 · 通知**。

```
□ ⭐ 如果今天只改一件事：
   先把 SKILL.md 的 frontmatter 补上 version 字段，
   然后跑一次更新检查脚本——这条链路就立起来了
□ 一天发布多次时版本号可连续递增，
   ⭐ 但通知渠道应合并为每日汇总，或只在重要变更时通知
□ ⭐ 更新提醒脚本本身也要纳入测试
   ——解析失败时不能静默跳过，
     否则使用者会误以为"没有更新"，反而丢失提醒能力
```

---

## 自查

```
□ 是否用了语义化提交前缀（feat/fix/docs/refactor/perf）？
□ ⭐ 破坏性变更是否单独通知（不混在普通修复里）？
□ 多技能仓库是否定制了 commit-analyzer（按模块发版）？
□ ⭐ 安装命令是否强制带 #vX.Y.Z 后缀？
□ 每个正式版本是否都有 git tag？
□ ⭐ registry 是否保留了最近几个版本（而非只留最新）？
□ ⭐ 有依赖的技能是否成组回滚？
□ 生产环境更新是否受控（避免任意成员临时修改）？
□ ⭐ 不兼容变更是否有迁移指引（含受影响场景与步骤）？
□ 废弃参数是否保留过渡期（而非直接删除）？
□ CHANGELOG 是否写在 SKILL.md 末尾？
□ ⭐ 是否用了内容寻址（tree SHA）而非只看版本号？
□ 溯源信息是否可随技能文件移动？
□ ⭐ 生产安装是否 --pin 到 tag 或提交？
□ 是否了解不可变发布（连管理员也改不了已发布版本）？
□ 发布前清单是否全部走过？
□ ⭐ 更新提醒脚本是否纳入测试（解析失败不静默跳过）？
```
