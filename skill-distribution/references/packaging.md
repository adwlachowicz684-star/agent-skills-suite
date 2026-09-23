# 打包、分发与来源记录

> **一个技能如何从仓库进入 agent，以及这一路上必须记录什么。**

## 目录

- [仓库布局：为什么是扁平的](#仓库布局为什么是扁平的)
- [自包含原则](#自包含原则)
- [安装器与扫描规则](#安装器与扫描规则)
- [Marketplace 清单](#marketplace-清单)
- [来源记录 provenance](#来源记录-provenance)
- [发布检查清单](#发布检查清单)

---

## 仓库布局：为什么是扁平的

```
repo/
├── skills/
│   ├── <技能名>/          # 一个技能一个目录，直接在容器目录下
│   │   ├── SKILL.md
│   │   ├── SOURCES.yaml   # 来源记录（若改编自上游）
│   │   ├── NOTICE.md      # 生成的署名
│   │   ├── references/
│   │   ├── scripts/
│   │   ├── assets/
│   │   └── evals/
│   │       ├── evals.json
│   │       └── files/
│   └── <另一个技能>/       # 相同的内部结构
├── .claude-plugin/
│   └── marketplace.json    # 生成的分发清单
├── LICENSE
└── THIRD_PARTY_NOTICES.md  # 所有 NOTICE.md 的聚合
```

> **每个技能内部结构完全相同。**
> 这种统一性不是为了整洁——它让校验器、目录生成器、评测运行器
> **能对所有技能一视同仁**，而不用为每个特例写分支。

**为什么扁平**（不用分类子目录）：

```
□ 技能的身份就是"装着 SKILL.md 的那个目录"
  ——分类目录对身份没有贡献
□ 按名字选择技能，只有在扁平命名空间里名字唯一时才无歧义
□ 分类仍然可以做——作为 frontmatter 的 metadata 字段 + 生成的索引表
  这样有同样的分组效果，却不必让安装器、宿主、用户都去约定一个路径
```

---

## 自包含原则

> ⚠️ **技能内部任何文件都不得引用其外部的路径。**

```
安装器一次复制/软链接一个技能到 agent 目录，
所以一个爬出技能根的相对路径，安装后指向的是空。
```

**两个技能需要同一个 helper 时**：

```
✅ 复制这个小 helper
❌ 引入一个共享目录

复制的代价是一个文件；
断掉的相对路径的代价是整个技能——而且是静默失效，
只对那些单独安装它的用户。
```

---

## 安装器与扫描规则

**事实标准安装器** `npx skills`：

```bash
npx skills add owner/repo                    # GitHub 简写
npx skills add https://github.com/owner/repo
npx skills add https://github.com/owner/repo/tree/main/skills/name  # 单个技能
npx skills add https://gitlab.com/org/repo   # 任意 git 宿主
npx skills add git@github.com:owner/repo.git # SSH
npx skills add ./my-local-skills             # 本地路径
```

**常用 flag**：

```
--list              只枚举不安装
--skill <名>        可重复，'*' 全部
--agent <名>        '*' 全部，universal 为共享目录
-g                  用户级
--copy              复制而非软链接
-y                  非交互
```

**限制**：下载 10 MiB、解压 25 MiB、1000 个文件（可用环境变量覆盖）。

**扫描规则**（决定你的布局是否可被发现）：

```
□ 遍历固定的容器目录列表：仓库根（若有 SKILL.md）、skills/、
  其 .curated / .experimental / .system 子目录、
  .agents/skills/、.claude/skills/ 及约 50 个其他宿主目录
□ 每个容器最多向下走三层
□ ⚠️ 更浅层的 SKILL.md 会遮蔽其下嵌套的一切
  ——容器根上一个多余的 SKILL.md 会隐藏其下所有技能
□ --full-depth 可额外找到容器目录之外的
□ 标准位置找不到时会递归兜底——方便，但不要依赖
□ 只有技能根可以含 SKILL.md
```

> ⚠️ **遮蔽保护了安装器，但保护不了所有宿主**：
> 有些宿主递归扫描，把任何含 SKILL.md 的目录都当成技能。
> 所以 `evals/files/SKILL.md` 这样的测试夹具
> **会多发布一个名为 `files` 的坏技能**。
>
> → **给夹具按本质命名**：`widget-builder-SKILL.md`，
> 并在安装后断言数量：
> `find .agents/skills -name SKILL.md | wc -l` 必须等于技能数。

---

## Marketplace 清单

**`.claude-plugin/marketplace.json`（或 `plugin.json`）显式声明技能**，
安装器也读它；其中声明的路径按声明深度搜索，**免除三层遍历限制**。

```json
{
  "name": "my-marketplace",
  "metadata": { "description": "Example skills", "version": "1.0.0" },
  "plugins": [{
    "name": "document-skills",
    "source": "./",
    "skills": ["./skills/pdf", "./skills/xlsx"]
  }]
}
```

**必要字段**：

```
Catalog：name · owner{name,email} · metadata{description,version} · plugins[]
Plugin：name · source{source,url} · description（≤125 字符） ·
        version（语义化） · keywords[] · strict
```

**关键规则**：

```
□ name 必须 kebab-case 且唯一
□ 所有组件路径必须是相对路径且以 ./ 开头
□ 不允许 ../ 段；只用正斜杠
□ ⚠️ 组件目录绝不能放进 .claude-plugin/（只有清单能进）
```

---

## 来源记录 provenance

> 若技能改编自上游作品：

```
SOURCES.yaml  —— 记录来源
NOTICE.md     —— 生成的署名（每个技能一份）
THIRD_PARTY_NOTICES.md —— 全仓库聚合
```

**要记录什么**：

```
□ 来源 URL 与版本
□ 许可证
□ 上游漂移检查（定期检查上游是否变更）
□ 生成的署名文件
```

> ⚠️ **vendored 材料的许可证要单独记录**——
> 这是分发时最容易出法律问题的地方。

---

## 发布检查清单

```
□ 技能用 3+ 个压力场景测过
□ TEST_RESULTS.md 存在（含 agent 原话引用）
□ 字数 <1000（wc -w SKILL.md）
□ commands/ 里创建了斜杠命令（/help 可见性的必要条件）
□ manifest.json 把技能链接到命令
□ marketplace.json 符合 schema
□ 两个仓库都有 LICENSE（推荐 MIT）
□ README 有安装说明
□ ⚠️ 先建 git tag 再让用户安装——插件系统拉的是
  特定 git tag，不是 main 分支
```

**版本更新**（一个反直觉的坑）：

```
❌ /plugin update 只检查"新插件"，不做版本更新
✅ 版本更新 = 卸载 + 重装：
   /plugin uninstall <名>
   /plugin install <名>@<marketplace>
   然后重启（斜杠命令在启动时加载）
```

**安装后验证**：

```bash
ls ~/.claude/plugins/cache/<plugin-name>/            # 文件是否装上
cat ~/.claude/plugins/cache/<plugin-name>/.claude-plugin/manifest.json  # 版本
```

> 注意安装路径是 `~/.claude/plugins/cache/<name>/`，
> **不是** `~/.claude/skills/`。

**三种安装方式**（覆盖面从广到窄）：

```
1. 手动本地——最通用，新手首选；支持全局/项目级
2. CLI 一键——推荐用于 GitHub 开源技能
3. 平台市场一键——最省事
```

---

## 自查

```
□ 仓库布局是否扁平（一个技能一个目录，无分类子目录）？
□ 是否所有技能内部结构一致？
□ 技能内是否有指向其外部的相对路径？
□ 共享 helper 是否选择了复制而非共享目录？
□ 是否有 stray SKILL.md 遮蔽了其他技能？
□ 测试夹具是否按本质命名（避免被当成技能）？
□ 安装后是否断言了技能数量？
□ marketplace.json 字段是否齐全、路径是否以 ./ 开头？
□ 组件目录是否误放进了 .claude-plugin/？
□ 改编自上游的是否有 SOURCES.yaml 与 NOTICE.md？
□ 发布前是否先建了 git tag？
□ 是否在干净环境测过完整安装（卸载→重装→重启→/help 验证）？
```
