# 变更日志与发布说明

> Changelog 是"确定性生成"的绝佳范例：
> 输入是 git 历史，输出有固定分类，**不该交给模型自由发挥**。

## 目录

- [生成流程](#生成流程)
- [Conventional Commits](#conventional-commits)
- [技术语言 → 用户语言](#技术语言--用户语言)
- [七类变更](#七类变更)
- [好/坏条目对照](#好坏条目对照)
- [版本号的自动推导](#版本号的自动推导)

## 生成流程

```
1. 扫描 git 历史
   □ 特定时间段 / 两个版本或 tag 之间 / 自上次发布 / 自定义日期范围
   □ 提取：提交信息、作者、日期、改动文件、提交类型

2. 分类
   □ 功能 / 改进 / 缺陷修复 / ⭐ 破坏性变更 /
     安全 / 废弃 / 文档 / 内部（⭐ 通常排除）

3. ⭐ 技术语言 → 用户语言（见下）

4. 格式化
```

> ⭐ **第 2 步的"内部"类通常要排除**——
> 重构、测试、CI/CD 对用户不可见。
> 这条不写进技能，agent 会把一堆 refactor 塞进 changelog。

## Conventional Commits

```
格式：<type>[optional scope]: <description>

      [optional body]

      [optional footer(s)]
```

**类型 → changelog 分区的映射**：

| 类型 | 含义 | Changelog 分区 |
|---|---|---|
| `feat` | 新功能 | Added |
| `fix` | 缺陷修复 | Fixed |
| `docs` | 文档 | ⭐ 通常跳过 |
| `style` | 格式 | ⭐ 通常跳过 |
| `refactor` | 重构 | Changed |
| `perf` | 性能提升 | Changed |
| `test` | 测试 | ⭐ 通常跳过 |
| `chore` | 维护 | ⭐ 通常跳过 |
| `ci` | CI 配置 | ⭐ 通常跳过 |
| `build` | 构建系统 | ⭐ 通常跳过 |

**破坏性变更的两种标法**：

```
1. 感叹号：  feat!: 或 feat(scope)!:
2. 脚注：    BREAKING CHANGE: <描述>
```

**自动生成的三条命令**：

```bash
# 自上次 tag 以来的所有提交
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s (%h)"

# 按类型分组（需 conventional commits）
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%s" \
  | grep -E "^feat" | sed 's/^feat[^:]*: /- /'

# 带日期
git log $(git describe --tags --abbrev=0)..HEAD \
  --pretty=format:"- %s (%ad)" --date=short
```

> 也可直接上工具：
> `conventional-changelog -p angular -i CHANGELOG.md -s`
> `standard-version`

## 技术语言 → 用户语言

> ⭐ **这是 changelog 技能的核心价值**——
> 提交信息是写给开发者的，changelog 是写给用户的。

```
技术提交：fix: resolve null pointer exception in user service
用户表达：修复了用户资料无法加载的问题
```

**四条转换规则**：

```
□ 去掉技术术语
□ ⭐ 聚焦用户影响（用户会注意到什么）
□ 用清晰、面向动作的语言
□ 合并相关改动
```

## 七类变更

```
Added      新功能
Changed    既有功能的改动
Deprecated 即将移除的功能
Removed    已移除的功能
Fixed      缺陷修复
Security   漏洞修复 ⭐
Breaking   破坏性变更 ⭐（需附迁移说明）
```

**标准格式**：

```markdown
## [Version] - YYYY-MM-DD

### ✨ Added
### 🔧 Changed
### 🐛 Fixed
### 🔒 Security
### ⚠️ Breaking Changes
### 📝 Deprecated
### 🗑️ Removed
```

## 好/坏条目对照

**✅ 好**：

```markdown
### Added
- 报表支持导出 CSV（#123）
- 常用操作快捷键（Ctrl+S 保存）

### Fixed
- 处理大文件时的内存泄漏（#456）
- 国际用户的时区显示错误
```

**❌ 坏**：

```markdown
### Added
- Added stuff            # 太含糊
- New feature            # 什么功能？
- Updated deps           # 不属于 Added，且太含糊

### Fixed
- Fixed bug              # 哪个 bug？
- Fix                    # 没有描述
- Fixes #123             # 应描述修了什么
```

**写作要点**：

```
□ ⭐ 以动词开头（Add / Fix / Update / Remove / Improve）
□ 具体：说明改了什么以及为什么
□ 带上 issue/PR 引用
□ ⭐ 想用户所想：他们需要知道什么
□ 合并相关改动，不要重复条目
```

**不该写**：

```
□ 内部重构
□ 没有解释的技术术语
□ 含糊的条目
```

## 版本号的自动推导

```
fix:            → PATCH
feat:           → MINOR
BREAKING CHANGE: 或 !: → MAJOR
```

**SemVer 格式**：`MAJOR.MINOR.PATCH`

```
MAJOR  破坏性变更、不兼容的 API 改动
MINOR  新功能，向后兼容
PATCH  缺陷修复，向后兼容
```

预发布：`1.0.0-alpha.1` / `1.0.0-beta.1` / `1.0.0-rc.1`

**版本链接**：

```markdown
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
```

## 质量清单

```
□ 所有用户可见的改动都已记录
□ ⭐ 破坏性变更被突出显示
□ issue/PR 编号已链接
□ 版本号遵循 SemVer
□ 日期用 ISO 格式（YYYY-MM-DD）
□ 条目按类型分组
□ ⭐ 安全修复被显著标注
```

> ⭐ 呼应 `release-versioning.md`（**`skill-distribution`**）：
> 技能自己的 CHANGELOG 还要额外写"哪些 agent 受影响"——
> 那是技能与普通项目 changelog 的关键差异。

## 自查

- [ ] 排除了 docs/style/test/chore/ci/build 这几类吗？
- [ ] 技术语言转成用户语言了吗？
- [ ] 破坏性变更有迁移说明吗？
- [ ] 条目以动词开头且具体吗？
- [ ] 安全修复显著标注了吗？
- [ ] 版本号由 conventional commits 自动推导吗？
- [ ] 日期是 ISO 格式吗？
